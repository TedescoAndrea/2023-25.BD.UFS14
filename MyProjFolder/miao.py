import azure.functions as func
import datetime
import json
import logging
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import requests
from SCRAPER_DEF import miao

app = func.FunctionApp()

# Qui va il codice del tuo progetto di scraping e aggiornamento file (per brevità non incluso qui)

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Esegui il metodo `miao` per eseguire lo scraping e aggiornare il file
    file_path = "cir_reports.xlsx"
    miao()  # Funzione di scraping e aggiornamento file

    # Verifica che il file Excel sia stato generato
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
        return func.HttpResponse(
            file_data,
            headers={
                "Content-Disposition": f"attachment; filename={file_path}",
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            },
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Errore nella generazione del file Excel",
            status_code=500
        )
