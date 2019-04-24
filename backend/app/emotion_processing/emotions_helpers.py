from keras.models import model_from_json
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2
import os
import tensorflow as tf
import librosa

# Explicitly declare some TF variables to prevent a couple bugs from showing up
global graph, model, a_model
graph = tf.get_default_graph()

# Constants
IMG_INPUT_WIDTH = 48  # Dimension of the input image to the model
PROBABILITY_THRESH = 0.4  # Has to be at least this probability for annotation in YouTube video
AUDIO_DURATION = 3.0
AUDIO_SR = 16000
EUC_DIST_THRES = 15  # If euclidean distance between top left corner of detected face in a frame and a previous frame, consider them the same face

# Load emotion model
models_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "models/")
model = load_model(os.path.join(models_path, "face_0330/face_0330.h5"))

face_detector = cv2.CascadeClassifier(os.path.join(models_path, 'haarcascade_frontalface_default.xml'))
emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

# Load audio model
a_model = load_model(os.path.join(models_path, 'audio_0408.h5'))
a_emotions = ["neutral", "happy", "sad", "angry", "fearful", "disgust", "surprised"]


def predict_emotion_from_audio(wav_name):
    ImageGen = ImageDataGenerator()

    audio_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "audio_files/")
    wav_file_path = os.path.join(audio_folder, wav_name)

    # Load file with librosa
    X, sample_rate = librosa.load(wav_file_path, res_type='kaiser_fast', duration=AUDIO_DURATION, sr=AUDIO_SR)
    sample_rate = np.array(sample_rate)

    # get mfccs transformation
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13)

    # Rehsape mfccs to 1, 13, 97, 1 for model input mfccs = np.reshape(mfccs, (1, 13, 94, 1))
    shape = mfccs.shape
    # as long as clip is 3 seconds
    mfccs = np.reshape(mfccs, (1, 13, 94, 1))

    # Map model predictions to emotions
    mfccs = ImageGen.standardize(np.copy(mfccs))

    with graph.as_default():
        predictions = a_model.predict(mfccs)[0]
    probabilities = tuple(zip(a_emotions, predictions))

    return probabilities


def predict_emotion_from_face(face_img):
    """
    Runs emotion detection model on an image of a face.

    Params
    ------
    face_img: array
        Cropped image of a face.

    Returns
    -------
    probabilities: array-like
        List of emotions with corresponding probabilities

    """
    # Process the image for model input
    img = _preprocess_image(face_img)

    # Obtain emotion predictions
    with graph.as_default():
        predictions = model.predict(img)[0]
    probabilities = tuple(zip(emotions, predictions))

    return probabilities

def _preprocess_image(img):
    """
    Performs several pre-processing steps to prepare an image for input to the emotion detection model.

    Params
    ------
    img: array
        Cropped image of a face

    Returns
    -------
    img_pixels: array, shape = (1, 48, 48, 1)
        Image in proper format for input to emotion model.
    """
    # Convert image to greyscale if necessary
    gray = np.copy(img)
    if len(gray.shape) > 2:
        if gray.shape[2] == 3:
            gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)

    # Resize to 48x48
    if gray.shape[0] != IMG_INPUT_WIDTH or gray.shape[1] != IMG_INPUT_WIDTH:
        gray = cv2.resize(gray, (IMG_INPUT_WIDTH, IMG_INPUT_WIDTH))

    # Properly shape axes for model input, s.t. shape is (1, 48, 48, 1)
    img_pixels = image.img_to_array(gray)
    img_pixels = np.expand_dims(img_pixels, axis=0)
    img_pixels /= 255

    return img_pixels

def get_faces(img):
    """
    Run face detection over an image and return bounding boxes for all detected faces

    Params
    ------
    img: array

    Returns
    -------
    faces: array
        Contains x, y, w, h values for the bounding box over each face.
    """

    # Convert to grayscale if necessary
    gray = img
    if gray.shape[2] == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)

    # Run face detection
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    return faces

def detect_face_and_annotate_emotions(frame):
    height, width = frame.shape[:2]

    scaling_factor = width / 640
    width_resize, height_resize = int(width // scaling_factor), int(height // scaling_factor)
    resized_frame = cv2.resize(frame, (width_resize, height_resize))

    faces = get_faces(resized_frame)

    # Detect emotions and annotate video
    for (x_res, y_res, w_res, h_res) in faces:
        # Get coordinates of frame in original frame resolution coordinate frame
        x, y, w, h = (int(x_res * width / width_resize), int(y_res * height / height_resize),
                      int(w_res * width / width_resize), int(h_res * height / height_resize))

        # Draw rectangle on original frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop out face
        detected_face = frame[int(y_res):int(y_res + h_res), int(x_res):int(x_res + w_res)]  # Crop face
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # Gray scale
        detected_face = cv2.resize(detected_face, (IMG_INPUT_WIDTH, IMG_INPUT_WIDTH))  # Resize (48x48)

        # Get emotion from face
        if True:
            predictions = predict_emotion_from_face(detected_face)
            prob = max(predictions, key=lambda t: t[1])[1]

            # Only annotate emotion if it's high enough probability
            if prob >= PROBABILITY_THRESH:
                # Annotate emotion label above bounding box
                emotion_name = max(predictions, key=lambda t: t[1])[0]
                cv2.putText(frame, emotion_name, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame

class EmotionsMap:
    def __init__(self, memory=6):
        # [{(xi,yi): ['happy': 0.1'], (xi2, yi2): ['happy': 0.2]}, {}, {}]
        self.emotion_map = {}
        self.memory = memory
        self.frame_counter = 0

    def predict(self, frame):
        height, width = frame.shape[:2]

        scaling_factor = width / 640
        width_resize, height_resize = int(width//scaling_factor), int(height//scaling_factor)
        resized_frame = cv2.resize(frame, (width_resize, height_resize))
        faces = get_faces(resized_frame)
        current_frame_map = {}

        # Detect emotions and annotate video
        for (x_res, y_res, w_res, h_res) in faces:
            # Get coordinates of frame in original frame resolution coordinate frame
            x, y, w, h = (int(x_res * width / width_resize), int(y_res * height / height_resize),
                          int(w_res * width / width_resize), int(h_res * height / height_resize))

            # Draw rectangle on original frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Crop out face
            detected_face = frame[int(y):int(y + h), int(x):int(x + w)]  # Crop face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # Gray scale
            detected_face = cv2.resize(detected_face, (IMG_INPUT_WIDTH, IMG_INPUT_WIDTH))  # Resize (48x48)

            # Get emotion from face
            predictions = predict_emotion_from_face(detected_face)
            current_frame_map[(x, y)] = predictions  # Add predictions to current frame map

            # Store in the emotion map
            self.emotion_map[self.frame_counter] = current_frame_map
            predictions = self._probability_from_memory(x, y)
            prob = max(predictions, key=lambda t: t[1])[1]

            # Only annotate emotion if it's high enough probability
            if prob >= PROBABILITY_THRESH:
                # Annotate emotion label above bounding box
                emotion_name = max(predictions, key=lambda t: t[1])[0]
                cv2.putText(frame, emotion_name, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        self.frame_counter += 1
        return frame

    def _probability_from_memory(self, x, y):
        current_frame = self.frame_counter
        face_coords = (x, y)

        # Remove old frames from the map
        self.emotion_map = dict([(k, v) for (k, v) in self.emotion_map.items() if k > self.frame_counter - self.memory])

        # Get average of existing frames that correspond with faces in most recent frame
        probabilities = dict(self.emotion_map[current_frame][(x, y)])

        for old_frame in self.emotion_map:
            if old_frame != current_frame:
                for old_face in self.emotion_map[old_frame]:
                    # Check distance
                    euc_distance = np.sqrt((face_coords[0] - old_face[0])**2 + (face_coords[1] - old_face[1])**2)

                    # Consider the same face if it meets our euclidean distance threshold
                    if (euc_distance <= EUC_DIST_THRES):
                        # Merge probabilities from the previous face into our probabilities array
                        old_prob = dict(self.emotion_map[old_frame][old_face])
                        probabilities = {k: v * old_prob.get(k) for (k, v) in probabilities.items()}

        normalizing_constant = sum(probabilities.values())
        probabilities = {k: v/normalizing_constant for (k, v) in probabilities.items()}

        return tuple(probabilities.items())

if __name__ == '__main__':
	test_audio = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'audio_files/test.wav')
	output = predict_emotion_from_audio(test_audio)
	print('Audio sample output: {}'.format(output))
