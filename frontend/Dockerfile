# Dockerfile for Vue frontend
FROM node:16-alpine

# set working directory
WORKDIR /app

# copy package files and install dependencies
COPY package*.json ./
RUN npm install

# copy source code
COPY . .

# expose dev server port
EXPOSE 3000

# start the app
CMD ["npm", "run", "serve"]
