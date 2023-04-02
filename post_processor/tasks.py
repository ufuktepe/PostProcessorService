import os

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from config.settings import ENV
from config.settings import S3_PATH
from .DataEngineering import results_merger
from .DataEngineering import utils


@shared_task(bind=True)
def merge_results(self, feature_table_paths, taxonomy_results_paths):
    """
    Celery task to merge the results.
    """
    output_dir = os.path.join(S3_PATH, self.request.id)
    utils.create_dir(output_dir)

    # Create a progress recorder.
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(5, 100, description=f"Process started.")

    # Path for the merged feature table qza file.
    qza_table_path = os.path.join(output_dir, 'merged_feature_tables.qza')

    # Path for the merged feature table qzv file.
    qzv_table_path = os.path.join(output_dir, 'merged_feature_tables.qzv')

    # Path for the merged taxonomy results qza file.
    qza_taxonomy_path = os.path.join(output_dir, 'merged_taxonomy_results.qza')

    # Path for the merged taxonomy bar plot.
    taxonomy_bar_plot_path = os.path.join(output_dir, 'taxonomy_bar_plot.qzv')

    progress_recorder.set_progress(20, 100, description=f"Merging feature tables...")
    results_merger.merge_feature_tables(feature_table_paths, qza_table_path, ENV)

    progress_recorder.set_progress(40, 100, description=f"Generating feature table visualizations...")
    results_merger.convert_feature_table(qza_table_path, qzv_table_path, ENV)

    progress_recorder.set_progress(60, 100, description=f"Merging taxonomy analysis results...")
    results_merger.merge_taxonomy_results(taxonomy_results_paths, qza_taxonomy_path, ENV)

    progress_recorder.set_progress(80, 100, description=f"Generating taxonomy analysis visualizations...")
    results_merger.generate_taxonomy_bar_chart(qza_table_path, qza_taxonomy_path, taxonomy_bar_plot_path, ENV)

    progress_recorder.set_progress(100, 100, description=f"Process completed.")
