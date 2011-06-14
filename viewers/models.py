from django.db import models

class Viewer(models.Model):
    jtv_handle = models.CharField(max_length=64)
    sc2_name = models.CharField(max_length=32)
    sc2_charcode = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    
    def __unicode__(self):
        return ''.join([self.jtv_handle, ' - ', self.sc2_name, '.', str(self.sc2_charcode)])
    
class ViewerSubmission(models.Model):
    viewer = models.ForeignKey(Viewer)
    submit_time = models.DecimalField(max_digits=15, decimal_places=3)
    
    def __unicode__(self):
        from time import time
        from decimal import Decimal
        time_ago = Decimal(str(time())) - self.submit_time
        return ''.join([str(time_ago), ' seconds ago'])