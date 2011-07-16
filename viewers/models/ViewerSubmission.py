from django.db import models

class ViewerSubmission(models.Model):
    sc2_name = models.CharField(max_length=64)
    sc2_charcode = models.CharField(max_length=8)
    submit_time = models.DecimalField(max_digits=17, decimal_places=5)
    
    class Meta:
        app_label = 'viewers'
        
    def __unicode__(self):
        from time import time
        from decimal import Decimal
        time_ago = Decimal(str(time())) - self.submit_time
        return ''.join([str(time_ago), ' seconds ago'])