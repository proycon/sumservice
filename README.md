# Summarisation service 

This repository contains a summarisation service powered by [a finetuned version of mbart by ML6](https://blog.ml6.eu/why-we-open-sourced-two-dutch-summarization-datasets-1047445abc97) for Dutch, and [CLAM](https://proycon.github.io/clam/). This webservice is developed at the Centre of Language and Speech Technology, Radboud University, Nijmegen.

## Installation

For end-users and hosting partners, we provide a container image that ships with a web interface. 
You can pull a prebuilt image from the Docker Hub registry using docker as follows:

```
$ docker pull proycon/sumservice
```

Run the container as follows:

```
$ docker run -v /path/to/your/data:/data -p 8080:80 proycon/sumservice
```

Assuming you run locally, the web interface can then be accessed on ``http://127.0.0.1:8080/``.

If you want to deploy this service on your own infrastructure, you will want to set some of the environment variables
defined in the `Dockerfile` when running the container, most notably the ones regarding authentication, as this is by
default disabled and as such *NOT* suitable for production deployments.

