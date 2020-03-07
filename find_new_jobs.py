## Task: Find all jobs that are new today
from datetime import date, timedelta
from models import *

Session = sessionmaker(bind = engine)
session = Session()

today = date.today()
yesterday = today - timedelta(days = 1)

# Create a CTE for all jobs up today
jobs_up_today = (
  session.query(Job.job_id).join(JobDate).filter(JobDate.date == today)
).cte('jobs_today')

today_ids = session.query(jobs_up_today.c.job_id).all()
today_ids = [i[0] for i in today_ids]

# Create a CTE for all jobs up yesterday
jobs_up_yesterday = (
  session.query(Job.job_id).join(JobDate).filter(JobDate.date == yesterday)
).cte('jobs_yesterday')

yesterday_ids = session.query(jobs_up_yesterday.c.job_id).all()
yesterday_ids = [i[0] for i in yesterday_ids]

# Select all jobs today that did not exist yesterday
q = session.query(jobs_up_today.c.job_id)\
        .outerjoin(jobs_up_yesterday, jobs_up_today.c.job_id == jobs_up_yesterday.c.job_id)\
        .filter(jobs_up_yesterday.c.job_id == None)
new_jobs_today = [i[0] for i in q.all()]

if new_jobs_today:
  print(f'There were {len(new_jobs_today)} new jobs found for {today}:')
  print('*'*45)

  q = session.query(Job).filter(Job.job_id.in_(new_jobs_today))
  for i in q.all():
    print(f'{i.job_id}: {i.title} in the {i.category} department [{i.location}]')
else:
  print(f'There were 0 new jobs found for {today}.')
  
print('')

# Select all jobs yesterday that no longer exist today
q = session.query(jobs_up_yesterday.c.job_id)\
        .outerjoin(jobs_up_today, jobs_up_yesterday.c.job_id == jobs_up_today.c.job_id)\
        .filter(jobs_up_today.c.job_id == None)

jobs_gone = [i[0] for i in q.all()]

if jobs_gone:
  print(f'There were {len(jobs_gone)} jobs removed on {today}:')
  print('*'*45)
  
  q = session.query(Job).filter(Job.job_id.in_(jobs_gone))
  for i in q.all():
    print(f'{i.job_id}: {i.title} in the {i.category} department [{i.location}]')
else:
  print(f'There were 0 no jobs removed on {today}.')