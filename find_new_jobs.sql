  select 
    j.*
  from job j 
  join job_date d on j.job_id = d.job_id
  where d.date = (select max(date) from job_date)
  and not exists (select job_id from job_date where date = d.date - 1 and job_id = j.job_id);