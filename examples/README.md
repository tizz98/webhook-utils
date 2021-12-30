# Webhook Utils Examples

## FastAPI

Run an end-to-end FastAPI example in 2 parts:

1. Run the [webhook receiver](./fastapi-webhook-receiver/README.md) using `WebhookRouter` in 1 terminal
2. Run the [webhook sender](./fastapi-webhook-sender/README.md) using `WebhookAuth` in another terminal
3. Run a `curl` command to test the full process
    ```shell
    curl -X POST -H "Content-Type: application/json" \
      -d '{"message": "Hello, world!"}' \
      http://localhost:8001/demo
    ```
