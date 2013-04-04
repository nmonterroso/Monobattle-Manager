from time import time
from decimal import Decimal

from django.db import models


class ViewerSubmission(models.Model):
	sc2_name = models.CharField(max_length=64)
	sc2_charcode = models.CharField(max_length=8)
	submit_time = models.DecimalField(max_digits=17, decimal_places=5)

	class Meta:
		app_label = 'viewers'

	def get_time_diff(self):
		return Decimal(str(time())) - self.submit_time

	def __unicode__(self):
		return ''.join([str(self.get_time_diff()), ' seconds ago'])