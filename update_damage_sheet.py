import gspread

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = '.secrets/PythonSheetsApiSecret.json'
CREDENTIALS_TOKEN = '.secrets/token.json'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1oc5TC_nGzLXk4sP3zhlyFeYt526cxXXVeDtvMDFWbno'
VALUE_RENDER_OPTION = 'FORMULA'
VALUE_INPUT_OPTION = 'RAW'

stats_starting_row = 4
stylte_stats_sheet = 'StyleStats'
style_stats_range = 'B4:T'
style_final_str_column = 'StyleStats!M4:M'
style_final_end_column = 'StyleStats!N4:N'
style_final_dex_column = 'StyleStats!O4:O'
style_final_agi_column = 'StyleStats!P4:P'
style_final_int_column = 'StyleStats!Q4:Q'
style_final_wil_column = 'StyleStats!R4:R'
style_final_lov_column = 'StyleStats!S4:S'
style_final_cha_column = 'StyleStats!T4:T'


class Character:
    rows = []
    name = ''


def login():
    return gspread.oauth(credentials_filename=CLIENT_SECRET_FILE, authorized_user_filename=CREDENTIALS_TOKEN)


def get_styles(auth):
    style_sheet = auth.open_by_key(SPREADSHEET_ID)
    styles = style_sheet.worksheet(stylte_stats_sheet).get(style_stats_range, value_render_option=VALUE_RENDER_OPTION)
    characters = {}
    for i, s in enumerate(styles):
        if s[0] not in characters:
            characters[s[0]] = [i + stats_starting_row]
        else:
            characters[s[0]].append(i + stats_starting_row)
    return characters


def update_sheet(auth, characters):
    style_sheet = auth.open_by_key(SPREADSHEET_ID)
    style_data_sheet = style_sheet.worksheet(stylte_stats_sheet)
    style_data_sheet.update('A1', 'Testing')


if __name__ == '__main__':
    update_sheet(login(), '')
