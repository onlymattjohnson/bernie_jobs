## Task: Find all jobs that are new today
from datetime import date, timedelta
from models import *

Session = sessionmaker(bind = engine)
session = Session()

today = date.today()
yesterday = today - timedelta(days = 1)

# Create a CTE for all jobs up today
jobs_up_today = (
  session.query(Job.job_id
  )
  .filter(JobDate.date == today)
).cte('jobs_today')

# Create a CTE for all jobs up yesterday
jobs_up_yesterday = (
  session.query(Job.job_id
  )
  .filter(JobDate.date == yesterday)
).cte('jobs_yesterday')

# Left join jobs today with jobs yesterday
j = join(
      jobs_up_today, jobs_up_yesterday, 
      jobs_up_today.c.job_id == jobs_up_yesterday.c.job_id,
      isouter = True)

# s = select([jobs_up_today]).select_from(j).where(jobs_up_yesterday.c.job_id == None)

# @TODO Select all jobs today that did not exist yesterday

# @TODO Select all jobs yesterday that no longer exist today