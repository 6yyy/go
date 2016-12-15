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
Subject: test

selenide-web-test.
"""
    message += str(mes)
    smtpObj = smtplib.SMTP('mail.intrice.ru', 25)
    smtpObj.sendmail(sender, receivers, message)
    print("Successfully sent email")

#def get_page(url):
#	return urllib.request.urlopen(url).read().decode("utf-8")

def get_json(url):
	urlPageJson = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
	return urlPageJson

url_env_auto = "http://hudson.connectivegames.com/view/%7Benv-auto%7D/api/json"
url_st = "http://hudson.connectivegames.com/view/st/api/json"
url_st_dev = "http://hudson.connectivegames.com/view/st-dev/api/json"
url_st_web = "http://hudson.connectivegames.com/view/st-web/api/json"
url_mobile_mac = "http://hudson.connectivegames.com/view/%7Bmobile%20+%20mac%7D/api/json"
url_win32_SM = "http://win32builder.intrice.ru:8080/api/json"

url_lib = [url_env_auto,url_st,url_st_dev,url_st_web,url_mobile_mac,url_win32_SM]


def get_error(url_site):
    add_result = str()
    add_result_error = str()
    send_enstable = str()
    send_failure = str()
    error_migration = str()
    json_home_page = get_json(url_site)
    for item in json_home_page["jobs"]:
        if item.get("color") != "disabled":
            build_json = get_json((item.get("url")+"lastBuild/api/json"))
            if build_json["result"] == "UNSTABLE":
                build_json_error = get_json((item.get("url") + "lastBuild/testReport/api/json"))
                add_result_error += item.get("url")+str(build_json["number"])+"\n"
                for item_error in build_json_error["suites"][0]["cases"]:
                    if item_error.get("status") == "REGRESSION":
                        add_result_error +=  item_error.get("name") + "  \n" + "\n"
            elif build_json["result"] == "FAILURE":
                if item.get("url")==("http://hudson.connectivegames.com/job/migration-test-launcher/"):
                    response = requests.get(item.get("url")+str(build_json["number"])+"/console")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a'):
                        job_name = str(link.get('href'))
                        if ("migration-test/") in job_name:
                            error_migration +=("\n"+"Migration-test-error "+"\n"+item.get("url")+str(build_json["number"])+ "\n" + "fails  "+job_name+"\n"+"\n")
                else:
                    add_result += (item.get("url")+str(build_json["number"])+ "\n" +"  " + str(build_json["result"]) +"\n")


    send_enstable += "\n" + add_result_error + "\n"
    send_failure += "\n" + str(add_result) + error_migration+"\n"
    if len(add_result) > 0:
        send_email(send_failure)
        print(send_failure)
    if len(add_result_error) > 0:
        send_email(send_enstable)
        print(send_enstable)

for item in url_lib:
    get_error(item)
