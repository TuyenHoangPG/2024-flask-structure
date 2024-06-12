# Flask Structure Demo

### Project structure

The project code base is mainly located within the `src` folder. This folder is divided in:

- `apps` - containing all app module like auth, user,...
- `commons` - containing common module for the project like configs, constant, etc.
- `libs` - containing external libs like sendmail, upload,...

- `migrations` - containing all database migration files

```
.
├── src
│   ├── apps                                  # Contain modules
│   │   ├── auth                              # Module auth
│   │   │   ├── dtos                          # Dto
│   │   │   │   └── requests                  # Include all request dto to validate payload
│   │   │   │   └── responses                 # Response data type
│   │   │   │
│   │   │   ├── auth_route.py                 # All route of this module
│   │   │   ├── auth_controller.py            # Controller
│   │   │   ├── auth_service.py               # Service
│   │   │   
│   │   │
│   │   └── app.py                            # Register app, route, middlewares,...
│   │
│   └── commons                               # Contains all shared datas
│   │   │
│   │   ├── configs                           # Configs
│   │   ├── constants                         # Constants
│   │   ├── dtos                              # Dtos
│   │   ├── middlewares                       # Middlewares
│   │   ├── utils                             # Utility code base
│   │   ├── models                            # Entity models
│   │   └── extensions.py                     # Declare extensions
│   │
│   └── app.py                                # Register extension, route, config,...
│
├── migrations                                # Contain all database migration files
├── server.py                                 # Serve Flask app

```

## Editor

- Visual studio code
- Extension: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

## Local Run

### Prepare env and package

- Create file `.env.dev` simular with file `.env.example`
- Replace environment key with your environment value
- Install packages using `pipenv`

```
# pyenv install 3.12
# pyenv shell 3.12 

# pipenv shell
# pipenv install
```

- Or install packages using requirements

```
# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r requirements.txt
```

### Linting and format

- Run lint
```
# pylint src
```
- Format all code
```
# black .
```


### Setup Database

- Install posgresql
- Run migration if folder `migrations` is already exist

```
# flask db upgrade
```

- If you want to create new migration file

```
# flask db revision -m "[Message]"
# flask db upgrade
```

- For new project setup, run the following command

```
# flask db init
# flask db revision -m "[Message]"
# flask db upgrade
```

- If you want upgrade/downgrade a migration file

```
# flask db upgrade/downgrade [revisionId]
```

### Run App

- Run Flask App

```
# export FLASK_ENV=dev
# export FLASK_APP=server.py
# flask run
```

### Swagger UI

```
# http://{{hostname}}/swagger-ui
```

## Docker Run
### Prepare env

- Create file `.env.dev` simular with file `.env.example`
- Replace environment key with your environment value

### Build image and run container
- Build image
```
# docker compose --env-file {env-file-name} -f docker-compose.yml build
```

- Run container
```
# docker compose --env-file {env-file-name} -f docker-compose.yml up
```

### To run migration inside docker container
```
# docker ps  -> to get api container name
# docker exec {api-container-name}  python3 -m flask db upgrade
```

### To run backup database manualy 
- Make sure that you currently run docker container
```
# chmod +x ./scripts/backup_db.sh 
# ./scripts/backup_db.sh [env]
```

### To schedule backup database
- Make sure that you currently run docker container
```
# chmod +x ./scripts/backup_db.sh 
# crontab -e

Then add an entry to schedule run script: 0 15 * * * path/to/the/backup_db.sh [env]
It means the script will run on 15:00 every day

```