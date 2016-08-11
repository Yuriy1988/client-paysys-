CLIENT_HOST="https://xopay.digitaloutlooks.com"
CLIENT_API_VERSION="dev"

install:
	sudo apt-get install wget curl
	wget -qO- https://deb.nodesource.com/setup_5.x | sudo bash -
	sudo apt-get install --yes nodejs
	npm install

build:
	npm install
	npm run build -- --client_host $(CLIENT_HOST) --client_api_version $(CLIENT_API_VERSION)

dev:
	npm run dev -- --client_host 127.0.0.1:7254 --client_api_version dev
