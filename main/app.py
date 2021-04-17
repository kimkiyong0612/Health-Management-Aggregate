import json
import gspread
# import requests

from oauth2client.service_account import ServiceAccountCredentials
"""local test
$ sam build && sam local start-api
"""


JSONFILE = "secreat.json"
SPREAD_SHEET_KEY = "1-NrRiDIs4i-I-Xl9QAvuTzoxLmZxLAsZ3YvrUcSDtnM"


# Google Spread Sheetsにアクセス
def connect_gspread(jsonfile, key):
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            jsonfile, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        return worksheet
    except Exception as e:
        print(e)



def lambda_handler(event, context):
    ws = connect_gspread(JSONFILE, SPREAD_SHEET_KEY)

    print(ws)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "get request",
            # "location": ip.text.replace("\n", "")
        }),
    }
