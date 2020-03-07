# Bulk load all the old files from CSV

import csv, glob
from datetime import datetime

from models import *

def load_data(csvf):
  jobs = []
  job_dates = []

  with open(csvf, 'r') as csvfile:
    f = csv.reader(csvfile, delimiter = ',', quotechar='"')
    next(f) # skip header 

    for r in f:
      job_row = {}
      job_row['job_id'] = r[3]
      job_row['title'] = r[1]
      job_row['category'] = r[0]
      job_row['link'] = r[2]
      job_row['location'] = r[4]
      
      job_date_row = {}
      job_date_row['job_id'] = r[3]
      job_date_row['date'] = datetime.strptime(r[5], '%Y-%b-%d')

      jobs.append(job_row)
      job_dates.append(job_date_row)

  Session = sessionmaker(bind = engine)
  session = Session()

  for job in jobs:
    if not session.query(Job).filter(Job.job_id == job['job_id']).first():
      row = Job(**job)
      session.add(row)

  for jd in job_dates:
    if not session.query(JobDate).filter(JobDate.job_id == jd['job_id'], JobDate.date == jd['date']).first():
      row = JobDate(**jd)
      session.add(row)
    else:
      print(f"Job {jd['job_id']} for date {jd['date']} already exists.")

  session.commit()

for csvf in glob.glob('old_data/*.csv'):
  load_data(csvf)
