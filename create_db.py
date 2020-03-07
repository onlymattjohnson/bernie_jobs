from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///bernie_job.db')
Base = declarative_base()

"""
category,job_title,page_link,job_id,location,run_date
"""

class Job(Base):
  __tablename__ = 'job'
  job_id = Column(Integer, primary_key = True) # job primary key, so we'll need a separate model for date_jobs
  title = Column(String)
  category = Column(String)
  link = Column(String)
  location = Column(String)
  dates = relationship('JobDate')

class JobDate(Base):
  __tablename__ = 'job_date'
  id = Column(Integer, primary_key = True)
  job_id = Column(Integer, ForeignKey('job.job_id'))
  date = Column(DATE)

Job.__table__.create(bind = engine, checkfirst = True)
JobDate.__table__.create(bind = engine, checkfirst = True)