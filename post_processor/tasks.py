import os
import shutil

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from config.settings import CONDA_PATH
from config.settings import ENV
from config.settings import S3_MERGED_RESULTS_PATH
from .DataEngineering import results_merger
from .DataEngineering import utils


@shared_task(bind=True)
def merge_results(self, feature_table_paths, taxonomy_results_paths, timestamp):
    """
    Celery task to merge the results.
    """
    output_dir = os.path.join(S3_MERGED_RESULTS_PATH, timestamp + '-' + self.request.id)
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
    try:
        results_merger.merge_feature_tables(feature_table_paths, qza_table_path, CONDA_PATH, ENV)
    except ValueError:
        utils.create_txt(file_path=os.path.join(output_dir, 'error.txt'),
                         contents='Error in merging feature tables.')
        return

    progress_recorder.set_progress(40, 100, description=f"Generating feature table visualizations...")
    try:
        results_merger.convert_feature_table(qza_table_path, qzv_table_path, CONDA_PATH, ENV)
    except ValueError as e:
        utils.create_txt(file_path=os.path.join(output_dir, 'error.txt'),
                         contents=f'Error in generating feature table visualizations.\n{str(e)}')
        return

    progress_recorder.set_progress(60, 100, description=f"Merging taxonomy analysis results...")
    try:
        results_merger.merge_taxonomy_results(taxonomy_results_paths, qza_taxonomy_path, CONDA_PATH, ENV)
    except ValueError:
        utils.create_txt(file_path=os.path.join(output_dir, 'error.txt'),
                         contents='Error in merging taxonomy analysis results.')
        return

    progress_recorder.set_progress(80, 100, description=f"Generating taxonomy analysis visualizations...")
    try:
        results_merger.generate_taxonomy_bar_chart(qza_table_path, qza_taxonomy_path, taxonomy_bar_plot_path, CONDA_PATH, ENV)
    except ValueError:
        utils.create_txt(file_path=os.path.join(output_dir, 'error.txt'),
                         contents='Error in generating taxonomy analysis visualizations.')
        return

    # Unzip feature table qzv file and move the data folder
    utils.unzip(qzv_table_path, output_dir)
    move_data_folder(output_dir=output_dir, folder_name='feature_table')

    # Unzip taxonomy results qzv file and move the data folder
    utils.unzip(taxonomy_bar_plot_path, output_dir)
    move_data_folder(output_dir=output_dir, folder_name='taxonomy_results')

    progress_recorder.set_progress(100, 100, description=f"Process completed.")


def move_data_folder(output_dir, folder_name):
    """
    Find the data folder, move it to the output directory and rename it to the given folder name.
    """
    done = False
    for root, sub_dirs, file_names in os.walk(output_dir):
        if done:
            break
        for sub_dir in sub_dirs:
            if sub_dir == 'data':
                shutil.move(os.path.join(root, sub_dir), os.path.join(output_dir, folder_name))
                done = True
                break
