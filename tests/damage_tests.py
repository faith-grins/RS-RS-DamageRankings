from data.model import Character, Equipment, Common
from data import load_styles


def test_fire_feather():
    print('Fire Feather test starting...')
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
    print('  {0}'.format(damage_values))
    test_pass = damage_values == [4516, 4551, 4586, 4620, 4655, 4690, 4725, 4759, 4794, 4829]
    print('PASS' if test_pass else 'FAIL')


def test_vortex_breaker():
    print('Vortext Breaker test starting...')
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
    print('  {0}'.format(damage_values))
    test_pass = damage_values == [53705, 54079, 54453, 54828, 55202, 55576, 55950, 56325, 56699, 57073]
    print('PASS' if test_pass else 'FAIL')


def test_luna_fulgur():
    print('Luna Fulgur test starting...')
    json_character = {'name': 'Madeleine', 'id': '00001'}
    maddie = Character.Character(json_character)
    styles = load_styles()
    maddie.add_styles(styles)
    maddie.update_base_stats(123)
    selected_style = [style for style in maddie.styles if style.style_name == '[Two Khamsins]'][0]
    # not at level 50, yet
    selected_style.str_bonus = 8
    selected_style.level_50_str_mod = 94.72 + 20
    # set cap manually
    maddie.max_base_str_value = 10
    selected_skill = [skill for skill in selected_style.skills if skill.name == 'Luna Fulgur'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 18
    weapon = Equipment.Weapon("Khamsin")
    weapon.max_wp = 41
    weapon.type = Common.WeaponType.Sword
    formation = Common.FormationBonus()
    formation.str = 50
    skill_rank = 62
    enemy_end = 213
    enemy_will = 213
    mastery_rank = 41
    enemy_resist = 0
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 15
    test_pass = False
    for skill_power in range(35, 45):
        selected_skill.power_number = skill_power
        damage_values = maddie.attack(selected_style, selected_skill, skill_rank, weapon, formation, equips,
                                      mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                      weapon_stone)
        if all([v in damage_values for v in {25147, 25702, 26256, 26072, 26626, 25575}]):
            print('  Exact match:  SkillPower={0}'.format(skill_power))
            print('  {0}'.format(damage_values))
            test_pass = True
    print('PASS' if test_pass else 'FAIL')


def test_doll_dance():
    print('Destruction Doll Dance test starting...')
    json_character = {'name': 'Coppelia', 'id': '00001'}
    coppy = Character.Character(json_character)
    styles = load_styles()
    coppy.add_styles(styles)
    coppy.update_base_stats(123)
    # currently overcapped on STR and AGI
    coppy.max_base_str_value += 2
    coppy.max_base_agi_value += 1
    selected_style = [style for style in coppy.styles if style.style_name == '[Careful Preparations]'][0]
    selected_skill = [skill for style in coppy.styles for skill in style.skills if skill.name == 'Destruction Doll Dance'][0]
    skill_rank = 99
    equips = Equipment.EquipmentBonus()
    equips.str = 11
    equips.agi = 21
    weapon = Equipment.Weapon("Cat's Claws")
    weapon.max_wp = 45
    weapon.type = Common.WeaponType.Fist
    mastery = 41
    formation = Common.FormationBonus()
    formation.agi = 50
    enemy_wil = 81
    enemy_resist = 30
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 20
    test_pass = False
    for end_value in range(100, 400):
        test_values = {35121, 36507}
        damage_values = coppy.attack(selected_style, selected_skill, skill_rank, weapon, formation, equips, mastery,
                                     end_value, enemy_wil, enemy_resist, turn_number, full_hp, weapon_stone)
        if all([v in damage_values for v in test_values]):
            print('  Exact match:  END={0}'.format(end_value))
            print('  {0}'.format(damage_values))
            test_pass = True
    print('PASS' if test_pass else 'FAIL')


def find_skill_power(character_name, style_name, skill_name, skill_rank, mastery_level, mainstat1, mainstat2,
                     enemy_resist, expected_values):
    """
    function to determine the skill power of a new skill.  assumes style level 50, no equipment, no formation, and that you are attacking the Kaiser Ants in Forest of Mystery 10
    :param character_name:  the name of the character being tested
    :param style_name:  the name of the style being used for the test
    :param skill_name:  the name of the skill being tested
    :param skill_rank:  the rank of the skill being tested
    :param mastery_level:  your mastery level for the skill type being tested
    :param mainstat1:  primary main stat for the skill in question.  (E.g.:  AGI for M. Arts, INT for spells, etc.)
    :param mainstat2:  primary main stat for the skill in question.  (STR for M. Arts.  None for all else)
    :param enemy_resist:  the appropriate resistance for the skill elements being used
    :param expected_values:  an iterable of at least two distinct damage values.  (More is better; one is insufficient)
    :return:  the power number of the skill being tested if found, else None
    """
    print('{0} test starting...'.format(skill_name))
    json_character = {'name': character_name, 'id': '00001'}
    test_character = Character.Character(json_character)
    styles = load_styles()
    test_character.add_styles(styles)
    selected_style = [style for style in test_character.styles if style.style_name == style_name][0]
    selected_skill = [skill for skill in selected_style.skills if skill.name == skill_name][0]
    # set stats
    test_character.update_base_stats(10)
    if selected_skill.weapon_type == Common.WeaponType.Fist:
        test_character.max_base_agi_value = mainstat1 - 10
        test_character.max_base_str_value = mainstat2 - 10
    if selected_skill.weapon_type in (Common.WeaponType.IntFist, Common.WeaponType.Spell):
        test_character.max_base_int_value = mainstat1 - 10
    if selected_skill.weapon_type in (Common.WeaponType.Bow, Common.WeaponType.Epee, Common.WeaponType.Gun):
        test_character.max_base_dex_value = mainstat1 - 10
    else:
        test_character.max_base_str_value = mainstat1 - 10
    equips = Equipment.EquipmentBonus()
    weapon = Equipment.Weapon("testWeapon")
    weapon.type = selected_skill.weapon_type
    formation = Common.FormationBonus()
    enemy_end = 85
    enemy_will = 81
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 0
    test_pass = False
    for skill_power in range(5, 99):
        selected_skill.power_number = skill_power
        damage_values = test_character.attack(selected_style, selected_skill, skill_rank, weapon, formation, equips,
                        mastery_level, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                        weapon_stone)
        if all([v in damage_values for v in expected_values]):
            print('  Exact match:  SkillPower={0}'.format(skill_power))
            print('  {0}'.format(damage_values))
            test_pass = True
    print('PASS' if test_pass else 'FAIL')


if __name__ == '__main__':
    test_fire_feather()
    test_vortex_breaker()
    test_luna_fulgur()
    test_doll_dance()
