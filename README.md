# FB-SCRAPER

In this work I tried to scrape the data from the FB public Page of [Nintendo](https://www.facebook.com/Nintendo/ ), then build up this service to form a web framework using fastAPI. 
Besides, the scraped posts and all their details were saved in a mongodb database.
Finally, this scraping service was Dockerized  as well as the database.



# The development environment:

1. Verify if python installed as well as install the virtualenv package

    ```bash
    python --version 
    pip install virtualenv
    ```

2. Create your python environment

    ```
    python -m venv py_env
    ```

3. Activate your virtual environment 

    ```
    source app/py_env/bin/activate #in Ubuntu 20.04 
    ```

4. While the py_env is active, use the requirements.txt with pip or these commands:

    ```
    pip install -r requirements.txt
    ```

5. Create an .env file and put these pieces of information:

    DB_CONNECTION: "mongodb connection string"

5. To test the app locally with debug mode:
    ```
    uvicorn src.app.main:app --reload
    ```

# MongoDB environment:
0. Install mongodb
```
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org

```


1. start mongod serivce
```
sudo systemctl start mongod.service
```

2. Verify that mongod service is running.
```
sudo systemctl status mongod
```


3. Run the mongo shell and add a user with read/write privileges. 
```
use admin
db.createUser({ user: "admin" , pwd: "admin", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]})
```
4. Log in to mongo as the new user
```
mongo --port 27017 -u "admin" -p "admin" --authenticationDatabase "admin"
```
5. Cretae a new db named fb_scraper.Then Create a collection named posts.
```
use fb_scraper
db.createCollection("posts")
```


# Dockerization:

```
docker-compose up
```

# Tests:



# Technologies:

- Fastapi & uvicorn
- Mongodb
- Docker



