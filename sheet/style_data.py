sheet_name = 'StyleData'
header_row = ['Character', 'Style Name', 'Rank', 'Skill1', 'Skill2', 'Skill3', 'Ability1', 'Ability2', 'Ability3', 'BaseStrMod', 'BaseEndMod', 'BaseDexMod', 'BaseAgiMod', 'BaseIntMod', 'BaseWilMod', 'BaseLovMod', 'BaseChaMod', 'Style%STR', 'Style+STR', 'Style%END', 'Style+END', 'Style%DEX', 'Style+DEX', 'Style%AGI', 'Style+AGI', 'Style%INT', 'Style+INT', 'Style%WIL', 'Style+WIL', 'Style%LOV', 'Style+LOV', 'Style%CHA', 'Style+CHA']


def write_style_data(authentication, sheet_id, styles, characters):
    character_names = [c for c in {character.name for character in characters}]
    character_names.sort()
    row_len = len(header_row)
    damage_sheet = authentication.open_by_key(sheet_id)
    style_sheet = damage_sheet.worksheet(sheet_name)
    sheet_range = style_sheet.range(1, 1, len(styles) + 1, len(header_row))
    for i, header in enumerate(header_row):
        sheet_range[i].value = header
    cell_number = row_len - 1
    row = 1
    for name in character_names:
        character_styles = [style for character in characters if character.name == name for style in character.styles]
        for style in character_styles:
            row += 1
            print(f'Setting data for row {row}:  {name} {style.style_name}')
            cell_number += 1
            sheet_range[cell_number].value = name
            cell_number += 1
            sheet_range[cell_number].value = style.style_name
            cell_number += 1
            sheet_range[cell_number].value = style.rank
            cell_number += 1
            sheet_range[cell_number].value = style.skills[0].name
            cell_number += 1
            sheet_range[cell_number].value = style.skills[1].name
            cell_number += 1
            sheet_range[cell_number].value = style.skills[2].name
            cell_number += 1
            sheet_range[cell_number].value = style.abilities[0].name
            cell_number += 1
            sheet_range[cell_number].value = style.abilities[1].name
            cell_number += 1
            sheet_range[cell_number].value = style.abilities[2].name
            cell_number += 1
            sheet_range[cell_number].value = style.base_str_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_end_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_dex_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_agi_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_int_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_wil_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_lov_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.base_cha_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_str_mod
            cell_number += 1
            sheet_range[cell_number].value = style.str_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_end_mod
            cell_number += 1
            sheet_range[cell_number].value = style.end_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_dex_mod
            cell_number += 1
            sheet_range[cell_number].value = style.dex_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_agi_mod
            cell_number += 1
            sheet_range[cell_number].value = style.agi_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_int_mod
            cell_number += 1
            sheet_range[cell_number].value = style.int_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_wil_mod
            cell_number += 1
            sheet_range[cell_number].value = style.wil_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_lov_mod
            cell_number += 1
            sheet_range[cell_number].value = style.lov_bonus
            cell_number += 1
            sheet_range[cell_number].value = style.level_50_cha_mod
            cell_number += 1
            sheet_range[cell_number].value = style.cha_bonus
    print('Updating sheet...')
    style_sheet.update_cells(sheet_range)
    print('Sheet successfully updated!')
