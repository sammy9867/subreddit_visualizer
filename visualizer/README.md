# Subreddit Visualizer Backend

## Getting Started

### Prerequisite
* Add a .env file and paste the following env variables:
```
# Django
SECRET_KEY=YOUR_SECREY_KEY
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DEBUG=1

# Praw
REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT=YOUR_REDDIT_USER_AGENT
SUBMISSION_LIMIT = 5
COMMENT_LIMIT = 1

# Celery with Redis as broker
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

* We are extracting data from Reddit API using praw. In order to get the client id and secret, you need to sign up [here](https://www.reddit.com/prefs/apps) and create an app.

### Installing 
* We use Docker to build and run the application. After your docker is up and running, execute the following commands to build and run the backend:

```
$ docker-compose up --build
```
* In another terminal, run the following data to migrate Django Models to the database after django service is running:
```
$ docker exec -it visualizer_django python manage.py migrate
```

### Dummy Data
* To fill your database with some initial dummy data, run the following command:
```
$ docker exec -it visualizer_django python manage.py get_subreddits <submission-count> <comment-count>
```

## Usage
* List of all subreddits: http://localhost:8000/api/v1/subreddits/
* List of top weekly submissions of all subreddits: http://localhost:8000/api/v1/weekly-scores/?score_type=sub&week_number=11&year=2021
* List of top weekly comments by subreddit: http://localhost:8000/api/v1/weekly-scores/?score_type=com&week_number=11&year=2021&subreddit_id=2s3qj