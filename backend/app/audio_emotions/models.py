from django.db import models


# Audio model
class Audio(models.Model):
	# One field for image, this is created as a textfield but will end up being parsed as a JSON object through
	# the function json.loads(serializer.data['image'])
	audio = models.TextField()
