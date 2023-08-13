Detectron2 scalable API
===

This app is designed to be scaled as much as it needs by using simple orchestration by 
`docker-compose`.

Requirements
---

- Docker
- Docker Compose
- make

Architecture
---

- **Nginx** configured as a load balancer and proxies requests using uwsgi_pass module.
- **Flask** is API facade service. You can run as much flask instances as you want, to handle more requests simultaneously. Flask processes are managed by uWSGI.
- **Celery** is used as a task manager to be able to scale number of working processes that are processing video frames. 
- **Redis** is used as a celery broker and results backend.

Make commands
===

build
---

Uses docker compose to build all the docker containers.

start
---

Uses docker compose to start application locally.

stop
---

Uses docker compose to stop application.

clear
---

Removes all host machine docker containers & images.

test-pylint
---

Uses pylint to lint code.

test-units
---

Uses pytest to run unit tests for application services.