# Krpsim
Projet d'optimisation du rendement d’un graphe de processus, avec des contraintes de ressources

## Installation

Install docker via [Docker.com](https://www.docker.com/products/docker-desktop) or with [Brew](https://brew.sh)
```bash
brew cask install docker
```
Make sure Docker Desktop is running on your machine then build the docker container
```bash
docker build -t krpsim .
```

## Usage

To run the program, run
```bash
docker run krpsim <file> <delay>
```

To see the full list of flags run
```bash
docker run krpsim --help
```