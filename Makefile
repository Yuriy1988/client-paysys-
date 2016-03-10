setup:
	sudo apt-get install python3.5 python3.5-dev python3-pip python-virtualenv

venv_install:
	virtualenv --no-site-packages -p python3.5 venv
	bash -c "source venv/bin/activate && pip install -r requirements.txt"

venv_update:
	bash -c "source venv/bin/activate && pip install -r requirements.txt"

db_install:
	sudo apt-get install postgresql postgresql-contrib python-psycopg2
	#sudo -u postgres dropdb -e --if-exists xopclientdb
	#sudo -u postgres dropuser -e --if-exists xopclientadmin
	sudo -u postgres psql -c "CREATE USER xopclientadmin WITH PASSWORD 'xopclient'"
	sudo -u postgres psql -c "CREATE DATABASE xopclientdb OWNER xopclientadmin"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE xopclientdb TO xopclientadmin"

