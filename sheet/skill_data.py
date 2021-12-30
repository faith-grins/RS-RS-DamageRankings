from data.model.Common import WeaponType


tab_name = 'SkillData'


def write_skills_data(authentication, sheet_id, skills_list):
    skill_names = [s for s in {skill.name for skill in skills_list if skill.power_number != '-' and int(skill.power_number) > 0}]
    skill_names.sort()
    damage_sheet = authentication.open_by_key(sheet_id)
    skill_tab = damage_sheet.worksheet(tab_name)
    header_row = ['SkillName', 'WeaponType', 'MaxBP', 'MinBP', 'SkillRank', 'SkillPower', 'DamageType1', 'DamageType2', 'Spell?']
    sheet_range = skill_tab.range(1, 1, len(skills_list), len(header_row))
    cell_number = 0
    for header in header_row:
        sheet_range[cell_number].value = header
        cell_number += 1
    row = 1
    for name in skill_names:
        matching_skills = [s for s in skills_list if s.name == name if s.power_number != '-' and int(s.power_number) > 0]
        for skill in matching_skills:
            row += 1
            is_spell = skill.weapon_type == WeaponType.Spell
            attack_type = skill.magic_type.name if is_spell else skill.weapon_type.name
            print(f'Setting data for row {row}:  {name} ({attack_type})')
            row_values = [name, attack_type, skill.bp_cost, skill.bp_cost - skill.awakens, skill.power_rank, skill.power_number, skill.damage_types[0].name]
            if len(skill.damage_types) == 2:
                row_values.append(skill.damage_types[1].name)
            else:
                row_values.append(None)
            row_values.append('Y' if is_spell else 'N')
            for value in row_values:
                sheet_range[cell_number].value = value
                cell_number += 1
    print('Updating sheet...')
    skill_tab.update_cells(sheet_range, value_input_option='USER_ENTERED')
    print('Sheet successfully updated!')

