# Docker-Webserver (nginx:mainline-alpine)

**NB!** Big change is in progress, consider this an **alpha** product!

## What is it?

Simple to use CLI for setting up nginx webserver in Docker Swarm
and adding websites' configs, proxies and static files

----

## Technology Stack

* **Docker Swarm** for orchestration
* **click** for CLI scripts

----

## Features

* **Run Highly-Available *nginx:mainline-alpine* stack** with attachable **nginx** network (*to use with others containers*) -> `webserver run`
* **Update stack images *without downtime*** -> `webserver update`
* **Generate HTTPS config** for website with examples -> `webserver genconf`
* **Get LetsEncrypt SSL certificate** for website *with one command and no configuration* (*except DNS A record*) -> `webserver gentls`
* **Generate DH params** for website -> `webserver gendh`
* Work with configuration files:
  * **Add configuration file** for website -> `webserver conf add`
  * **Generate and add config with one command** -> `webserver conf create`
  * **Edit configuration file** for website -> `webserver conf edit`
  * **Reload configs *without downtime*** -> `webserver conf reload`
* **Add/Update static files** for website -> `webserver static add`

ROADMAP (v1.0.0)
----
* **See stats** of running stack
* **Stop** the stack
* **Restart** the stack

ROADMAP (v1.x.x)
----
* **Analyze logs with GoAccess**

----

Made by Igor Nehoroshev (https://neigor.me) for his own needs (if You find it useful - great!😎)