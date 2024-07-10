# Binfluencer Bot

This project is a Bin Reminder system that checks the bin collection schedule for Glasgow City Council based on their and sends reminders using a messaging service. The project uses Python and Prefect for orchestration and task management.

This is an ongoing bit of work.  Bin_alert.py is the og app that was running on an azure automation account. You can run this as a standalong script using cron or you can use the Prefect Flow within the Flow structure to deploy to a local or remote (Depending on your DOCKER_HOST env variable) docker container with a prefect scheduler.

This has been built and run locally using a PIPENV virtual environment and it hasn't been tested in anything else, so caveat emptor.

BINURL environment variable needs to be set to your personal address using the calendar finder [Glasgow Refuse and Recycling Address Search](https://onlineservices.glasgow.gov.uk/forms/RefuseAndRecyclingWebApplication/AddressSearch.aspx)

Messaging uses the Pushover App and API [Pushover App](https://pushover.net). It's a great tool and super cheap for personal use.


## Features

- Scrapes bin collection schedules from specified GCC bin calendar URL.
- Sends reminders for bin collections on the day of or day before the uplift.
- Sends a Pushover notification with what bin is due out, it's colour and a link to the calendar.
- Supports logging for debugging and monitoring.
- Supports remote Docker deployment
- Supports Prefect deployment and scheduling
- Configurable using environment variables.

## Upcoming Work

-

## Requirements

- Python 3.8+
- Prefect
- BeautifulSoup4
- Requests
- dotenv

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/binfluencer-bot.git
    cd binfluencer-bot
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory and add the following environment variables:**

    ```plaintext
    BINURL=<Your Bin Calendar URL> 
    PUSHOVERAPITOKEN=<Your Pushover API Token>
    USERTOKEN=<Your User Token>
    APIURL=<Your API URL>
    DEBUG=0  # Set to 1 for debugging mode
    ```

## Running the Script

To run the script, use the following command:

```sh
python bin_alert.py
