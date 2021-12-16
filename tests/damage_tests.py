from data.model import Character, Equipment, Common
from data import load_styles


def test_fire_feather():
    json_character = {'name': 'Polka Lynn Wood', 'id': '00001'}
    polka = Character.Character(json_character)
    styles = load_styles()
    polka.add_styles(styles)
    polka.update_base_stats(117)
    selected_style = [style for style in polka.styles if style.style_name == '[Inherited Shucho Arts]'][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Fire Feather'][0]
    equips = Equipment.EquipmentBonus()
    weapon = Equipment.Weapon("Sword")
    weapon.max_wp = 0
    weapon.type = Common.WeaponType.Sword
    damage_values = polka.attack(selected_style, selected_skill, weapon, 0, equips, 41, 85, 81, 0, 1, True)
    print(damage_values)
    print(damage_values == [4516, 4551, 4586, 4620, 4655, 4690, 4725, 4759, 4794, 4829])


def test_vortex_breaker():
    json_character = {'name': 'Valdor', 'id': '00001'}
    valdor = Character.Character(json_character)
    styles = load_styles()
    valdor.add_styles(styles)
    valdor.update_base_stats(160)
    selected_style = [style for style in valdor.styles if style.style_name == '[Fruits of My Training]'][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Vortex Breaker'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 17
    equips.agi = 32
    weapon = Equipment.Weapon("Cat's Claws")
    weapon.max_wp = 45
    weapon.type = Common.WeaponType.Fist
    damage_values = valdor.attack(selected_style, selected_skill, weapon, 0, equips, 35, 85, 81, -35, 1, True)
    print(damage_values)


if __name__ == '__main__':
    test_vortex_breaker()
    # test_fire_feather()

