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

db_install_mac:
	brew install postgresql
	sudo PATH=$PATH:/usr/pgsql-9.5.1/bin/ pip install psycopg2
	sudo -u postgres psql -c "CREATE USER xopclientadmin WITH PASSWORD 'xopclient'"
	sudo -u postgres psql -c "CREATE DATABASE xopclientdb OWNER xopclientadmin"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE xopclientdb TO xopclientadmin"


# ------ Database -----
DB_NAME=xopclientdb
DB_USER=xopclientadmin
DB_PASSWORD=xopclient

db_psql_remove:
	sudo -u postgres dropdb -e --if-exists $(DB_NAME)
	sudo -u postgres dropuser -e --if-exists $(DB_USER)

db_psql_create: db_psql_remove
	sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASSWORD)'"
	sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER)"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $(DB_NAME) TO $(DB_USER)"

db_clean:
	sudo -u postgres psql $(DB_NAME) -c "DROP SCHEMA public CASCADE"
	sudo -u postgres psql $(DB_NAME) -c "CREATE SCHEMA public"
	sudo -u postgres psql $(DB_NAME) -c "GRANT ALL ON SCHEMA public TO postgres"
	sudo -u postgres psql $(DB_NAME) -c "GRANT ALL ON SCHEMA public TO public"


# ------ For DB testing -----
DB_TEST_NAME=xopclienttestdb
DB_TEST_USER=xopclienttest
DB_TEST_PASSWORD=test123

db_test_create:
	sudo -u postgres dropdb -e --if-exists $(DB_TEST_NAME)
	sudo -u postgres dropuser -e --if-exists $(DB_TEST_USER)
	sudo -u postgres psql -c "CREATE USER $(DB_TEST_USER) WITH PASSWORD '$(DB_TEST_PASSWORD)'"
	sudo -u postgres psql -c "CREATE DATABASE $(DB_TEST_NAME) OWNER $(DB_TEST_USER)"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $(DB_TEST_NAME) TO $(DB_TEST_USER)"

db_init: db_psql_create db_test_create
	rm -r -f migrations
	./manage.py db init
	./manage.py db migrate
	./manage.py db upgrade

db_update:
	./manage.py db migrate
	./manage.py db upgrade

db_create: db_psql_create db_update
