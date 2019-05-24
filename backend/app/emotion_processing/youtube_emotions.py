import pafy
import cv2
import datetime
from multiprocessing.pool import ThreadPool
from collections import deque
import subprocess as sp
from subprocess import Popen, PIPE
import os
import emotions_helpers
import glob
import time
import distutils.spawn

# Check if on AWS
ON_AWS = True # TODO: update this somehow (before: if 'AWS_PATH' in os.environ else False][0])


def download_video(vid_url, min_width):
    # Setup pafy object
    ydl_opts = {"--no-check-certificate": True}
    pafy_vid = pafy.new(vid_url, ydl_opts)

    # Choose the min res. stream that meets our min_width, or the max res. if all avail streams are smaller than min
    mp4_streams = [vstream for vstream in pafy_vid.streams if vstream.extension == 'mp4']  # Rest of script needs mp4
    desired_streams = [vstream for vstream in mp4_streams if int(vstream.resolution.split('x')[0]) >= min_width]
    stream = [desired_streams[0] if desired_streams else mp4_streams[-1]][0]

    # Download file
    download_path = "original_{}.{}".format(int(time.time()), stream.extension)
    stream.download(filepath=download_path, quiet=True)

    return download_path


def get_frames(cap, command):
    # Setup multiprocessing
    threadn = cv2.getNumberOfCPUs()*50
    pool = ThreadPool(processes=threadn)
    pending = deque()
    proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

    frame_counter = 0

    # Loop through video
    while True:
        while len(pending) > 0 and pending[0].ready():
            res = pending.popleft().get()
            proc.stdin.write(res.tostring())

        # Read more frames if there are open spots in the queue
        if len(pending) < threadn:
            ret, frame = cap.read()
            frame_counter += 1

            # Break at end of file
            if not ret:
                break

            if frame_counter % 1000 == 0:
                print("Frame: {}".format(frame_counter))

            cv2.waitKey(1)

            # Add task to process this new frame to the pool
            task = pool.apply_async(emotions_helpers.detect_face_and_annotate_emotions, (frame.copy(),))
            pending.append(task)

    # Close out when done writing the video
    cap.release()
    proc.stdin.close()
    proc.stderr.close()


def process_video(input_path, output_path):
    # Open video file
    cap = cv2.VideoCapture()
    cap.open(input_path)

    # Get stats from video for ffmpeg command
    height, width, fps = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          str(cap.get(cv2.CAP_PROP_FPS)))
    dimensions = "{}x{}".format(width, height)

    # Create ffmpeg console command
    pix_fmt = 'bgr24'  # OpenCV uses bgr
    ffmpeg_cmd = ['ffmpeg',
                  '-y',                     # Overwrites output file if it exists
                  '-f', 'rawvideo',         # Specify input format as raw video
                  '-s', dimensions,         # Specify video dimensions
                  '-pix_fmt', pix_fmt,      # Specify video pixel format
                  '-r', fps,                # Frame rate
                  '-i', '-',                # Establishes the stdin as input for opencv frame pipe
                  '-i', input_path,         # Add the original video as an input since we need it's audio
                  '-map', '0:0',            # Take frames from the opencv pipe
                  '-map', '1:1',            # Take audio from the original video
                  '-c:v', 'mpeg4',          # Video encoder
                  '-preset', 'ultrafast',   # Fast encoding at expensive of higher filesize
                  '-b:v', '4000K',          # Video bitrate
                  '-shortest',              # Match shorter of audio or video streams to be safe
                  output_path]

    # Call function to pipe and process frames from video to ffmpeg
    get_frames(cap, ffmpeg_cmd)


def process_video_singlethreaded(input_path, output_path):
    # Open video
    cap = cv2.VideoCapture()
    cap.open(input_path)

    # Get stats from video for VideoWriter
    height, width, fps = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          cap.get(cv2.CAP_PROP_FPS))

    temp_output = "temp_vid.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))
    emotions_map = emotions_helpers.EmotionsMap()

    frame_counter = 0

    # Read, process, and write frames to temporary vidoe file
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if ret:
            processed = emotions_map.predict(frame)
            # processed = emotions_helpers.detect_face_and_annotate_emotions(frame)
            out.write(processed)
            cv2.waitKey(1)

            frame_counter += 1
            if frame_counter % 1000 == 0:
                print("Frame: {}".format(frame_counter))

    cap.release()
    out.release()

    # Merge video and audio in ffmpeg
    ffmpeg_cmd = ['ffmpeg -y -i {} -i {} -c:v libx264 -map 0:0 -map 1:1 {} -preset ultrafast'.format(
        temp_output, input_path, output_path)]
    sp.call(ffmpeg_cmd, shell=True)
    os.remove(temp_output)


def check_aws_env():
    # Check if bucket is mounted already
    bucket_check_cmd = 'ps -ef | grep s3fs'
    bucket_check_output = str(Popen([bucket_check_cmd], shell=True, stdout=PIPE).communicate()[0])
    if 'bucket' in bucket_check_output:
        bucket_directory = bucket_check_output.split('emotions-and-me-bucket ')[1].split(' -o passwd_file')[0]
        return os.path.join(os.path.expanduser('~'), bucket_directory)

    # Check S3FS dependencies for mounting the bucket
    s3fs = bool(distutils.spawn.find_executable('s3fs'))
    if not s3fs:
        print("*** S3FS IS NOT INSTALLED. SEE https://github.com/s3fs-fuse/s3fs-fuse ***")

    password_file = os.path.isfile(os.path.join(os.path.expanduser('~'), '.passwd-s3fs'))
    if not password_file:
        print("*** NO PASSWORD FILE FOR S3FS. SEE https://github.com/s3fs-fuse/s3fs-fuse ***")

    if not (s3fs and password_file):
        exit(0)

    # Mount bucket if not mounted
    bucket_directory = os.path.join(os.path.expanduser("~"), "bucket")
    mount_command = 's3fs emotions-and-me-bucket {0} -o passwd_file={1}/.passwd-s3fs'.format(
        bucket_directory, os.path.join(os.path.expanduser('~')))
    ret = sp.call([mount_command])

    if ret == 1:
        print("*** ERROR MOUNTING BUCKET ***")
        exit(0)

    return bucket_directory

def youtube_emotions_pipeline(url, processed_video_name, video_entry, min_width=640):
    # Check if ffmpeg is installed
    if not bool(distutils.spawn.find_executable('ffmpeg')):
        print("*** FFMPEG NOT INSTALLED. SEE https://www.ffmpeg.org/download.html ***")
        exit(0)

    # Check AWS for bucket mount point and retrieve the bucket directory
    # bucket_dir = ''
    # if ON_AWS:
    #     bucket_dir = check_aws_env()

    # Download sample video
    try:
        original_video = download_video(url, min_width=min_width)
    except:
        # If download fails, return an error
        setattr(video_entry, "status", 'FAILED')
        video_entry.save()
        return False

    # Process the video
    start = datetime.datetime.now()
    process_video_singlethreaded(original_video, processed_video_name)  # process_video(original_video, output)
    stop = datetime.datetime.now()
    print("Total Time: {}".format(stop - start))

    # Delete original videos
    [os.remove(video_file) for video_file in glob.glob("original*.mp4")]

    # Move to bucket
    if ON_AWS:
        # move_command = 'mv {} {}'.format(output, os.path.join(bucket_dir), output)
        move_command = 'aws s3 cp {} s3://emotions-and-me-bucket/ --acl public-read'.format(processed_video_name)
        sp.call([move_command], shell=True)

        aws_link = "https://s3.amazonaws.com/emotions-and-me-bucket/"
        
        setattr(video_entry, "status", 'SUCCEEDED')
        video_entry.save()

        return os.path.join(aws_link, processed_video_name)

    # Return generic path if not on AWS
    else:
        setattr(video_entry, "status", 'FAILED')
        video_entry.save()

        return processed_video_name


if __name__ == '__main__':
    # Retrieve and process sample video
    stars = 'https://www.youtube.com/watch?v=7CVtTOpgSyY'
    # brady = 'https://www.youtube.com/watch?v=v584xpFFis4'
    # kid = 'https://www.youtube.com/watch?v=aIYBZIM10DA'
    youtube_emotions_pipeline(url=stars) 
