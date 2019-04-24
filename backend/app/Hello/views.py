from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Greeting
from .serializer import GreetingSerializer
# Create your views here.


class AllTech(APIView):

    queryset = Greeting.objects.all()
    serializer_class = GreetingSerializer

    def get(self, request):
        all_names = []
        for greeting in Greeting.objects.all():
            all_names.append(greeting.get_name())

        return Response(all_names, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GreetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechView(APIView):

    def get(self, request, pk, format=None):
        try:
            greeting = Greeting.objects.get(pk=pk)
            return Response("Hello there, " + greeting.get_name())
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        greeting = Greeting.objects.get(pk=pk)
        greeting.delete()
        return Response(status=status.HTTP_200_OK)
