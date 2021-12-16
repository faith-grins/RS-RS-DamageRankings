from data.model import Character, Equipment, Common
from data import load_styles


def test_fire_feather():
    json_character = {'name': 'Polka Lynn Wood', 'id': '00001'}
    polka = Character.Character(json_character)
    styles = load_styles()
    polka.add_styles(styles)
    polka.update_base_stats(122)
    selected_style = [style for style in polka.styles if style.style_name == '[Inherited Shucho Arts]'][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Fire Feather'][0]
    equips = Equipment.EquipmentBonus()
    weapon = Equipment.Weapon("Sword")
    weapon.max_wp = 0
    weapon.type = Common.WeaponType.Sword
    formation = Common.FormationBonus()
    damage_values = polka.attack(selected_style, selected_skill, 99, weapon, formation, equips, 41, 85, 81, 0, 1, True, 0)
    print(damage_values)
    print(damage_values == [4516, 4551, 4586, 4620, 4655, 4690, 4725, 4759, 4794, 4829])


def test_vortex_breaker():
    json_character = {'name': 'Valdor', 'id': '00001'}
    valdor = Character.Character(json_character)
    styles = load_styles()
    valdor.add_styles(styles)
    valdor.update_base_stats(158)
    selected_style = [style for style in valdor.styles if style.style_name == '[Fruits of My Training]'][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Vortex Breaker'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 12
    equips.agi = 14
    weapon = Equipment.Weapon("Cat's Claws")
    weapon.max_wp = 45
    weapon.type = Common.WeaponType.Fist
    formation = Common.FormationBonus()
    damage_values = valdor.attack(selected_style, selected_skill, 99, weapon, formation, equips, 35, 85, 81, -35, 1, True, 0)
    print(damage_values)
    print(damage_values == [53705, 54079, 54453, 54828, 55202, 55576, 55950, 56325, 56699, 57073])


def test_luna_fulgur():
    json_character = {'name': 'Madeleine', 'id': '00001'}
    maddie = Character.Character(json_character)
    styles = load_styles()
    maddie.add_styles(styles)
    maddie.update_base_stats(123)
    selected_style = [style for style in maddie.styles if style.style_name == '[Two Khamsins]'][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Luna Fulgur'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 18
    weapon = Equipment.Weapon("Khamsin")
    weapon.max_wp = 41
    weapon.type = Common.WeaponType.Sword
    formation = Common.FormationBonus()
    formation.str = 50
    for end_value in range(100, 400):
        damage_values = maddie.attack(selected_style, selected_skill, 62, weapon, formation, equips, 41, end_value, 81, 0, 1, True, 15)
        if all([v in damage_values for v in (25147, 25702, 26256, 26072, 26626, 25575)]):
            print(damage_values)
    # print(damage_values)
    # print(damage_values == [53705, 54079, 54453, 54828, 55202, 55576, 55950, 56325, 56699, 57073])


def test_doll_dance():
    json_character = {'name': 'Coppelia', 'id': '00001'}
    coppy = Character.Character(json_character)
    styles = load_styles()
    coppy.add_styles(styles)
    coppy.update_base_stats(123)
    # currently undercapped on STR and overcapped on AGI
    coppy.max_base_str_value -= 1
    coppy.max_base_agi_value += 1
    selected_style = [style for style in coppy.styles if style.style_name == '[Careful Preparations]'][0]
    selected_skill = [skill for style in coppy.styles for skill in style.skills if skill.name == 'Destruction Doll Dance'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 11
    equips.agi = 21
    weapon = Equipment.Weapon("Cat's Claws")
    weapon.max_wp = 45
    weapon.type = Common.WeaponType.Fist
    formation = Common.FormationBonus()
    formation.agi = 50
    for end_value in range(100, 400):
        damage_values = coppy.attack(selected_style, selected_skill, 99, weapon, formation, equips, 41, end_value, 81, 0, 1, True, 15)
        if all([v in damage_values for v in {35294, 35523, 35752}]):
            print(damage_values)
    # print(damage_values)
    # print(damage_values == [53705, 54079, 54453, 54828, 55202, 55576, 55950, 56325, 56699, 57073])


if __name__ == '__main__':
    # test_vortex_breaker()
    # test_fire_feather()
    # test_luna_fulgur()
    test_doll_dance()
