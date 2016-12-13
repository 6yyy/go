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



add_result = []
add_result_error = []

def get_page(url):
	return urllib.request.urlopen(url).read().decode("utf-8")

def get_json(page):
	urlPageJson = json.loads(page)
	return urlPageJson

url_st_web = "http://hudson.connectivegames.com/view/st-web/api/json"

home_page = get_page(url_st_web)
json_home_page = get_json(home_page)
for item in json_home_page["jobs"]:
	if item.get("color") != "disabled":
		build_page = get_page(item.get("url")+"lastBuild/api/json")
		build_json = get_json(build_page)
        if build_json["result"] == "UNSTABLE":
            build_page_error = get_page(item.get("url") + "lastBuild/testReport/junit/com.connectivegames.sites.utils/SelenideWebTest/api/json")
            build_json_error = get_json(build_page_error)
            for item_error in build_json_error["child"]:
                add_result_error += item_error.get("name") + "  \n"
		if build_json["result"] != "SUCCESS":
				add_result += ([build_json["fullDisplayName"] + build_json["result"]])
print(add_result)

y += add_result+"\n"+url + job_name + "lastBuild\n" + add_result_error+"\n"

print(y)

#send_email(y)