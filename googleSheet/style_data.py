from googleSheet import sheet
import data.ingest
import ingest_data
from operator import attrgetter


style_data_sheet_name = 'StyleData'
cell_range_start = 'A3:AG'


def update_style_data():
    # get character/style data
    sheet.ensure_data_updated()
    styles = data.ingest.load_styles()
    characters = data.ingest.load_characters(styles)
    characters.sort(key=attrgetter('name'))
    # login, set working sheet
    auth = sheet.login()
    style_sheet = auth.open_by_key(sheet.SPREADSHEET_ID)
    style_data_sheet = style_sheet.worksheet(style_data_sheet_name)
    # set update params
    cell_range = cell_range_start + str(3 + len(styles))
    rows = []
    for c in characters:
        for style in c.styles:
            # style data
            c_row = [c.name]
            c_row.append(style.style_name)
            c_row.append(style.rank)
            c_row.append(style.skills[0].name)
            c_row.append(style.skills[1].name)
            c_row.append(style.skills[2].name)
            c_row.append(style.abilities[0].name)
            c_row.append(style.abilities[1].name)
            c_row.append(style.abilities[2].name)
            # base stat data
            c_row.append(style.base_str_bonus)
            c_row.append(style.base_end_bonus)
            c_row.append(style.base_dex_bonus)
            c_row.append(style.base_agi_bonus)
            c_row.append(style.base_int_bonus)
            c_row.append(style.base_wil_bonus)
            c_row.append(style.base_lov_bonus)
            c_row.append(style.base_cha_bonus)
            # style stat data
            c_row.append(style.level_50_str_mod)
            c_row.append(style.str_bonus)
            c_row.append(style.level_50_end_mod)
            c_row.append(style.end_bonus)
            c_row.append(style.level_50_dex_mod)
            c_row.append(style.dex_bonus)
            c_row.append(style.level_50_agi_mod)
            c_row.append(style.agi_bonus)
            c_row.append(style.level_50_int_mod)
            c_row.append(style.int_bonus)
            c_row.append(style.level_50_wil_mod)
            c_row.append(style.wil_bonus)
            c_row.append(style.level_50_lov_mod)
            c_row.append(style.lov_bonus)
            c_row.append(style.level_50_cha_mod)
            c_row.append(style.cha_bonus)
            rows.append(c_row)
    style_data_sheet.update(cell_range, rows)


if __name__ == '__main__':
    update_style_data()

