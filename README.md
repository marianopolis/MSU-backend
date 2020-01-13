# MSU backend

<p align="center">
  <b><a href="#setup">Setup</a></b>
  |
  <b><a href="#configuration">Configuration</a></b>
</p>

Backend for the MSU app. Used by congress members to upload information
and documents for students to use.

## Setup

To run the app, you need the following installed and running:
  * Python 3.7+
  * PostgreSQL

### Install dependencies

```
$ pip install -r requirements.txt
```

### Set up the Postgres tables

Ensure that the PostgreSQL service is running on your system.

On Windows, search for the 'Services' app, find the service called
'postgresql-\*', and click on 'Start'

By default, Postgres is accessed through the superuser 'postgres' with
password 'postgres'. If you don't already have such a user, you can
connect to the Postgres instance by running psql and then the following
commands:

```
CREATE USER postgres;
ALTER USER postgres PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
\q
```

The default configuration under `config.py` assumes you have the
`msu_dev` and `msu_test` databases created, which are used for
development and testing, respectively. You can create them by doing:

```
$ psql -U postgres
postgres=# Password for user postgres:postgres
postgres=# CREATE DATABASE msu_dev;
postgres=# CREATE DATABASE msu_test;
postgres=# \q
```

And then migrating both.

On Unix:

```
$ FLASK_APP=msu FLASK_ENV=development flask db upgrade
$ FLASK_APP=msu FLASK_ENV=testing flask db upgrade
```

On Windows, you'll have to configure the environment variables
before running flask:

```
> set FLASK_APP=msu
> set FLASK_ENV=development
> flask db upgrade
> set FLASK_ENV=testing
> flask db upgrade
```

### Run the app

```
$ FLASK_APP=msu FLASK_ENV=development flask run --host=0.0.0.0
```

The `0.0.0.0` is to allow devices on your local network to connect
to the server.

### Run the tests

```
python -m pytest
```

## Configuration

All the configuration for the app is done under `config.py`,
which can be accessed through the app's config property:

```py
from flask import current_app

current_app.config['KEY']
```

The app uses several external services to provide its features,
which are configured as follows.

### File hosting

Files are hosted on AWS S3, which is interfaced using boto3. To
use boto3, you'll first need to configure your account credentials,
as seen on the
[boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

Then, ensure the following environment variables are set:

* `S3_BUCKET_FILES`: Name of bucket for storing general files
* `S3_BUCKET_IMAGES`: Name of bucket for storing images