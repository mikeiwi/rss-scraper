# RSS-scraper
Django RSS scraper built with docker-compose, postgresql, rabbit-mq and celery.

## Requirements
- [Docker](https://www.docker.com/)
- [Docker compose](https://docs.docker.com/compose/)

## Running the app
To run the project you have to:
- build the docker image first by running `docker-compose build`
- then you can run the built image with `docker-compose up`

Everything is now installed in containers and running thanks to the magic of docker compose. Now you may navigate to your browser at http://localhost:8000 and you'll see a login page. You are ready to start using the RSS scraper!

## Testing

To run all of the existing tests in the project just type `docker-compose run web pytest`. 

You may also check the coverage jus tby adding `--cov` to the pytest command, just like this: `docker-compose run web pytest --cov`

## Technical Specs
The rss scrapper use [feedparser](https://pythonhosted.org/feedparser/), a very powerful rss library, for all the scrapping. 

We have 3 main models in our site:
- User
- Feed 
- Entry

**Feed** and **User** have a many to many relationship, this means that multiple users may follow the same feed (the field *url* is unique among all feeds). This way we don't have to update duplicated feeds. Even when a user updates a feed manually, it will be updated for all the users that follow that feed. All users win.

**Entry** is an item of the feed. Every time the feed is updated, new entries are created for the feed. But if the *link* of the entry already exists, the entry is updated.

**Entry** is also related to **User**. Why?, well any user may bookmark an entry. Even multiple users may bookmark the same entry. So you guessed right, **Entry** and **User** have a many to many relationship as well.

Celery is our boss for updating the feeds asynchronously. Users may manually update a feed this way and there is also a crontab job running every hour updating all the feeds.


# Nice to have list
This project was created as simple as possible, in order to make it easy to read and develop. As any other small simple project there are always things you wish to have, these are a few I suggest that I feel are some of the most important ones:
- multiple Dockerfile and docker-compose.yml files for different environments. Currently all development libraries are being installed and there are some unneeded config for production environments.
- Gunicorn and Nginx (or any server architecture for production porpuses). Right now we're using the built-in django server.
- Environment Variables: of course you can't go around having all your credentials, sensible and special configuration hiding in plain sight.
