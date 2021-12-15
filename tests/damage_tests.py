from data.model import Character, Equipment, Common
from data import load_styles


def test_fire_feather():
    json_character = {'name': 'Polka Lyn Wood', 'id': '00001'}
    polka = Character.Character(json_character)
    styles = load_styles()
    polka.add_styles(styles)
    polka.update_base_stats(163)


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
    damage_values = valdor.attack(selected_style, selected_skill, weapon, 0, equips, 35, 85, 85, -35, 1, True)
    print(damage_values)


if __name__ == '__main__':
    test_vortex_breaker()

