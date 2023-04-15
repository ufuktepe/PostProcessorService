from django.db import models


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)
    acc = models.CharField(max_length=255)
    taxon = models.CharField(max_length=1024, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    abundance = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'results'


class Status(models.Model):
    acc = models.CharField(primary_key=True, max_length=255)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    public = models.BooleanField()
    status = models.SmallIntegerField()
    output_path = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'status'
