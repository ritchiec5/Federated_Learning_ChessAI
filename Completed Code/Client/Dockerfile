# our base image
FROM python:3.9-slim

# ENV Variables
ENV FLASKPORT 5001
ENV STOCKFISHPORT 8080
ENV IPADDRESS 192.168.1.154


# install Python modules needed by the Python app
COPY requirements.txt ./

RUN pip install -r requirements.txt

# copy everything into image
COPY . .

# tell the port number the container should expose
EXPOSE 5001

# run the application
CMD python -u "Client.py" $FLASKPORT $STOCKFISHPORT $IPADDRESS