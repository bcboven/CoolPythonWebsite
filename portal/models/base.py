

from datetime import datetime
from django.db import models
from uuidfield import UUIDField

class BaseModel(models.Model):
	""" The Basic Model Everything Extends, gives us some fun methods and properties"""

	created_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	uuid = UUIDField(auto=True)

	class Meta:
		abstract = True
