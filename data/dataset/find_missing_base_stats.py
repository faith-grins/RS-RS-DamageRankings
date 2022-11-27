from data import load_styles
from csv import writer, DictReader


def write_base_style_stats(filename):
    with open(filename, 'w', newline='') as file_out:
        csv_writer = writer(file_out)
        header = ['Character', 'Style', 'STR', 'END', 'DEX', 'AGI', 'INT', 'WIL', 'LOV', 'CHA']
        csv_writer.writerow(header)
        styles = load_styles()
        for s in styles:
            stats = [s.base_str_bonus, s.base_end_bonus, s.base_dex_bonus,
                     s.base_agi_bonus, s.base_int_bonus, s.base_wil_bonus, s.base_lov_bonus, s.base_cha_bonus]
            if all([s == 0 for s in stats]):
                csv_writer.writerow([s.character_name, s.style_name])


def update_base_style_stats(in_filename):
    with open(in_filename, 'r') as input_file:
        csv_reader = DictReader(input_file)
        dict_styles = [row for row in csv_reader]
        styles = load_styles()
        for s in styles:
            stats = [s.base_str_bonus, s.base_end_bonus, s.base_dex_bonus,
                     s.base_agi_bonus, s.base_int_bonus, s.base_wil_bonus, s.base_lov_bonus, s.base_cha_bonus]
            if all([stat == 0 for stat in stats]):
                matching_style = [style for style in dict_styles if style['Character'] == s.character_name and
                                  style['Style'] == s.style_name][0]
                s.base_str_bonus = int(matching_style['STR'])
                s.base_end_bonus = int(matching_style['END'])
                s.base_dex_bonus = int(matching_style['DEX'])
                s.base_agi_bonus = int(matching_style['AGI'])
                s.base_int_bonus = int(matching_style['INT'])
                s.base_wil_bonus = int(matching_style['WIL'])
                s.base_lov_bonus = int(matching_style['LOV'])
                s.base_cha_bonus = int(matching_style['CHA'])
    return styles


if __name__ == '__main__':
    write_base_style_stats('base_styles_missing_stats3.csv')
