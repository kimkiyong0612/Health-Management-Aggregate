import json
import gspread
import pandas as pd
import matplotlib.pyplot as plt

import tempfile

from oauth2client.service_account import ServiceAccountCredentials

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
        ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
        return ws
    except Exception as e:
        print(e)

#


def create_chart(ws):
    COL_TIMESTAMP = "タイムスタンプ"
    COL_MAIL = "メールアドレス"
    COL_PHYSIC_PLUS = "身体の調子はいいですか?"
    COL_PHYSIC_MINUS = "身体の調子は悪いですか?"
    COL_MENTAL_PLUS = "気分は良いですか?"
    COL_MENTAL_MINUS = "気分は悪いですか?"

    # SpreadSheetをdataframe型へ変換
    df = pd.DataFrame(ws.get_all_records())

    # タイムスタンプをdatetime型に変換
    df[COL_TIMESTAMP] = pd.to_datetime(df[COL_TIMESTAMP])
    # スコアをnumeric型へ変換
    targe_cols = [COL_PHYSIC_PLUS, COL_PHYSIC_MINUS,
                  COL_MENTAL_PLUS, COL_MENTAL_MINUS]
    for col in targe_cols:
        df[col] = pd.to_numeric(df[col])

    # グラフ用のcolum追加
    df['physical'] = df[COL_PHYSIC_PLUS] - df[COL_PHYSIC_MINUS]
    df['mental'] = df[COL_MENTAL_PLUS] - df[COL_MENTAL_MINUS]

    # 不要colum削除
    df.drop(targe_cols, axis=1, inplace=True)

    users = list(df[COL_MAIL].drop_duplicates())
    with tempfile.TemporaryDirectory() as temdir:
        print('temdir', temdir)
        for user in users:
            # ユーザ毎のグラフ描画
            df_for_user = df[df[COL_MAIL] == user].rename(
                columns={COL_TIMESTAMP: 'datatime'})
            plt.figure()
            df_for_user.plot.line(title=user, x='datatime', grid=True)
            plt.savefig(f'{temdir}/{user}.png')
            plt.close('all')
            print(f'created chart about {user}')


def lambda_handler(event, context):
    ws = connect_gspread(JSONFILE, SPREAD_SHEET_KEY)
    create_chart(ws)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Completa!!!",
            # "location": ip.text.replace("\n", "")
        }),
    }
