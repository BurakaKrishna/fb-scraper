import requests
import pandas as pd

# Inititalization
user_id = "1231231823" 
# Add your user_id
next_pagination_string = "MTQ3MTUwODk1MjoxNDc"
# get next_pagination_string from the url when firing the query in graph api explorer
access_token = 'EAACEdEose0cBACLfI9AbsZCZB1ZANvj1ZA6L4ZCPoZCGrPYHH70Xmo1S2B1gw'
# replace this with access token
url = "https://graph.facebook.com/v2.1/%s/home?access_token=%s&after=%s&debug=all&format=json&method=get&pretty=0&suppress_http_code=1" % (user_id,access_token,next_pagination_string)

fb_status = {}

def make_status_update_dataframe(no_of_times_to_call):
	for i in range(no_of_times_to_call):
		if i == 0:
			fb_data = get_data_from_fb_stream(url)
		data = fb_data.json()['data']
		fb_status = find_status_in_fb_stream_data(data)
		next_url = fb_data.json()['paging']['next']
		fb_data = get_data_from_fb_stream(next_url)
	return pd.DataFrame(fb_status.items())

def find_status_in_fb_stream_data(data):
	for i in range(len(data)):
		try:
			if data[i]['type'] == "status":
				fb_status[data[i]['from']['name']] = data[i]['message']
			fb_status['last_page'] = fb_data.json()['paging']['next']
		except:
			pass

def get_data_from_fb_stream(url):
	fb_data = requests.get(url)
	return fb_data

if __name__ == "__main__":
	make_status_update_dataframe(100)
