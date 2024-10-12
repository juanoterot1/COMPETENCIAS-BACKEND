# BUILD APP

sam build --template-file template.dev.yaml


# START APP

sam local start-api -p 8080 --docker-network 272514457fd8 --log-file logs.txt