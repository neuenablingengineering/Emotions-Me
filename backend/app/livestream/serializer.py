from rest_framework import serializers
from .models import Url, ProcessedVideo


# Serializer to process url 
class UrlSerializer(serializers.ModelSerializer):
	class Meta:
		model = Url
		fields = '__all__'

class ProcessedVideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProcessedVideo
		fields = '__all__'