from rest_framework import serializers
from .models import Audio


# Serializer to process raw data from front end into backend readable format
class AudioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Audio
		fields = '__all__'
