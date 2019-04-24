from rest_framework import serializers
from .models import Image


# Serializer to process raw data from front end into backend readable format
class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = '__all__'
