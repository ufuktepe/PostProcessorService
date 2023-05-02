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
    attributes = models.TextField(blank=True, null=True)
    jattr = models.TextField(blank=True, null=True)
    description_sam = models.TextField(blank=True, null=True)
    treatment_sam = models.TextField(blank=True, null=True)
    sample_type_sam = models.TextField(blank=True, null=True)
    isolation_source_sam = models.TextField(blank=True, null=True)
    health_state_sam = models.TextField(blank=True, null=True)
    genotype_sam = models.TextField(blank=True, null=True)
    disease_stage_sam = models.TextField(blank=True, null=True)
    disease_sam = models.TextField(blank=True, null=True)
    cell_type_sam = models.TextField(blank=True, null=True)
    birth_location_sam = models.TextField(blank=True, null=True)
    tissue_sam = models.TextField(blank=True, null=True)
    dev_stage_sam = models.TextField(blank=True, null=True)
    age_sam = models.TextField(blank=True, null=True)
    ecotype_sam = models.TextField(blank=True, null=True)
    cultivar_sam = models.TextField(blank=True, null=True)
    breed_sam = models.TextField(blank=True, null=True)
    strain_sam = models.TextField(blank=True, null=True)
    isolate_sam = models.TextField(blank=True, null=True)
    race_ethnicity = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

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
    email = models.CharField(max_length=255, blank=True, null=True)
    email_notification = models.BooleanField()
    public = models.BooleanField()
    status = models.SmallIntegerField()
    output_path = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'status'
