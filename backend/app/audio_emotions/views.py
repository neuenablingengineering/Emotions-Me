from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions, authentication
from .models import Audio
import sys
import os

# Import emotions stuff - have to modify our system paths a little bit since emotion_proc folder is in parent dir
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(path, "emotion_processing/"))
import emotions_helpers


class AudioView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser,)
    authentication_classes = ()

    def post(self, request, format='wav'):
        my_file = request.FILES['file']
        #audio_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "audio_files/")
        #audio_clip_path = os.path.join(audio_folder_path, "audio.wav")
        audio_folder_path = os.path.dirname(__file__).replace('audio_emotions', 'emotion_processing/audio_files/')
        dst = open(os.path.join(audio_folder_path, my_file.name), 'wb+')
        for chunk in my_file.chunks():
            dst.write(chunk)
            dst.close()
        output = emotions_helpers.predict_emotion_from_audio(my_file.name)
        print(output)
        # if file exists then remove it
        # os.remove the audio file
        #import pdb; pdb.set_trace()
        if os.path.exists(os.path.join(audio_folder_path, my_file.name)):
              os.remove(os.path.join(audio_folder_path, my_file.name))

        return Response(output, status=status.HTTP_200_OK)
