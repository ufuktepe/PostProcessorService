# Post Processor Service for the Microbiome Analysis Platform
Post Processor service merges Qiime2 results and generates visualizations for feature tables and taxonomy analyses.

## Installation

Create an EC2 instance on AWS using the Qiime2 image. Please refer to https://docs.qiime2.org/ for details.

Install Qiime2: https://docs.qiime2.org/2023.2/install/

Pull the Data Engineering submodule
```git submodule update --init --recursive```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Install Redis 
```sudo apt-get install redis-server```

Install Supervisor 
```sudo apt-get install supervisor```

Install nginx 
```sudo apt install nginx```

Create directories for gunicorn
```sudo mkdir -pv /var/{log,run}/gunicorn/```

Change ownership of the folders
```sudo chown -cR qiime2:qiime2 /var/{log,run}/gunicorn/```

Copy the celery.conf file to /etc/supervisor/celery.conf

Create a log folder for celery
```sudo mkdir /var/log/celery```


## Usage

1. Mount your S3 bucket to the EC2 instance.
2. Add database credentials in config/settings.py
3. Provide file paths for S3_MERGED_RESULTS_PATH and CONDA_PATH in config/settings.py
4. Start the redis server using ```sudo systemctl start redis```
5. Start supervisor ```sudo supervisord -c /etc/supervisor/celery.conf```
5. Navigate to the project folder ```cd PostProcessorService/```  
6. Run the following commands.

```python
source venv/bin/activate  
sudo service nginx start
gunicorn -c config/dev.py
```

7. To merge Qiime2 results and generate visualizations send a post request to port 8000. The body of the post request must include json data with the following format:
{
  "run_ids": "SRR18828316 SRR18828317 SRR18828318"
}
