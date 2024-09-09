import creds
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user_email = input("Enter your email: ")

TIMES_JOB = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=%22Graduate+Trainee%22&txtKeywords=Developer%2C%22Graduate+Trainee%22&txtLocation=India&cboWorkExp1=0'

html_text = requests.get(TIMES_JOB).text
soup = BeautifulSoup(html_text, 'html.parser')
jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")


def fetch_jobs():
    job_list = []

    for job in jobs:
        published_date = job.find("span", class_= "sim-posted").text
        company_name = job.find("h3", class_="joblist-comp-name").text.strip('\n     (More Jobs)')
        role = job.find("h2").text.strip()
        job_posting = {}
        if 'few' in published_date:
            job_posting['company_name'] = company_name
            job_posting['skills'] = job.find("span", class_="srp-skills").text.strip()
            job_posting['job_role'] = role
            job_posting['link'] = job.header.h2.a["href"]
            job_list.append(job_posting)

    return job_list


def send_email(job_list, recipient_email):
    sender_email = creds.mail
    sender_password = creds.password

    subject = "Your Personalized Job Openings"
    body = "Here are the latest job listings:\n\n"

    for job in job_list:
        body += f"ROLE: {job['job_role']}\n\n"
        body += f"COMPANY: {job['company_name']}\n\n"
        body += f"SKILLS REQUIRED: {job['skills']}\n\n"
        body += f"LINK: {job['link']}\n\n\n"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.outlook.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


def job_scraper():
    fresher_jobs = fetch_jobs()
    if fresher_jobs:
        send_email(fresher_jobs, user_email)


job_scraper()
print("Email send successfully. Check your Inbox!")

