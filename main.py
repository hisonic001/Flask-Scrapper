from flask import Flask, render_template, request, redirect
from saram import get_jobs as saram_job
from indeed import get_jobs as indeed_job

app = Flask("JobScrapper")

db={}

@app.route("/")
def home():
  return render_template("main.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  existingJobs=db.get(word)
  if existingJobs:
    jobs=existingJobs
  if word:
    word=word.lower()
    fromDb=db.get(word)
    if fromDb:
      jobs=fromDb
    else:
      jobs=saram_job(word)+indeed_job(word)
      jobs = sorted(jobs, key=(lambda x: x['title']))
      db[word]=jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    word=word,
    resultNumber=len(jobs),
    jobs=jobs)

app.run(host="0.0.0.0")