from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import column_property, relationship, sessionmaker
from sqlalchemy.sql import *

from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days = 1)

engine = create_engine('sqlite:///bernie_job.db')
Base = declarative_base()

"""
category,job_title,page_link,job_id,location,run_date
"""

class Job(Base):
  """
    Job model

    This model holds a record for each job that is posted on the Bernie 2020
    jobs site.
  """
  __tablename__ = 'job'
  job_id = Column(Integer, primary_key = True) # job primary key, so we'll need a separate model for date_jobs
  title = Column(String)
  category = Column(String)
  link = Column(String)
  location = Column(String)
  dates = relationship('JobDate')

class JobDate(Base):
  """
    JobDate model

    This model holds a record for each date that a Job ID was present.
  """
  __tablename__ = 'job_date'
  id = Column(Integer, primary_key = True)
  job_id = Column(Integer, ForeignKey('job.job_id'))
  date = Column(DATE)

def create_db():
  Job.__table__.create(bind = engine, checkfirst = True)
  JobDate.__table__.create(bind = engine, checkfirst = True)