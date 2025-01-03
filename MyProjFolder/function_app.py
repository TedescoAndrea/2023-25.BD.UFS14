import azure.functions as func
import datetime
import json
import logging
from animal_detection import detect_animal_sound  # Importa la funzione

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    sound = req.params.get('sound')

    if not sound:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sound = req_body.get('sound')

    if sound:
        animal = detect_animal_sound(sound)
        return func.HttpResponse(f"Riconosciuto: {animal}.")
    else:
        return func.HttpResponse(
            "Specifica un suono (miao o bau). Miao miao miao",
            status_code=200
        )
