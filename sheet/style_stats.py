from data.model.Common import WeaponType, str_weapon_types, dex_weapon_types, agi_weapon_types, int_weapon_types


sheet_name = 'StyleStats'


def write_stats_data(authentication, sheet_id, styles, characters):
    character_names = [c for c in {character.name for character in characters}]
    character_names.sort()
    damage_sheet = authentication.open_by_key(sheet_id)
    style_sheet = damage_sheet.worksheet(sheet_name)
    sheet_range = style_sheet.range(4, 1, len(styles) + 4, 28)
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
            row_values.append(name)
            row_values.append(style.character_name if style.character_name != name else '')
            row_values.append(style.style_name)
            # Base stats
            row_values.append(f'=$D$2+{style.base_str_bonus}')
            row_values.append(f'=$D$2+{style.base_end_bonus}')
            row_values.append(f'=$D$2+{style.base_dex_bonus}')
            row_values.append(f'=$D$2+{style.base_agi_bonus}')
            row_values.append(f'=$D$2+{style.base_int_bonus}')
            row_values.append(f'=$D$2+{style.base_wil_bonus}')
            row_values.append(f'=$D$2+{style.base_lov_bonus}')
            row_values.append(f'=$D$2+{style.base_cha_bonus}')
            # Style adjusted stats
            row_values.append(f'=FLOOR(MAX($E{character_first_row}:$E{character_last_row})*(1+{style.level_50_str_mod}/100))+{style.str_bonus}')
            row_values.append(f'=FLOOR(MAX($F{character_first_row}:$F{character_last_row})*(1+{style.level_50_end_mod}/100))+{style.end_bonus}')
            row_values.append(f'=FLOOR(MAX($G{character_first_row}:$G{character_last_row})*(1+{style.level_50_dex_mod}/100))+{style.dex_bonus}')
            row_values.append(f'=FLOOR(MAX($H{character_first_row}:$H{character_last_row})*(1+{style.level_50_agi_mod}/100))+{style.agi_bonus}')
            row_values.append(f'=FLOOR(MAX($I{character_first_row}:$I{character_last_row})*(1+{style.level_50_int_mod}/100))+{style.int_bonus}')
            row_values.append(f'=FLOOR(MAX($J{character_first_row}:$J{character_last_row})*(1+{style.level_50_wil_mod}/100))+{style.wil_bonus}')
            row_values.append(f'=FLOOR(MAX($K{character_first_row}:$K{character_last_row})*(1+{style.level_50_lov_mod}/100))+{style.lov_bonus}')
            row_values.append(f'=FLOOR(MAX($L{character_first_row}:$L{character_last_row})*(1+{style.level_50_cha_mod}/100))+{style.cha_bonus}')
            # Formation Final Stats
            str_bonus = 5 if style.weapon_type in str_weapon_types else 0
            dex_bonus = 5 if style.weapon_type in dex_weapon_types else 0
            agi_bonus = 5 if style.weapon_type in agi_weapon_types else 0
            int_preferred = style.weapon_type in int_weapon_types or len([skill for skill in style.skills if skill.weapon_type == WeaponType.Spell]) > 1
            int_bonus = 5 if int_preferred else 0
            row_values.append('')
            row_values.append('')
            row_values.append('')
            row_values.append('')
            row_values.append('')
            row_values.append('')
            row_values.append('')
            row_values.append('')
            for value in row_values:
                cell_number += 1
                sheet_range[cell_number].value = value
    print('Updating sheet...')
    style_sheet.update_cells(sheet_range, value_input_option='USER_ENTERED')
    print('Sheet successfully updated!')
