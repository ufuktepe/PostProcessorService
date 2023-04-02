from django.db import models


class Study(models.Model):
    id = models.TextField(primary_key=True)
    # Metadata
    library_layout = models.CharField(max_length=100)
    # File Paths
    feature_table_path = models.TextField()
    taxonomy_results_path = models.TextField()
