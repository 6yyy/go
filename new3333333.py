import urllib.request
import json
from html.parser import HTMLParser

add_result = []

def get_page(url):
	return urllib.request.urlopen(url).read().decode("utf-8")

def get_json(page):
	urlPageJson = json.loads(page)
	return urlPageJson

url_st_web = "http://hudson.connectivegames.com/view/st-dev/api/json"

home_page = get_page(url_st_web)
json_home_page = get_json(home_page)
for item in json_home_page["jobs"]:
	if item.get("color") != "disabled":
		build_page = get_page(item.get("url")+"lastBuild/api/json")
		build_json = get_json(build_page)
		if build_json["result"] != "SUCCESS":
				add_result += ([build_json["fullDisplayName"] + build_json["result"]])

print(str(add_result))
