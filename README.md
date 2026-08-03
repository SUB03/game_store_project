## THIS IS A LEARNING PROJECT WHERE I BUILD A ONLINE GAME DISTRIBUTION PLATFORM

WORK IN PROGRESS

Running steps for linux:

First step is to generate secret key using `echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env`.

Then you have to add `SQLALCHEMY_URL=postgresql+psycopg://postgres:postgres@postgres:5432/learning` to your generated .env

If you want to init db with games you have to download dataset from [kaggle](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset), place it in datasets folder and filter it with `python filter_dataset.py`

Then you need to create tables (and if you have installed datasets it will populate tables) with
`alembic -c store_service/alembic.ini upgrade head` and `alembic -c auth_service/alembic.ini upgrade head` commands

Finally you can run project with `docker-compose up -d`.

For local development u also might wanna install proto as packages:
use `cd shared` and then `pip install -e ./protobufs` for dev build.