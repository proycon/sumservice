FROM nvidia/cuda:13.4.3-base-ubuntu26.04

LABEL org.opencontainers.image.authors="Maarten van Gompel <proycon@anaproy.nl>"
LABEL description="A summarisation service, powered by an LLM"

# By default, there is no authentication on the service,
# which is most likely not what you want if you aim to
# deploy this in a production environment.
# You can connect your own Oauth2/OpenID Connect authorization by setting the following environment parameters
# *AND* mounting files you references here into the container
ENV CLAM_OIDC_CONFIG_FILE=""

# Same for HTTP Basic Authentication:
ENV CLAM_USER_FILE=""

ENV CLAM_URL="http://127.0.0.1:8080"
ENV CLAM_ROOT="./data"

ENV CLAM_LISTEN="0.0.0.0:8080"
ENV CLAM_TERMS_OF_SERVICE=""

# You can use this to set extra parameters to CLAM like --debug
ENV CLAM_EXTRA=""

#Set this to your huggingface token
ENV HF_TOKEN=""

# Install all global dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends cargo rustc curl ca-certificates netcat-openbsd make python3-pip ffmpeg zip git gettext-base && \
    cargo install --root /usr --git https://codeberg.org/proycon/clam --branch clam-4.0

# Add the sources of this webservice
COPY . /var/webservice

ENV XDG_CACHE_DIR=/var/webservice/.cache
ENV XDG_CONFIG_DIR=/var/webservice/.cache
ENV TRANSFORMERS_CACHE=/var/webservice/.cache
ENV MPLCONFIGDIR=/var/webservice/.cache
ENV HF_HOME=/var/webservice/.cache
ENV HOME=/var/webservice
WORKDIR /var/webservice

# Install the service itself, set permissions, and cleanup unneeded sources afterwards
RUN cd /var/webservice && GLOBAL_ENV=1 make install-dependencies && mkdir -p /var/www/webservice/.cache && chown 1000:1000 /var/webservice /var/webservice/.cache && rm -Rf /var/webservice/local.env /var/webservice/.cache/pip /root/.cache /root/.cargo && apt-get remove -y cargo

VOLUME ["/data"]
EXPOSE 8080

USER ubuntu
ENTRYPOINT ["./entrypoint.sh"]
