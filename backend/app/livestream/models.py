from django.db import models


# Create your models here.
class Url(models.Model):
	url = models.TextField(blank=True)
	debug = models.TextField(blank=True)

class ProcessedVideo(models.Model):
	STATUS_CHOICES = (
		("FAILED", "FAILED"),
		("SUCCEEDED", "SUCCEEDED"),
		("PENDING", "PENDING"),
	)

	id = models.AutoField(primary_key=True)
	processed_video_name = models.TextField(blank=True)
	original_url = models.TextField(blank=True)
	saved_path = models.TextField(blank=True)
	status = models.CharField(
		choices=STATUS_CHOICES,
		default="PENDING",
		max_length=8
	)
