#!/bin/bash 
docker stop myenergy_db
docker rm myenergy_db
docker run -d -v $(pwd)/database_storage:/var/lib/postgresql/data -e POSTGRES_DB=myenergy -e POSTGRES_PASSWORD=doros -p 5432:5432 --name myenergy_db postgres
