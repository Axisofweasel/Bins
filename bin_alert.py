import datetime
import logging
import re
import requests
import os
from bs4 import BeautifulSoup



logging.basicConfig(
    filename= './app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

api_token = os.getenv('ApiUrl')
user_token = os.getenv('UserToken')
api_url = os.getenv('ApiUrl')
bin_url = os.getenv('BinUrl')

bins ={
'Your next Blue Bin day': ['Blue Bin','#0000FF'],
'Your next Green Bin day': ['Green Bin','#008000'],
'Your next Brown Bin day': ['Brown Bin','#A52A2A'],
'Your next Purple Bin day': ['Purple Bin','#800080']
}

today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days = 1)
tomorrowdate = tomorrow.strftime('%Y-%m-%d')
#testdate = datetime.datetime.strptime('2024-05-19', '%Y-%m-%d')


html = requests.get(url=bin_url)
sitesoup = BeautifulSoup(html._content, 'html.parser')
bin_html = sitesoup.find('fieldset')
child_html = bin_html.findChildren('p')
address = sitesoup.find(id="Application_AddressForUPRN")
address = address.text.strip().strip(',')

messagelist = []
messagelist.append(f'<b>{address}</b>')
messagelist.append(f'<a href="{bin_url}">Bin Calendar</a>')

send = False

for c in child_html:
    x = re.split('\\.', c.text.strip())
    y = re.split(' is ', x[0])
    if 'Today' in x[0]:
        messagelist.append(f'<font color={bins[y[0]][1]}>Today: {bins[y[0]][0]}</font>')
        send = True
    else:
        if 'Tomorrow' in y[1]: 
            send = True
            messagelist.append(f'<font color={bins[y[0]][1]}>Tomorrow: {bins[y[0]][0]}</font>')

formatted_message = '\n'.join(messagelist)


title = 'Bin Reminder'
message = formatted_message
html = 1

logging.info(f'{message}')

message_dict = {
    'token': api_token,
    'user': user_token,
    'title': title,
    'message': message,
    'html':html
}

if send == True:
    try:
        x = requests.post(api_url, json=message_dict)
        x.raise_for_status()
        logging.info('POST successful')
    except requests.exceptions.HTTPError as e:
        logging.error(f'HTTP error occurred: {e}')
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Connection error occurred: {e}')
    except requests.exceptions.Timeout as e:
        logging.error(f'Timeout error occurred: {e}')  # Fixed here
    except requests.exceptions.RequestException as e:
        logging.error(f'An error occurred: {e}')  # Fixed here