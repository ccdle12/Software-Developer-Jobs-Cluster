import urllib
import json
import sqlite3
from bs4 import BeautifulSoup
import time

page = 1
jobCount = 0

conn = sqlite3.connect('SoftwareJobs.sqlite3')
cur = conn.cursor()
raw_input("****************READ ME******************\nTo select 'YES' press <enter> / to select 'NO' enter 'n'\nContinue...")


while True:
    try:
        # userInput = raw_input("Do you want to scrape page {}?: ".format(page))
        # print "This is the Current Page: ", currentPage
        userInput = raw_input("How many pages do you want to scrape?: ")

        if userInput.lower() == "n":
            print "Exiting Program..."
            break

        userInput = int(userInput)

        while userInput > 0:

            sourceCode = urllib.urlopen("http://www.reed.co.uk/jobs?cached=True&pageno="+str(page)+"&keywords=Software+Developer&pagesize=100").read()

            soup = BeautifulSoup(sourceCode, 'html.parser')
            article = soup('article')

            reedPageCounter = soup('div')

            ##### Show the number of jobs left to scrape #####
            for eachLink in reedPageCounter:
                if '<div class="page-counter" data-bind="text: pagedResultsCount">' in str(eachLink):
                    currentPage = str(eachLink).split('pagedResultsCount">')[1].split('</div>')[0].strip()

            ##### END Show the number of jobs left to scrape #####

            for eachJob in article:

                job = str(eachJob).split('itemprop="title" title=')

                if len(job) <= 1:
                    continue

                # if jobCount < len(article):
                try:
                    # print "-----------------------------------------------------------"
                    jobTitle = job[1].split('">')[0].split("</a>")[0].split('"')[1]
                    jobTitle = unicode(jobTitle, 'utf-8')
                    # print jobTitle

                    jobLocation = str(eachJob).split('<li class="location">')[1].split("</li>")[0]
                    jobLocation = unicode(jobLocation, 'utf-8')
                    # print jobLocation

                    jobSalary = str(eachJob).split('<li class="salary">')[1].split('</li>')[0]
                    jobSalary = unicode(jobSalary, 'utf-8')
                    # print jobSalary

                    jobType = str(eachJob).split('<li class="time">')[1].split("</li>")[0]
                    jobType = unicode(jobType, 'utf-8')
                    # print jobType

                    jobApplicants = str(eachJob).split('<li class="applications">')[1].split('</li>')[0]
                    jobApplicants = unicode(jobApplicants, 'utf-8')
                    # print jobApplicants

                    jobRecruiter = str(eachJob).split("<a href=")[1].split("title=")[1].split(">")[0].split('"')[1]
                    jobRecruiter = unicode(jobRecruiter, 'utf-8')
                    # print jobRecruiter
                    # print "-----------------------------------------------------------"
                    jobCount += 1

                    cur.execute('''INSERT INTO Reed (title, location, salary, jobType, applicants, recruiter)
                                VALUES(?,?,?,?,?,?)''', (jobTitle, jobLocation, jobSalary, jobType, jobApplicants, jobRecruiter))

                    if jobCount % 50 == 0:
                        conn.commit()
                    # print "Current jobCount: ", jobCount

                except:
                    print "------------------------------------------------------------"
                    print "This is the page count: ", page
                    print "This is the job count on this page: ", jobCount
                    print "This is the Current Page: ", currentPage
                    print "------------------------------------------------------------"
                    page += 1
                    time.sleep(1)
                    userInput -= 1


        # else:
        #     print "Exiting program..."
        #     break

    except Exception, e:
        print str(e)
