# Facebook_scraper
This repository is a dockerised scraper application for facebook public pages.
## How to run
First, you need to install and configure Docker on your system following this ([installation guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-fr)).
Then, excute this commands
```
$ git clone https://github.com/maramraddaoui/Facebook_scraper
$ cd [path_to_custom_scraper_project]
$ docker-compose up -d --build
$ docker run -i -t -p 8080:8000 scraperapp:v1
```
## Run tests
```
$ docker exec -it [container_id] bash
$ pytest -v
```
## Clean-up
This command helps to Stop and remove containers, networks, images, and volumes.
```
$ docker-compose down
```
