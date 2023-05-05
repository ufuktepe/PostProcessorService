# Post Processor Service for the Microbiome Analysis Platform
Post Processor service merges Qiime2 results and generates visualizations for feature tables and taxonomy analyses.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Install Qiime2: https://docs.qiime2.org/2023.2/install/

## Usage

1. Add database credentials in config/settings.py
2. Provide file paths for S3_MERGED_RESULTS_PATH and CONDA_PATH in config/settings.py
3. Run the following commands.

```python
source venv/bin/activate  
python3 manage.py runserver 0:8000
```

4. To Qiime2 merge results and generate visualizations send a post request to port 8000. The body of the post request must include json data with the following format:
{
  "run_ids": "SRR18828316 SRR18828317 SRR18828318"
}

