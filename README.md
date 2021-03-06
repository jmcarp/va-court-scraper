# Virginia Court Scraper

This tool is designed to collect court case information published on [Virginia's district and circuit court case information websites](http://www.courts.state.va.us/caseinfo/). Data collected by the scraper can be downloaded at [VirginiaCourtData.org](http://virginiacourtdata.org).

## How to run the scraper

### Environment

I'll be using AWS, but that's not a requirement.

1. Create an EC2 instance. You'll need something than can run Google Chrome, so I'm using Windows
1. Create an RDS PostrgreSQL instance
1. Make sure your security groups allow your server to connect to the database
1. Connect to the server using RDP
1. Install Google Chrome, git, and Python 2.7
1. Install [pyscopg2](http://www.stickpeople.com/projects/python/win-psycopg/)
1. Clone this repository

        git clone https://github.com/bschoenfeld/va-court-scraper.git

1. Download [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) to the root of the repo directory
1. Create a virtual environment in the root of the repo directory. Again, I'm using powershell on windows. The commands will be a bit different for activating the virtual environment and setting the environment variables

        pip install virtualenv
        virtualenv venv
        .\venv\Scripts\activate.ps1

1. Install dependencies

        pip install selenium mechanize beautifulsoup4 psycopg2 SQLAlchemy GeoAlchemy2 pgcli

1. Connect to the database and add the postgis extension

        pgcli postgres://<PGUSER>:<PGPASSWORD>@<PGHOST>:<PGPORT>/<PGDATABASE>
        CREATE EXTENSION postgis;
        \q

1. Set environment variables

        $env:POSTGRES_DB="<PGUSER>:<PGPASSWORD>@<PGHOST>:<PGPORT>/<PGDATABASE>"

### Initalize database with list of courts

Running this script will open a chrome window for the district court website. Click the Accept button and solve the captcha. The script will continue automatically once you do. 

        python load_courts_to_db.py

### Create tasks

First, create data collection tasks. Tasks are made up of a locality, court level, case type, and date range. Run this script to create tasks. The parameters are ending date, starting date, court level (district or circuit), case type (civil or criminal), and optionally, court fips. If court fips is left out, a task will be created for every court.

        python court_bulk_task_creator.py 6/6/2017 6/5/2017 district criminal

### Collect cases

Now you can create collectors. When a collector runs, it will take a task and start collecting data. You must specify the court level (district or circuit) as a parameter. You can run mulitple collectors at once, but in my experience, the website becomes unstable when running more than 10 collectors in parallel.

        python court_bulk_collector.py district

_Warning - This task system that I've created is pretty terrible and uncompleted tasks can easily be lost. I'd love to replace it with a more robust tool, but I haven't gotten around to it yet. Sorry_

## How to run the export

The export script exports data from Postgres to CSV files. The data are exported first by court type and year of most recent hearing, and then by person id. The script uses the psql subprocess to run the copy command to download large chunks of data to the local machine. Then the script breaks the CSVs up so that no file has more than 250,000 cases. Finally, the CSVs are zipped up and pushed to an AWS S3 bucket. Once the script has uploaded all the zip files, it generates a bunch of metadata about the files (number of cases, file size, S3 path) and pushes that metadata to a Firebase database.

Be sure to connect to the database using psql and vacuum it before and after the export.

```
VACUUM (VERBOSE, ANALYZE);
```

Start an Amazon Linux EC2 instance. SSH and run the following commands.

```
sudo yum update
sudo yum -y install gcc gcc-c++ make
sudo yum -y install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
sudo yum -y install git
git clone https://github.com/bschoenfeld/va-court-scraper.git
cd va-court-scraper
virtualenv venv
source venv/bin/activate
pip install selenium mechanize beautifulsoup4 psycopg2 SQLAlchemy GeoAlchemy2 pgcli boto3 awscli python-firebase
export FIREBASE_TOKEN='<FIREBASETOKEN>'
export PGHOST='<PGHOST>'
export PGDATABASE='<PGDATABASE>'
export PGUSER='<PGUSER>'
export PGPASSWORD='<PGPASSWORD>'
export POSTGRES_DB='<PGUSER>:<PGPASSWORD>@<PGHOST>:<PGPORT>/<PGDATABASE>'
```

Run `psql` to make sure you can connect to the instance. Type `\q` to disconnect.  
Run `aws configure` to set up your connection to AWS. Confirm everthing is setup by running `aws s3 ls`.  
Run the script  

```
nohup python court_bulk_exporter.py >> export.out 2>&1 &
```
