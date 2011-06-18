from django.db import models

class ViewerSubmission(models.Model):
    viewer = models.ForeignKey('Viewer')
    submit_time = models.DecimalField(max_digits=15, decimal_places=3)
    
    class Meta:
        app_label = 'viewers'
        
    def __unicode__(self):
        from time import time
        from decimal import Decimal
        time_ago = Decimal(str(time())) - self.submit_time
        return ''.join([str(time_ago), ' seconds ago'])