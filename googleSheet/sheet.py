import gspread
from data.ingest import cleanup
from ingest_data import reload_ingest_manifest


# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1oc5TC_nGzLXk4sP3zhlyFeYt526cxXXVeDtvMDFWbno'
VALUE_RENDER_OPTION = 'FORMULA'
VALUE_INPUT_OPTION = 'RAW'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = '.secrets/PythonSheetsApiSecret.json'
CREDENTIALS_TOKEN = '.secrets/token.json'

# data update cache flag
Ingest_Cache_Clean = False


def login():
    return gspread.oauth(credentials_filename=CLIENT_SECRET_FILE, authorized_user_filename=CREDENTIALS_TOKEN)


def ensure_data_updated():
    if Ingest_Cache_Clean:
        return
    else:
        reload_ingest_manifest()
        cleanup()
