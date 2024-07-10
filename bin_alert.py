import datetime
import dotenv
import logging
import re
import requests
import os
from bs4 import BeautifulSoup


def calendar_check():
    
    logging.basicConfig(
    filename= './app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    )
    
    dotenv.load_dotenv()
    debug = int(os.getenv('DEBUG', '0')) 
    bin_url = os.getenv('BINURL')

    bins ={
    'Your next Blue Bin day': ['Blue Bin','#0000FF'],
    'Your next Green Bin day': ['Green Bin','#008000'],
    'Your next Brown Bin day': ['Brown Bin','#A52A2A'],
    'Your next Purple Bin day': ['Purple Bin','#800080']
    }

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days = 1)
    tomorrowdate = tomorrow.strftime('%Y-%m-%d')

    logging.debug('Getting Bin Calendar')
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

    if debug == 1:
        logging.debug('Setting Debug Message')
        send = True
        formatted_message = 'Debugging Binfluencer Bot'

    return formatted_message, send
    
    
def message_post(formatted_message, send):
    
    api_token = os.getenv('PUSHOVERAPITOKEN')
    user_token = os.getenv('USERTOKEN')
    api_url = os.getenv('APIURL')
    debug = int(os.getenv('DEBUG', '0')) 
    
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
            logging.debug('Sending Message')
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
    return

def bin_flow():
    formatted_message, send = calendar_check()
    message_post(formatted_message, send)
    return

if __name__=="__main__":
    bin_flow()