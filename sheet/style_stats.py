from data.model.Common import WeaponType, str_weapon_types, dex_weapon_types, agi_weapon_types, int_weapon_types


sheet_name = 'StyleStats'


def write_stats_data(authentication, sheet_id, styles, characters):
    character_names = [c for c in {character.name for character in characters}]
    character_names.sort()
    damage_sheet = authentication.open_by_key(sheet_id)
    style_sheet = damage_sheet.worksheet(sheet_name)
    sheet_range = style_sheet.range(4, 1, len(styles) + 4, 27)
    cell_number = -1
    header_rows = 2
    row = 1
    for name in character_names:
        character_styles = [style for character in characters if character.name == name for style in character.styles]
        character_first_row = row + header_rows + 1
        character_last_row = row + header_rows + len(character_styles)
        for style in character_styles:
            row += 1
            print(f'Setting data for row {row}:  {name} {style.style_name}')
            row_values = []
            current_row = row + header_rows
            row_values.append(style.rank)
            row_values.append(style.character_name)
            row_values.append(style.style_name)
            # Base stats
            row_values.append(f'=vlookup($C{current_row},StyleData,9,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,10,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,11,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,12,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,13,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,14,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,15,FALSE)+$C$2')
            row_values.append(f'=vlookup($C{current_row},StyleData,16,FALSE)+$C$2')
            # Style adjusted stats
            row_values.append(f'=FLOOR(MAX($D{character_first_row}:$D{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,17,FALSE)/100))+VLOOKUP($C{current_row},StyleData,18,FALSE)')
            row_values.append(f'=FLOOR(MAX($E{character_first_row}:$E{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,19,FALSE)/100))+VLOOKUP($C{current_row},StyleData,20,FALSE)')
            row_values.append(f'=FLOOR(MAX($F{character_first_row}:$F{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,21,FALSE)/100))+VLOOKUP($C{current_row},StyleData,22,FALSE)')
            row_values.append(f'=FLOOR(MAX($G{character_first_row}:$G{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,23,FALSE)/100))+VLOOKUP($C{current_row},StyleData,24,FALSE)')
            row_values.append(f'=FLOOR(MAX($H{character_first_row}:$H{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,25,FALSE)/100))+VLOOKUP($C{current_row},StyleData,26,FALSE)')
            row_values.append(f'=FLOOR(MAX($I{character_first_row}:$I{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,27,FALSE)/100))+VLOOKUP($C{current_row},StyleData,28,FALSE)')
            row_values.append(f'=FLOOR(MAX($J{character_first_row}:$J{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,29,FALSE)/100))+VLOOKUP($C{current_row},StyleData,30,FALSE)')
            row_values.append(f'=FLOOR(MAX($K{character_first_row}:$K{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,31,FALSE)/100))+VLOOKUP($C{current_row},StyleData,32,FALSE)')
            # Formation Final Stats
            str_bonus = 5 if style.weapon_type in str_weapon_types else 0
            dex_bonus = 5 if style.weapon_type in dex_weapon_types else 0
            agi_bonus = 5 if style.weapon_type in agi_weapon_types else 0
            int_preferred = style.weapon_type in int_weapon_types or len([skill for skill in style.skills if skill.weapon_type == WeaponType.Spell]) > 1
            int_bonus = 5 if int_preferred else 0
            row_values.append(f'=FLOOR(MAX($D{character_first_row}:$D{character_last_row})*(1.{str_bonus}+VLOOKUP($C{current_row},StyleData,17,FALSE)/100))+VLOOKUP($C{current_row},StyleData,18,FALSE)')
            row_values.append(f'=FLOOR(MAX($E{character_first_row}:$E{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,19,FALSE)/100))+VLOOKUP($C{current_row},StyleData,20,FALSE)')
            row_values.append(f'=FLOOR(MAX($F{character_first_row}:$F{character_last_row})*(1.{dex_bonus}+VLOOKUP($C{current_row},StyleData,21,FALSE)/100))+VLOOKUP($C{current_row},StyleData,22,FALSE)')
            row_values.append(f'=FLOOR(MAX($G{character_first_row}:$G{character_last_row})*(1.{agi_bonus}+VLOOKUP($C{current_row},StyleData,23,FALSE)/100))+VLOOKUP($C{current_row},StyleData,24,FALSE)')
            row_values.append(f'=FLOOR(MAX($H{character_first_row}:$H{character_last_row})*(1.{int_bonus}+VLOOKUP($C{current_row},StyleData,25,FALSE)/100))+VLOOKUP($C{current_row},StyleData,26,FALSE)')
            row_values.append(f'=FLOOR(MAX($I{character_first_row}:$I{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,27,FALSE)/100))+VLOOKUP($C{current_row},StyleData,28,FALSE)')
            row_values.append(f'=FLOOR(MAX($J{character_first_row}:$J{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,29,FALSE)/100))+VLOOKUP($C{current_row},StyleData,30,FALSE)')
            row_values.append(f'=FLOOR(MAX($K{character_first_row}:$K{character_last_row})*(1+VLOOKUP($C{current_row},StyleData,31,FALSE)/100))+VLOOKUP($C{current_row},StyleData,32,FALSE)')
            for value in row_values:
                cell_number += 1
                sheet_range[cell_number].value = value
    print('Updating sheet...')
    style_sheet.update_cells(sheet_range, value_input_option='USER_ENTERED')
    print('Sheet successfully updated!')
