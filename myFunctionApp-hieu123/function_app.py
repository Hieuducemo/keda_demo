import os

import azure.functions as func
from azure.storage.queue import QueueClient

app = func.FunctionApp()

@app.function_name(name="SendToQueue")
@app.route(route="send", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    queue_name = "hieuduc231"
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if not connection_string:
        return func.HttpResponse("Missing storage connection string", status_code=500)

    try:
        req_body = req.get_json()
        message = req_body.get("message", "Hello from Azure Function!")
    except ValueError:
        return func.HttpResponse("Invalid JSON body", status_code=400)

    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    queue_client.send_message(message)

    return func.HttpResponse(f"Message sent: {message}", status_code=200)
