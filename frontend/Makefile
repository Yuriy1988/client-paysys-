CLIENT_HOST="http://192.168.1.118:7254"
CLIENT_API_VERSION="dev"

install:
	sudo apt-get install wget curl
	wget -qO- https://deb.nodesource.com/setup_5.x | sudo bash -
	sudo apt-get install --yes nodejs
	npm install

build:
	npm install
	npm run build -- --client_host $(CLIENT_HOST) --client_api_version $(CLIENT_API_VERSION)
