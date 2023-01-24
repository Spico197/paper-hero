FROM python:3.10-slim

#Install cron and git
RUN apt-get update
RUN apt-get -y install cron git

# prepare scripts
WORKDIR /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./scripts/ /app/scripts/
RUN bash scripts/get_aclanthology.sh
COPY ./src/ /app/src/
COPY ./index.html /app/index.html
COPY ./server.py /app/server.py

# Add the cron job
RUN crontab -l | { cat; echo "*/10 * * * * bash /app/scripts/clean_tmp.sh"; } | crontab -
RUN crontab -l | { cat; echo "0 0 * * * bash /app/scripts/get_aclanthology.sh"; } | crontab -
# Run the command on container startup
CMD cron

# start service
EXPOSE 7860
CMD ["python", "-u", "server.py"]
