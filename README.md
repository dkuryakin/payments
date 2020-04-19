# payments

## What is it?

This repo implements simple payments system.

## Dependencies

On host machine you just need to have:
 * docker
 * docker-compose
 
Inside docker container it relies on:
 * python3.7
   * fastapi
   * sqlalchemy + gino(for async)
   * passlib
   * pytest
 * postgres11
 
 ## Tests
 
 Just run:
 ```shell script
$ ./run_tests.sh
```

## Run

To run payments, just up it with docker compose:
```shell script
$ docker-compose up --force-recreate --build
```

## Docs

Enjoy swagger docs, based on address 
http://localhost:80/docs

## Database web ui

For simplicity there are also pgadmin:
http://localhost:81

Go to the docker-compose.yml for credentials.