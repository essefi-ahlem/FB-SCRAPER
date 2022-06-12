# pull official base image
FROM python:3.9.7

#set the working directory
WORKDIR /scraping_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#copy project
COPY . /scraping_app

# copy requirements file
#COPY ./requirements.txt /scraping_app/requirements.txt

#install requirements
RUN pip install -r /scraping_app/requirements.txt 

CMD ["python", "src/app/main.py"]

