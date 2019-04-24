from django.db import models


# Image model
class Image(models.Model):
	# One field for image, this is created as a textfield but will end up being parsed as a JSON object through
	# the function json.loads(serializer.data['image'])
	image = models.TextField(blank=True)
