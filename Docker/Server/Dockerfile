# our base image
FROM python:3.9-slim
 
# install Python modules needed by the Python app
COPY ../../requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p "/Completed Code/Server"

#copy everything into the image
ADD ["../../Completed Code/Server", "Completed Code/Server"]

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "Completed Code/Server/Server.py"]

