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

And then migrating both. The flask environment is configured in
`.flaskenv`, which is overridden by environment variables.

On Unix:

```
$ flask db upgrade
$ FLASK_ENV=testing flask db upgrade
```

On Windows, you'll have to configure the environment variables
before running flask:

```
> flask db upgrade
> set FLASK_ENV=testing
> flask db upgrade
```

### Run the server

```
$ flask run
```

Alternatively, if that doesn't work you can do

```
$ python -m flask run
```

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

* `S3_BUCKET`: Name of bucket for storing files

### Facebook events querying

Facebook events are retrieved using facebook's
[Graph API](https://developers.facebook.com/docs/graph-api).

The routes for querying group and page events require configuring
access tokens, so the following environment variables must be
configured:

* `FB_GROUP_ID`: Facebook ID of the group to query
* `FB_ACCESS_TOKEN`: User access token from a group admin;

See the
[documentation](https://developers.facebook.com/docs/graph-api/reference/v5.0/group/events)
