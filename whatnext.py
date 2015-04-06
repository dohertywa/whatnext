from bottle import route, run,template,debug
import requests
import json
import random
import arrow
import bottle.ext.memcache

app = bottle.Bottle()
plugin = bottle.ext.memcache.MemcachePlugin(servers=['localhost:11211'])
app.install(plugin)

#keyword = 'mc'

RAV_KEY = "Ru_HwXZ_kgbFgq7t4Trh3f6xblkrSQz3pVDjC9Ig"
APP_KEY = "FED0135B342E318AE033"
api_uri = "https://api.ravelry.com"

def api_call(url):
	headers = {'Accept-Encoding':'gzip'}
	req = requests.get(api_uri+url, auth=(APP_KEY,RAV_KEY), headers=headers, verify=False)
	return req.json()

def get_friends(username):
	return api_call('/people/%s/friends/list.json' % username)

def get_queue_projects(username):
	return api_call('/people/%s/queue/list.json?page_size=1000' % username)

def get_project_count(queue):
	return int(queue['paginator']['results']) or 0

def get_random_project(count):
	plist = range(0,count)
	random.shuffle(plist)
	return random.choice(plist)

def calculate_time_in_queue(date_added):
	from datetime import datetime
	today = datetime.today().date()
	added = datetime.strptime(date_added, '%Y-%m-%d').date()
	days = abs((today-added)).days
	years, remainder_days = divmod(days,365)
	months, days_left = divmod(remainder_days, 30)
	tiq = ""
	if years > 0:
		if years == 1:
			tiq += "1 year "
		else:
			tiq += str(years) + " years "
	if months > 0:
		if months == 1:
			tiq += "1 month "
		else:
			tiq += str(months) + " months "
	if days > 0:
		if days == 1:
			tiq += "1 day "
		else:
			tiq += str(days_left) + " days"
	return tiq

def generate_pattern_link(pattern_name):
	return "http://www.ravelry.com/patterns/library/" + str(pattern_name).replace(' ','-').lower()

@app.route('/myqueue/:username')
def display_queue(username,mc):
	project_list = mc.get(username)
	if not project_list:
		mc.set(username, get_queue_projects(username))
		project_list = mc.get(username)
	friends = mc.get('friends_' + username)
	if not friends:
		mc.set('friends_' + username, get_friends(username))
		friends = mc.get('friends_' + username)
	project_count = get_project_count(project_list)
	if project_count is not 0:
		queued_projects = project_list['queued_projects']
		pchoice = get_random_project(project_count)
		project = queued_projects[pchoice]
		date_added = arrow.get(project['created_at'],'YYYY/MM/DD').format('YYYY-MM-DD')
		date_added = calculate_time_in_queue(date_added)
		pattern_link = generate_pattern_link(project['short_pattern_name'])
	return template('myqueue.tpl', friends=friends,date_added=date_added,project=project,username=username,page_count=int(project_list['paginator']['page_count']),number_projects=project_count, pattern_link=pattern_link)

app.debug(True)
app.run(host='localhost', port=9090, server='bjoern', reloader=True)
