# BUILD APP

sam build --template-file template.dev.yaml


# START APP

sam local start-api -p 8080 --docker-network bc367fa3eb69 --log-file logs.txt