import azure.functions as func
from booker import booker
from config import CONFIG

def main(timer: func.TimerRequest) -> None:
    booker(CONFIG)