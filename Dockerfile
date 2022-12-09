FROM python:3

WORKDIR /app

COPY webhookrelay/ ./
RUN pip3 install -r requirements.txt


CMD [ "python3", "-u" , "app.py"]
