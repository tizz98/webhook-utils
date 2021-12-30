# FastAPI Webhook Receiver

A demo FastAPI webhook receiver.

## Setup

```shell
pip install webhook-utils[examples]
```

## Running

```shell
git clone git@github.com:tizz98/webhook-utils.git
cd webhook-utils/examples/fastapi-webhook-receiver
uvicorn main:app
```

Webhooks can be sent to the server using the following URL:
`POST http://localhost:8000/webhooks/demo`

The body will be printed to the console if the signature is valid.
If the signature is not set a 403 will be returned.
If the signature is invalid a 401 will be returned.
