# Summarisation service 

This repository contains a summarisation webservice for interview transcriptions. It is a small
wrapper around [the atrium-summarization tool](https://github.com/Aditya3107/ATRIUM_summarization) which in turn uses the DeekSeek LLaMa model. The webservice layer is provided via [CLAM](https://proycon.github.io/clam/). 
This webservice is developed at the Centre of Language and Speech Technology, Radboud University, Nijmegen.

## Installation

For end-users and hosting partners, we provide a container image that ships with a web interface. 
You can pull a prebuilt image from the Docker Hub registry using docker as follows:

```
$ docker pull proycon/sumservice
```

Run the container as follows, a [huggingface token](https://huggingface.co/docs/hub/security-tokens) is required to obtain the LLM on first run:

```
$ docker run -v /path/to/your/data:/data -p 8080:80 --env HF_TOKEN=your_huggingface_token proycon/sumservice 
```

Assuming you run locally, the web interface can then be accessed on ``http://127.0.0.1:8080/``.

If you want to deploy this service on your own infrastructure, you will want to set some of the environment variables
defined in the `Dockerfile` when running the container, most notably the ones regarding authentication, as this is by
default disabled and as such *NOT* suitable for production deployments.
