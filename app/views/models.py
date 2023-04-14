from django.db import models

# Create your models here.


class TrafficReport(models.Model):

    traffic_report_id = models.CharField(max_length=256, primary_key=True)
    published_date = models.DateTimeField(null=False, blank=False)
    issue_reported = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    latitude = models.CharField(max_length=100, blank=False, null=False)
    longitude = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    traffic_report_status = models.CharField(max_length=100, blank=False, null=False)
    traffic_report_status_date_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'traffic_report'