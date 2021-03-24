FROM ubuntu
RUN apt-get update -yq && apt-get upgrade -yq && apt-get install -yq curl git nano
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && apt-get install -yq nodejs build-essential
WORKDIR /myapp2
COPY package*.json app.js ./
RUN npm install
EXPOSE 3000
COPY pyworld.sh ./
COPY start.sh ./
EXPOSE 7800
CMD ["/bin/sh", "start.sh"]
