#Using Python slim image for lightweight app
FROM python:3.11-slim 

#Set the work directory for app in the container
WORKDIR /app

#Copy the requirement file and then install dependencies in the file
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#Copying entire code into the current directory
COPY /app .

#Exposing the port to which app should be configured to 
EXPOSE 8080

#Defining command to run once container starts
CMD [ "python" , "app.py"]

