from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from .models import Image
from .serializer import ImageSerializer
import json
import numpy as np
import sys
import os

# Import emotions stuff - have to modify our system paths a little bit since emotion_proc folder is in parent dir
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(path, "emotion_processing/"))
import emotions_helpers


class ImageView(APIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    # Front-end can "post" a JSON object with image data and receive emotion response back
    def post(self, request, format=None):
        # Load image serializer
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            # Load image data as a NumPy array with correct datatype s.t. it's compatible with backend processing
            pic = np.array(json.loads(serializer.data['image'])).astype(np.uint8)

            # Obtain probabilities of each emotion from the face
            probabilities = emotions_helpers.predict_emotion_from_face(pic)

            # Return raw probabilities with no processing/filtering (we may want to update this later)
            return Response(probabilities, status=status.HTTP_201_CREATED)

        # Error case
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
