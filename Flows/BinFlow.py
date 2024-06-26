import datetime
import dotenv
import requests
import re
import os
from bs4 import BeautifulSoup
from prefect import task, flow, get_run_logger, runtime

@task(log_prints=True)
def calendar_check():
    
    logger = get_run_logger()
    logger.info("INFO level logging")
    logger.info("You can see this becausse we're logging DEBUG errors")

    bin_url = os.getenv('BINURL')
    debug = int(os.getenv('DEBUG', '0')) 

    bins ={
            'Your next Blue Bin day': ['Blue Bin','#0000FF'],
            'Your next Green Bin day': ['Green Bin','#008000'],
            'Your next Brown Bin day': ['Brown Bin','#A52A2A'],
            'Your next Purple Bin day': ['Purple Bin','#800080']
            }

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days = 1)
    tomorrowdate = tomorrow.strftime('%Y-%m-%d')
    
    logger.debug('Getting Bin Calendar')
    html = requests.get(url=bin_url)
    sitesoup = BeautifulSoup(html._content, 'html.parser')
    bin_html = sitesoup.find('fieldset')
    child_html = bin_html.findChildren('p')
    address = sitesoup.find(id="Application_AddressForUPRN")
    address = address.text.strip().strip(',')

    logger.debug('Formatting message')
    messagelist = []
    messagelist.append(f'<b>{address}</b>')
    messagelist.append(f'<a href="{bin_url}">Bin Calendar</a>')
    
    send = False
    
    logger.debug('Checking dates for sending')
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
        logger.debug('Setting Debug Message')
        send = True
        formatted_message = 'Debugging Binfluencer Bot'

    return formatted_message, send

@task(log_prints=True)
def message_post(formatted_message, send):
    
    logger = get_run_logger()
    logger.info("INFO level logging")
    logger.info("You can see this becausse we're logging DEBUG errors")

    api_token = os.getenv('PUSHOVERAPITOKEN')
    user_token = os.getenv('USERTOKEN')
    api_url = os.getenv('APIURL')
    
    title = 'Bin Reminder'
    message = formatted_message
    html = 1

    logger.info(f'{message}')

    message_dict = {
        'token': api_token,
        'user': user_token,
        'title': title,
        'message': message,
        'html': html
    }
    
    if send == True:
        try:
            logger.debug('Sending Message')
            x = requests.post(api_url, json=message_dict)
            x.raise_for_status()
            logger.info('POST successful')
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Connection error occurred: {e}')
        except requests.exceptions.Timeout as e:
            logger.error(f'Timeout error occurred: {e}')  
        except requests.exceptions.RequestException as e:
            logger.error(f'An error occurred: {e}')  
    return



@flow(log_prints=True, retries=3, retry_delay_seconds=30)
def binflow():
    
    dotenv.load_dotenv()

    logger = get_run_logger()
    logger.info("INFO level logging")
    logger.info("You can see this becausse we're logging DEBUG errors")
    
    print("My Name is", runtime.flow_run.name)
    print("I'm part of deployment", runtime.deployment.name)
    print("I should have started at", runtime.flow_run.scheduled_start_time)

    formatted_message, send = calendar_check()
    message_post(formatted_message, send)
    
if __name__ =="__main__":
    dotenv.load_dotenv()
    binflow.deploy(
        name = "Binfluencer Bot",
        work_pool_name="my-docker-pool",
        image="binfluencer-bot",
        push = False,
        tags=["Bins", "Chris"],
        job_variables={"env":{
            "BINURL": os.getenv('BINURL'),
            "PUSHOVERAPITOKEN": os.getenv('PUSHOVERAPITOKEN'),
            "USERTOKEN": os.getenv('USERTOKEN'),
            "APIURL": os.getenv('APIURL'),
            "DEBUG": os.getenv('DEBUG'),
        }}
    )