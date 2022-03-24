import azure.functions as func
from booker import booker
from config import CONFIG


def main(req: func.HttpRequest) -> func.HttpResponse:
    booker(CONFIG)

    return func.HttpResponse(f"HTTP triggered function executed successfully.")

