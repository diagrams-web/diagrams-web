# diagrams-web
Still work in progress to edit and generate [diagrams](https://github.com/mingrammer/diagrams) with your browser.

Contributions are welcome!

This project is built on Python (Flask app).

No more active project:
- Node.js version (Polka and Sapper with Typescript), check it out: [microdiagram](https://github.com/renyuanz/microdiagram)

## Instructions:

### from source:

from source root, run `docker-compose up --build`

Wait to have something like this:
```shell
web_1  |  * Serving Flask app "app" (lazy loading)
web_1  |  * Environment: production
web_1  |    WARNING: This is a development server. Do not use it in a production deployment.
web_1  |    Use a production WSGI server instead.
web_1  |  * Debug mode: on
web_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
web_1  |  * Restarting with stat
web_1  |  * Debugger is active!
web_1  |  * Debugger PIN: 830-873-016
```

then open your browser http://0.0.0.0:5000/

and start coding! (i.e updating the code of diagrams-web)


### from docker hub:

Here is only if you want to use the interface.

Get the latest image from dockerhub

```shell
docker pull banana123/diagrams-web:latest
```

Use any familiar tool to run the container OR

Create a new network if you don't want to mess up with your other projects:
```shell
docker network create --subnet=172.22.0.0/16 diagrams-net
```

Start the container in the previous created subnet with a specific ip.
```shell
docker run --name diagrams-web --net diagrams-net --ip 172.22.0.10 banana123/diagrams-web
```
You should be able to access the interface on:

http://172.22.0.10:5000/

You also should have access to the logs if it crash and you need to debug!

If you need to access inside the container to check what is inside 
```shell
docker exec -it diagrams-web ash
```

![Screenshot](web/static/new_design.png)
