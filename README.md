# firebase_web_notifications_sent

## Setup

### Clone the repository:

```sh
$ git clone git@github.com/su-bitcoding/firebase_web_notifications_sent.git
$ cd firebase_web_notifications_sent
```

### Create a virtual environment to install dependencies and activate it:

```sh
$ python3 -m venv env
$ source env/bin/activate
```

### Install the dependencies:

```sh
$ pip install -r requirements.txt
```

### Migrations:

```sh
$ python manage.py migrate
```

### Run the server:

```sh
 $ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

### Generate a firebaseConfig

```sh
your firebase a project when you sent a notifications in project settings in you create a web app that you can get a config file
```

### Generate KEY_FILE_PATH 

```sh
your firebase a project in a settings in service account in generate a key file
 
```

### Generate vapidKey 

```sh
your firebase a project in a settings in cloud messaging in generate a keypair is your vapidKey 

```

### Sent notifications cURL

```sh
curl --location 'http://127.0.0.1:8000/sent-web-notification' \
--header 'Cookie: csrftoken=IrIwJfkiZR7W5l6rauazusaybAesDtFP' \
--form 'token="your generate a frontend side token "'  \
--form 'title="hello Testing"' \  
--form 'body="testing"'
```