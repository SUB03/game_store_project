## Learning Project: Online Game Distribution Platform

**Work in progress**

This is a learning project where I am building an online game distribution platform.

## Running on Linux

### 1. Generate a secret key

Create a `.env` file entry for the JWT secret key:

```bash
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

### 2. Add the database URL

Add the following line to your generated `.env` file:

```env
SQLALCHEMY_URL=postgresql+psycopg://postgres:postgres@postgres:5432/learning
```

### 3. Optional: initialize the database with games

If you want to populate the database with games:

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset).
2. Place it in the `datasets` folder.
3. Run the dataset filter script:

```bash
python filter_dataset.py
```

### 4. Create the database tables

Run the Alembic migrations:

```bash
alembic -c store_service/alembic.ini upgrade head
alembic -c auth_service/alembic.ini upgrade head
```

If the dataset is available, the tables will also be populated.

### 5. Start the project

Run the project with Docker Compose:

```bash
docker-compose up -d
```

## Local development

For local development, you may also want to install the protobuf packages:

```bash
cd shared
pip install -e ./protobufs
```