from django.db import models

# Create your models here.


class Greeting(models.Model):
    name = models.CharField(max_length=50)

    def get_name(self):
        return self.name

