# BUILD APP

sam build --template-file template.dev.yaml


# START APP

sam local start-api -p 8080 --docker-network 9254b51da23f --log-file logs.txt