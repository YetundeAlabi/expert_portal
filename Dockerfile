FROM python:3.9

RUN mkdir -p /home/app

# create the app user
RUN addgroup app && adduser --system --no-create-home app --ingroup app

# create the appropriate directories
ENV HOME=/home/app

ENV APP_HOME=/home/app/

WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt $APP_HOME

RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN mkdir -p static

RUN mkdir -p media

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
