FROM node:wheezy

ENV PYTHONUNBUFFERED 1

# install python & pip
RUN apt-get update -y
RUN apt-get install -y python-dev
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python -

# create our app dir
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install npm dependencies
ADD package.json package.json
RUN npm install

# set up django app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy local files
ADD . .

# bundle the js
RUN npm run bundle

# run our migrations
RUN python manage.py migrate
