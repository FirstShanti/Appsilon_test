# Wikidata Display Project

This project is a web application that allows users to browse movies from Wikidata. The application is built using Flask AppBuilder, Docker, and PostgreSQL.

## Features

- Display Wikidata entities with details such as title, release date, and imdbId.
- Filter entities based on release year and less or equal then today.
- Dockerized deployment for easy setup and scalability.
- PostgreSQL database for data storage.

## Problems

- some entities has two different records with different imdbId and vise versa, that show Wikipedia issue. We can find duplicates and wrong references to imdb.

## Requirements

- Python 3.10
- Flask AppBuilder
- Docker
- PostgreSQL

## Installation

- clone repository
```git clone https://github.com/your-username/Appsilon_test.git```
- go into the project directory:
```cd Appsilon_test```
- install docker, docker compose
- create .env file:
    POSTGRES_USER=appsilon
    POSTGRES_PASSWORD=12345
    POSTGRES_DB=appsilon
    ADMIN_USERNAME=admin
    ADMIN_PASSWORD=admin
    SECRET_KEY=BLABLABLA
- run command:
```docker compose run --build```