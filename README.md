# NBA-DATA

This project contains various ETL Pipelines (using Mage.AI) that process/clean various differnt types of NBA Data and upload them to GCS and Google Bigquery, where they can be used to conduct various in-depth analyses on NBA Data.


## How to replicate my project
1. Clone this repository locally
2. Navigate to the project directory and run `docker compose build` (The should come bundled with all necessary dependencies)
3. Once the Docker image is built, run `docker compose up`
4. Update credentials and related global variables, like bucket name, project_id, etc. 

#### NOTE : This was based off of my own GCP account and credentials, in order to use your own account you will need to add your key in the secrets folder, and update pipeline variables like bucket-name and project-id with your own information. 

Below are some example images of analytical dashboards and graphs that I have been able to create using my Data warehouse : 

PLACEHOLDER FOR IMAGES
