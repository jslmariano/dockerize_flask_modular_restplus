# FLASK MODULAR RESTFUL With Docker Compose

## Overview

A modular restful api made from flask restplus, and already docker containerized.

Requirements:

- Docker CE ( Could be hosted on windows, vmware or virtualbox | Debian 9 )
- Python 3.7
- Flask (latest)

## Notes

- Please see .env file for database configuration
- No need to import dummy database it wll be handled by `docker-compose`
- *Email* setup is for local only and not for production please see console logs for email confirmations.
- - If you bring up your docker in background please use `docker-compose logs` to peek on console


## Local Dev Instructions

1. Install docker from this tutorial https://docs.docker.com/install/
1. Extract the files on your workspace - `/<path_to_workspace>/dockerize_flask_modular_restplus`
1. Go to your project directory - `/<path_to_workspace>/dockerize_flask_modular_restplus`
1. Build images - `docker-compose build` (This may take a while for 1st time, go grab your coffee :) )
1. Start services - `docker-compose up`
1. Browse your applciation on - `localhost`
1. Always run mmigration for new tables ` docker exec -it dockerize_flask_modular_restplus_web_1 /usr/local/bin/python manage.py migrate`
1. Test scripts are available, `docker exec -it dockerize_flask_modular_restplus_web_1 /usr/local/bin/python manage.py test`

## Restful API
1. Go to https://documenter.getpostman.com/view/6907051/SzezdXyz?version=latest and Click "Run in postman"
1. If your postman opens choose "Flask Modular RestPlus | Local" as environment to your top right corner
1. If the 2 above does not work, proceed below to the manual
1. Download and install postman here https://www.postman.com/downloads/
1. If you wanted to sign-in you can use your google account but this is optional
1. Repeat 1st instruction
1. On your left side panel you should see the "Flask Modular RestPlus" in Collections tab
1. Finally add environment variables
1. Click the gear icon on top right corner
1. Click "Add" button
1. Type "Flask Modular RestPlus | Local" as the environment name
1. Variables are
```
VARIABLE    | INITIAL VALUE    | CURRENT VALUE    |
host        | localhost        | localhost        |
token_auth  | (leave blank)    | (leave blank)    |
```

### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Users ###

Create a user by POSTing to api `/user`, using curl or anything you are comfortable
with body
```
{
    "username":"admin",
    "email":"admmin@example.com",
    "password":"admin"
}
```

### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.

    NOTE: Authorization header is automatically updated in POSTMAN variable `token_auth` if you login using POSTMAN :)


### TROUBLESHOOTING

- If nginx is running then stop it because docker web container will listen to port 80
- If postgresql is running then stop it because docker postgresql container will listen to port 5432
- If using VirtualBox from windows you should mount you files properly for permission correction - `mount -t vboxsf -o rw,uid=1000,gid=1000 <share_name> <mount_path>`
- Local host url - `localhost`


### Idea came from ###
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563


### Contributing
If you want to contribute to this flask modular restplus, clone the repository and just start making pull requests.

```
https://github.com/jslmariano/dockerize_flask_modular_restplus.git
```
