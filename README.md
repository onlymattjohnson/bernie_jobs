# Bernie Jobs Tracker

This is a project that tracks jobs posted by the Bernie 2020 campaign.

## Requirements

* BeautifulSoup
* Pandas

## save_bernie_jobs.py

This is a script that will connect to the Bernie 2020 website and download a csv file of open jobs.

### Fields captured

| Field     | Description                                                      |
| --------- | ---------------------------------------------------------------- |
| category  | The department the job was posted in                             |
| job_title | The text title of the job                                        |
| page_link | The URL for the job posting                                      |
| job_id    | A unique identifier for each job pulled from the slug of the URL |
| location  | A city or state or other geographic location                     |
| run_date  | The date the file was pulled and generated                       |