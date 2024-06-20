FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

# Install Python, pip, and cron
RUN apt-get update && apt-get install -y python3.9 python3.9-venv python3-pip cron

WORKDIR /app
COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt

COPY bin_alert.py .
RUN chmod +x /app/bin_alert.py
#RUN pip install --no-cache-dir -r requirements.txt
RUN (crontab -l 2>/dev/null; echo "0 6 * * * python3.9 /app/bin_alert.py") | crontab -

CMD ["cron","-f"]
#CMD ["python3.9", "bin_alert.py"]