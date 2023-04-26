import os
import shutil

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from config.settings import CONDA_PATH
from config.settings import ENV
from config.settings import S3_MERGED_RESULTS_PATH
from .DataEngineering import results_merger
from .DataEngineering import utils
from .models import Metadata
from .models import Results


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

    # # Unzip feature table qzv file and move the data folder
    # utils.unzip(qzv_table_path, output_dir)
    # move_data_folder(output_dir=output_dir, folder_name='feature_table')
    #
    # # Unzip taxonomy results qzv file and move the data folder
    # utils.unzip(taxonomy_bar_plot_path, output_dir)
    # move_data_folder(output_dir=output_dir, folder_name='taxonomy_results')

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


@shared_task(bind=True)
def create_results_csv(self, run_ids, output_dir):
    """
    Celery task to create a csv file that includes Qiime2 results.
    """
    # Create a progress recorder.
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(5, 100, description=f"Process started.")

    csv_contents = []
    n_runs = len(run_ids)

    # Populate csv contents list
    for i, run_id in enumerate(run_ids):
        progress_recorder.set_progress(int(5 + 85 * (i + 1) / n_runs), 100, description=f"Querying the database.")

        try:
            run_metadata = Metadata.objects.get(pk=run_id)
        except Metadata.DoesNotExist:
            # Skip the run id
            continue

        try:
            run_results = Results.objects.filter(acc=run_id)
        except Results.DoesNotExist:
            # Skip the run id
            continue

        center_name = run_metadata.center_name
        experiment = run_metadata.experiment
        library_layout = run_metadata.librarylayout
        sample_acc = run_metadata.sample_acc
        biosample = run_metadata.biosample
        organism = run_metadata.organism
        sra_study = run_metadata.sra_study
        bioproject = run_metadata.bioproject
        geo_loc_name_country_calc = run_metadata.geo_loc_name_country_calc
        geo_loc_name_country_continent_calc = run_metadata.geo_loc_name_country_continent_calc
        
        for run_result in run_results:
            csv_contents.append(f'{run_result.acc},{run_result.taxon},{run_result.confidence},{run_result.abundance},'
                                f'{center_name},{experiment},{library_layout},{sample_acc},{biosample},{organism},'
                                f'{sra_study},{bioproject},{geo_loc_name_country_calc},'
                                f'{geo_loc_name_country_continent_calc}\n')

    progress_recorder.set_progress(95, 100, description=f"Generating the csv file.")

    # Create the csv file
    results_csv_path = os.path.join(output_dir, 'results.csv')
    with open(results_csv_path, "w") as results:
        results.write('acc,taxon,confidence,abundance,center_name,experiment,library_layout,sample_acc,biosample,'
                      'organism,sra_study,bioproject,geo_loc_name_country_calc,geo_loc_name_country_continent_calc\n')
        results.writelines(csv_contents)

    progress_recorder.set_progress(100, 100, description=f"Process completed.")