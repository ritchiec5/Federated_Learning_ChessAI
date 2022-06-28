# Running the docker code

```console
cd 'Completed Code'

// build the docker compose up
docker-compose up --build

// run docker-compose
docker-compose up

// run detached
docker-compose up -d

// stop docker compose
docker-compose down
```

// extract file from container
docker cp <containerId>:/file/path/within/container /host/path/target

You may adjust the docker compose file to add more clients 

``` console
docker-compose up --build --remove-orphans --force-recreate
```
// Should there be any error
