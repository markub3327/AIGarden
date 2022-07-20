# AIGarden 🚰🌱🥕🍅

[![Release](https://img.shields.io/github/release/markub3327/AIGarden)](https://github.com/markub3327/AIGarden/releases)
[![Issues](https://img.shields.io/github/issues/markub3327/AIGarden)](https://github.com/markub3327/AIGarden/issues)
![Commits](https://img.shields.io/github/commit-activity/w/markub3327/AIGarden)
![Size](https://img.shields.io/github/repo-size/markub3327/AIGarden)
[![Visits](https://badges.pufler.dev/visits/markub3327/AIGarden)](https://badges.pufler.dev)
[![Updated](https://badges.pufler.dev/updated/markub3327/AIGarden)](https://badges.pufler.dev)

This open-source project is using Raspberry Pi to control your garden and simplified caring about the garden. You can make watering autonomous and monitoring plants smarter.

## Development
```shell
docker build -t markub3327/ubuntu-web:latest ./docker
```

## Deployment

- ### Install packages
```shell
sudo apt update && sudo apt upgrade -y
sudo apt install python3-lgpio python3-pip -y

git clone https://github.com/markub3327/AIGarden
cd AIGarden/
```
- ### Install requirements 
```shell
python3 -m pip install -r requirements.txt --no-cache-dir
```
- ### Run (in developer mode)
```shell
cd ai_garden/
python3 manage.py runserver 0:8000
```


| | |
|------------------|------------------------------|
| Operating system | Ubuntu Server 22.04          |
| Boards           | Raspberry Pi 4               |
| Sensors          | DHT22, BMP180, Soil moisture |


------------------------------------------
**Frameworks:** Tensorflow, OpenCV, Django
