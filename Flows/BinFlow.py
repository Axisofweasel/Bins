import dotenv
import logging
import requests
import os
from prefect import flow

@flow(log_prints=True)
def binflow():
    
    dotenv.load_dotenv()

    logging.basicConfig(
        filename= './app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    api_token = os.getenv('PushoverApiToken')
    user_token = os.getenv('UserToken')
    api_url = os.getenv('ApiUrl')

    formatted_message = 'This is a test of the emergency bin system'

    title = 'Test'
    message = formatted_message
    html = 1

    logging.info(f'{message}')

    message_dict = {
        'token': api_token,
        'user': user_token,
        'title': title,
        'message': message,
        'html': html
    }
    
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
    
    
if __name__ =="__main__":
    #binflow()
    #binflow.serve()
    dotenv.load_dotenv()
    binflow.deploy(
        name = "Binfluencer Bot",
        work_pool_name="my-docker-pool",
        image="binfluencer-bot",
        push = False,
        tags=["Bins", "Chris"],
        job_variables={"env":{
            "BinUrl": os.getenv('BinUrl'),
"PushoverApiToken": os.getenv('PushoverApiToken'),
"UserToken": os.getenv('UserToken'),
"ApiUrl": os.getenv('ApiUrl'),
        }}
    )