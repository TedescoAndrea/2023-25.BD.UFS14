import logging
import requests
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import azure.functions as func

# Lista degli URL da cui fare scraping
urls = [
    "https://cir-reports.cir-safety.org/FetchCIRReports",
    "https://cir-reports.cir-safety.org/FetchCIRReports/?&pagingcookie=%26lt%3bcookie%20page%3d%26quot%3b1%26quot%3b%26gt%3b%26lt%3bpcpc_name%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_ingredientidname%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_cirrelatedingredientsid%20last%3d%26quot%3b%7bC223037E-F278-416D-A287-2007B9671D0C%7d%26quot%3b%20first%3d%26quot%3b%7b940AF697-52B5-4A3A-90A6-B9DB30EF4A7E%7d%26quot%3b%20%2f%26gt%3b%26lt%3b%2fcookie%26gt%3b&page=2",
]

def fetch_cir_reports(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        records = []
        for result in data.get("results", []):
            ingredient_name = result.get("pcpc_ingredientname", "")
            inci_name = result.get("pcpc_ciringredientname", "")
            id_link = result.get("pcpc_ingredientid", "")
            link = f"https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={id_link}"
            records.append({
                "Ingredient_Name": ingredient_name,
                "INCI_Name": inci_name,
                "Link": link
            })
        return records
    else:
        logging.error(f"Errore durante il recupero dei dati: {response.status_code}")
        return []

def fetch_and_collect_all():
    all_records = []
    for url in urls:
        logging.info(f"Recupero dati dall'URL: {url}")
        records = fetch_cir_reports(url)
        all_records.extend(records)
    return all_records

def save_to_excel(records, file_path):
    df = pd.DataFrame(records).drop_duplicates(subset=["Ingredient_Name"])
    if os.path.exists(file_path):
        wb = load_workbook(file_path)
        ws = wb.active
        ws.delete_rows(2, ws.max_row)
    else:
        wb = load_workbook(BytesIO())
        ws = wb.active
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    wb.save(file_path)
    logging.info(f"Dati salvati in '{file_path}'")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Inizio della funzione di scraping e aggiornamento del file Excel.")
    file_path = "/tmp/cir_reports.xlsx"

    records = fetch_and_collect_all()
    if records:
        save_to_excel(records, file_path)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            return func.HttpResponse(
                data,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={'Content-Disposition': 'attachment; filename="cir_reports.xlsx"'}
            )
        else:
            return func.HttpResponse("Errore: il file Excel non è stato generato.", status_code=500)
    else:
        return func.HttpResponse("Nessun nuovo dato da aggiornare.", status_code=200)
