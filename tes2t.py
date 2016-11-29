import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import smtplib


def send_email(mes):
    sender = 'polozov@intrice.ru'
    receivers = ['polozov@intrice.ru']
    message = """From: From Person <polozov@intrice.ru>
To: To Person <polozov@intrice.ru>
Subject: selenide-web-test

selenide-web-test.
"""
    message += str(mes)
    smtpObj = smtplib.SMTP('mail.intrice.ru', 25)
    smtpObj.sendmail(sender, receivers, message)
    print("Successfully sent email")

x = str('')
y = str()
url = 'http://hudson.connectivegames.com/view/st-web/'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
test_add = []
test_add2 = str()
for link in soup.find_all('a'):
    job_name = str(link.get('href'))
    #print(job_name)
    if ("job") in job_name:
        if not ("last") in job_name:
           if job_name[0]!="/":
               url2 = str(url + job_name + "lastBuild/api/json")
               #print(url2)
               x = urllib.request.urlopen(url2).read().decode("utf-8")
               buildStatusJson = json.loads(x)
               if buildStatusJson["result"] == "UNSTABLE":
                   url3 = str(url + job_name + "lastBuild/testReport/junit/com.connectivegames.sites.utils/SelenideWebTest/api/json")
                   x2 = urllib.request.urlopen(url3).read().decode("utf-8")
                   # print(" build status: " + buildStatusJson["result"])
                   testjson = json.loads(x2)
                   for item3 in testjson["child"]:
                       test_add2 += item3.get("name")+"  \n"
                   test_add = ([buildStatusJson["fullDisplayName"] + buildStatusJson["result"]])

                   y += str(test_add)+"\n"+url + job_name + "lastBuild\n" + test_add2+"\n"
print(y)

send_email(y)