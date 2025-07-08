# Reverse Proxy
This is a reverse proxy built using Nginx. The folder nginx houses the reverse proxy logic. 
The backend folder houses a temporary http pages with mock up UIs. 
The docker-compose.yml spins up 2 images (one for the temp backend and the other for the reverse proxy) 
and puts them on the same network.

## Quickstart (linux)
From a terminal:
```
# make sure you are in the reverse_proxy folder
# build the docker images 
docker-compose up --build

# view pages in a web browser
http://localhost/main
http://localhost/question-editor
http://localhost/gameboard
```
