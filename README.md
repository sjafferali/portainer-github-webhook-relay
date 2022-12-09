[![Docker Hub badge](https://img.shields.io/docker/pulls/sjafferali/portainer-github-webhook-relay)](https://hub.docker.com/repository/docker/sjafferali/portainer-github-webhook-relay)


# portainer-github-webhook-relay
A simple webhook that relays github webhooks to portainer to avoid dealing with portainer webhook URLs.

This app allows you to use a single web hook URL for portioner stack webhooks. 

## Usage

Here are some example snippets to help you get started creating a container.

### docker-compose

```yaml
---
version: "3.4"
services:
  webhookrelay:
    container_name: webhookrelay
    restart: unless-stopped
    image: sjafferali/portainer-github-webhook-relay:latest
    environment:
      - PORTAINER_ENDPOINT=https://myportainerendpoint.com
      - PORTAINER_USERNAME=username
      - PORTAINER_PASSWORD=password
    ports:
      - 80:80
    restart: unless-stopped
```

### docker cli ([click here for more info](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
  --name=webhookrelay \
  -e =Europe/London \
  -e PORTAINER_ENDPOINT=https://myportainerendpoint.com \
  -e PORTAINER_USERNAME=username \
  -e PORTAINER_PASSWORD=password \
  -p 80:80 `#optional` \
  --restart unless-stopped \
  sjafferali/portainer-github-webhook-relay:latest
```

## Environment Variables

| Name | Description | Optional |
|:--|:--|:--|
| PORTAINER_ENDPOINT | Endpoint of portainer instance to query for webhooks and send webhooks to. | False |
| PORTAINER_USERNAME | Username to authenticate with. | False |
| PORTAINER_PASSWORD | Password to authenticate with. | False |
| PORTAINER_TOKEN_EXPIRATION | How long to cache the authentication token. Defaults to 7 hours. | True |
| STACK_CACHE_EXPIRATION | How long to cache the portainer stack details. Defaults to 0 which means it will query portainer for the list of stacks on every webhook that is received. | True |
