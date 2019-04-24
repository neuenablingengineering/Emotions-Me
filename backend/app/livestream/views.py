from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from .models import Url, ProcessedVideo
from .serializer import UrlSerializer, ProcessedVideoSerializer
from django.core.validators import URLValidator
import os
import sys
import threading
import time

# Import youtube stuff 
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(path, "emotion_processing/"))
import youtube_emotions

class UrlView(APIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


    def create_entry(self, url, min_width=640):
        output = "processed_video_{}.mp4".format(int(time.time()))
        aws_link = "https://s3.us-east-2.amazonaws.com/emotions-and-me-bucket/"
        path = os.path.join(aws_link, output)

        v = ProcessedVideo(original_url=url, processed_video_name=output, saved_path=path)
        v.save()

        return v


    def post(self, request, format=None):
        # Load image serializer
        serializer = UrlSerializer(data=request.data)

        if serializer.is_valid():
            if 'debug' in serializer.data:
                return Response("https://s3.us-east-2.amazonaws.com/emotions-and-me-bucket/script_output.mp4",
                                status=status.HTTP_201_CREATED)

            elif 'url' in serializer.data:
                vid_url = serializer.data['url']
                vid_entry = self.create_entry(vid_url)
                # vid_entry = ProcessedVideo.objects.get(id=vid_id)
                
                processed_video_name = vid_entry.processed_video_name

                thread = threading.Thread(target=youtube_emotions.youtube_emotions_pipeline, args=(vid_url, processed_video_name, vid_entry))
                thread.daemon = True
                thread.start()

                if not bool(path):
                    return Response("Bad URL", status=status.HTTP_400_BAD_REQUEST)

                responseData = {
                    "id": vid_entry.id,
                    "status": vid_entry.status,
                    "original_url": vid_entry.original_url,
                    "saved_path": vid_entry.saved_path
                }
                return Response(responseData, status=status.HTTP_201_CREATED)

        # Error case
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckVideoView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            video_entry  = ProcessedVideo.objects.get(id=request.query_params['id'])
            responseData = {
                "id": request.query_params['id'],
                "status": video_entry.status,
                "original_url": video_entry.original_url,
                "saved_path": video_entry.saved_path
            }
            return Response(responseData, status=status.HTTP_200_OK)
        except:
            responseData = "Error finding video entry with given id"

            return Response(responseData, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

