import gspread

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = '../.secrets/PythonSheetsApiSecret.json'
CREDENTIALS_TOKEN = '.secrets/token.json'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1oc5TC_nGzLXk4sP3zhlyFeYt526cxXXVeDtvMDFWbno'
VALUE_RENDER_OPTION = 'FORMULA'
VALUE_INPUT_OPTION = 'RAW'


def login():
    return gspread.oauth(credentials_filename=CLIENT_SECRET_FILE, authorized_user_filename=CREDENTIALS_TOKEN)
