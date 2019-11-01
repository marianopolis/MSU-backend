# MSU backend

Backend for the MSU app. Used by congress members to upload information
and documents for students to use.

## Running

To run the app, you need to have the following installed and running:
  * Python 3.7+
  * PostgreSQL

### Install dependencies

```
$ pip install -r requirements.txt
```

### Set up the Postgres table

```
$ psql -U postgres
postgres=# CREATE DATABASE msu_dev;
postgres=# CREATE DATABASE msu_test;
postgres=# \q
$ FLASK_APP=msu FLASK_ENV=development flask db upgrade
$ FLASK_APP=msu FLASK_ENV=testing flask db upgrade
```

### Run the app

```
$ FLASK_APP=msu FLASK_ENV=development flask run --host=0.0.0.0
```

### Run the tests

```
python -m pytest
```
