FROM node:13


# Create app directory
ADD code/ /home/cybersec/proj1/
WORKDIR /home/cybersec/proj1/

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)

RUN npm install

# Bundle app source
COPY . .

EXPOSE 3000
CMD [ "npm", "start" ]
