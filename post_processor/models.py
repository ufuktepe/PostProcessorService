from django.db import models


class Metadata(models.Model):
    acc = models.TextField(primary_key=True)
    assay_type = models.TextField(blank=True, null=True)
    center_name = models.TextField(blank=True, null=True)
    consent = models.TextField(blank=True, null=True)
    experiment = models.TextField(blank=True, null=True)
    sample_name = models.TextField(blank=True, null=True)
    instrument = models.TextField(blank=True, null=True)
    librarylayout = models.TextField(blank=True, null=True)
    libraryselection = models.TextField(blank=True, null=True)
    librarysource = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    sample_acc = models.TextField(blank=True, null=True)
    biosample = models.TextField(blank=True, null=True)
    organism = models.TextField(blank=True, null=True)
    sra_study = models.TextField(blank=True, null=True)
    releasedate = models.DateTimeField(blank=True, null=True)
    bioproject = models.TextField(blank=True, null=True)
    mbytes = models.IntegerField(blank=True, null=True)
    loaddate = models.TextField(blank=True, null=True)
    avgspotlen = models.IntegerField(blank=True, null=True)
    mbases = models.IntegerField(blank=True, null=True)
    library_name = models.TextField(blank=True, null=True)
    biosamplemodel_sam = models.TextField(blank=True, null=True)
    collection_date_sam = models.TextField(blank=True, null=True)
    geo_loc_name_country_calc = models.TextField(blank=True, null=True)
    geo_loc_name_country_continent_calc = models.TextField(blank=True, null=True)
    geo_loc_name_sam = models.TextField(blank=True, null=True)
    ena_first_public_run = models.TextField(blank=True, null=True)
    ena_last_update_run = models.TextField(blank=True, null=True)
    sample_name_sam = models.TextField(blank=True, null=True)
    datastore_filetype = models.TextField(blank=True, null=True)
    jattr = models.TextField(blank=True, null=True)
    race_sam = models.TextField(blank=True, null=True)
    body_site_sam = models.TextField(blank=True, null=True)
    source_name_sam = models.TextField(blank=True, null=True)
    bytes = models.TextField(blank=True, null=True)
    tissue_sam = models.TextField(blank=True, null=True)
    cell_type_sam = models.TextField(blank=True, null=True)
    sex_calc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'


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
