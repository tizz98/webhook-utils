# FastAPI Webhook Sender

A demo FastAPI webhook sender.

## Setup

```shell
pip install webhook-utils[examples]
```

## Running

```shell
git clone git@github.com:tizz98/webhook-utils.git
cd webhook-utils/examples/fastapi-webhook-sender
uvicorn main:app --port 8001
```

This is just a demo, so you can use any arbitrary JSON data to test.

```shell
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "Hello, world!"}' \
  http://localhost:8001/demo
```
