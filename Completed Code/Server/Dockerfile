# our base image
FROM python:3.9-slim

# ENV Variables
ENV IPADDRESS 192.168.1.154

# install Python modules needed by the Python app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD python -u "Server.py" $IPADDRESS
