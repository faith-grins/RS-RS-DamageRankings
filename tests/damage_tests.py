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
    test_pass = False
    for str_mod in [x / 100 for x in range(9472, 13000)]:
        selected_style.level_50_str_mod = str_mod
        # set cap manually
        maddie.max_base_str_value = 10
        selected_skill = [skill for skill in selected_style.skills if skill.name == 'Luna Fulgur'][0]
        equips = Equipment.EquipmentBonus()
        weapon = Equipment.Weapon("Khamsin")
        weapon.type = Common.WeaponType.Sword
        formation = Common.FormationBonus()
        skill_rank = 96
        enemy_end = 85
        enemy_will = 81
        mastery_rank = 41
        enemy_resist = 0
        turn_number = 1
        full_hp = turn_number == 1
        weapon_stone = 0
        for skill_power in range(35, 45):
            selected_skill.power_number = skill_power
            damage_values = maddie.attack(selected_style, selected_skill, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
            if all([v in damage_values for v in {13895, 14464, 14123}]):
                print('  Exact match:  SkillPower={0}, StrMod={1}'.format(skill_power, str_mod))
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
    test_character.update_base_stats(1)
    if selected_skill.weapon_type == Common.WeaponType.Fist:
        test_character.max_base_agi_value = mainstat1 - 9
        test_character.max_base_str_value = mainstat2 - 9
        selected_style.level_50_str_mod = 0
        selected_style.level_50_agi_mod = 0
        selected_style.str_bonus = 0
        selected_style.agi_bonus = 0
    if selected_skill.weapon_type in (Common.WeaponType.IntFist, Common.WeaponType.Spell):
        test_character.max_base_int_value = mainstat1 - 9
        selected_style.level_50_int_mod = 0
        selected_style.int_bonus = 0
    if selected_skill.weapon_type in (Common.WeaponType.Bow, Common.WeaponType.Epee, Common.WeaponType.Gun):
        test_character.max_base_dex_value = mainstat1 - 9
        selected_style.level_50_dex_mod = 0
        selected_style.dex_bonus = 0
    else:
        test_character.max_base_str_value = mainstat1 - 9
        selected_style.level_50_str_mod = 0
        selected_style.str_bonus = 0
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
    for skill_power in range(6, 99):
        selected_skill.power_number = skill_power
        damage_values = test_character.attack(selected_style, selected_skill, skill_rank, weapon, formation, equips,
                        mastery_level, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                        weapon_stone)
        if all([v in damage_values for v in expected_values]):
            print('  Exact match:  SkillPower={0}'.format(skill_power))
            print('  {0}'.format(damage_values))
            test_pass = True
    print('PASS' if test_pass else 'FAIL')


def luna_fulgur_v_cross_break():
    json_character = {'name': 'Madeleine', 'id': '00001'}
    maddie = Character.Character(json_character)
    styles = load_styles()
    maddie.add_styles(styles)
    maddie.update_base_stats(124)
    selected_style = [style for style in maddie.styles if style.style_name == '[Two Khamsins]'][0]
    luna_fulgur = [skill for skill in selected_style.skills if skill.name == 'Luna Fulgur'][0]
    demilune = [skill for style in maddie.styles for skill in style.skills if skill.name == 'Demilune Echo'][0]
    equips = Equipment.EquipmentBonus()
    equips.str = 18
    weapon = Equipment.Weapon("Khamsin")
    weapon.type = Common.WeaponType.Sword
    weapon.max_wp = 41
    formation = Common.FormationBonus()
    formation.str = 50
    skill_rank = 99
    enemy_end = 213
    enemy_will = 213
    mastery_rank = 41
    enemy_resist = 0
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 15
    luna_fulgur.power_number = 43
    initial_str = selected_style.level_50_str_mod
    maddie_attack1 = maddie.attack(selected_style, luna_fulgur, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    str_buff = 15
    selected_style.level_50_str_mod = initial_str + str_buff
    maddie_attack2 = maddie.attack(selected_style, demilune, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    str_buff += 15
    str_buff *= 0.75
    selected_style.level_50_str_mod = initial_str + str_buff
    maddie_attack3 = maddie.attack(selected_style, luna_fulgur, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    str_buff += 15
    selected_style.level_50_str_mod = initial_str + str_buff
    maddie_attack4 = maddie.attack(selected_style, demilune, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    json_character = {'name': 'Urpina', 'id': '00002'}
    urpina = Character.Character(json_character)
    urpina.add_styles(styles)
    urpina.update_base_stats(124)
    selected_style = [style for style in urpina.styles if style.style_name == "[Now That's Dual Wielding!]"][0]
    cross_break = [skill for skill in selected_style.skills if skill.name == 'Cross Break'][0]
    cross_break.power_number = 50
    sword_breath = [skill for skill in selected_style.skills if skill.name == 'Sword Breath'][0]
    sword_breath.power_number = 10
    selected_style.level_50_str_mod = 100
    selected_style.str_bonus = 13
    selected_style.abilities[0] = selected_style.abilities[2]
    weapon_stone = 20
    urpina_attack1 = urpina.attack(selected_style, cross_break, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    urpina_attack2 = urpina.attack(selected_style, sword_breath, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    urpina_attack3 = urpina.attack(selected_style, cross_break, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    urpina_attack4 = urpina.attack(selected_style, sword_breath, skill_rank, weapon, formation, equips,
                                   mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                   weapon_stone)
    maddie_damage = (sum(maddie_attack1) + sum(maddie_attack2) + sum(maddie_attack3) + sum(maddie_attack4)) / 10
    urpina_damage = (sum(urpina_attack1) + sum(urpina_attack2) + sum(urpina_attack3) + sum(urpina_attack4)) / 10
    print(maddie_damage)
    print(urpina_damage)


def test_cross_break():
    print('Cross Break test starting...')
    cross_break = {17456, 16544, 16674, 16935, 17195, 17325, 17065, 16804, 16414, 16283}
    sword_breath = {2346, 2365}
    find_skill_power('Urpina', "[Now That's Dual Wielding!]", 'Cross Break', 99, 41, 265, 0, 0, cross_break)
    # print('PASS' if test_pass else 'FAIL')


def lunar_blade_vs_urps():
    styles = load_styles()
    # constants
    equips = Equipment.EquipmentBonus()
    equips.str = 18
    weapon = Equipment.Weapon("Death Sword")
    weapon.type = Common.WeaponType.Greatsword
    weapon.max_wp = 45
    formation = Common.FormationBonus()
    formation.str = 50
    skill_rank = 99
    enemy_end = 213
    enemy_will = 213
    mastery_rank = 41
    enemy_resist = -35
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 20
    # Silver
    json_character = {'name': 'Silver', 'id': '00001'}
    silver = Character.Character(json_character)
    silver.add_styles(styles)
    silver.update_base_stats(125)
    selected_style = [style for style in silver.styles if style.style_name == '[Silver-Style Test of Guts]'][0]
    storm_roar = [skill for skill in selected_style.skills if skill.name == 'Storm Roar'][0]
    silver_attack = silver.attack(selected_style, storm_roar, skill_rank, weapon, formation, equips,
                                   mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                   weapon_stone)
    # Urps
    json_character = {'name': 'Urpina', 'id': '00002'}
    urpina = Character.Character(json_character)
    urpina.add_styles(styles)
    urpina.update_base_stats(125)
    selected_style = [style for style in urpina.styles if style.style_name == "[Now That's Dual Wielding!]"][0]
    cross_break = [skill for skill in selected_style.skills if skill.name == 'Cross Break'][0]
    cross_break.power_number = 28
    selected_style.level_50_str_mod = 100
    selected_style.str_bonus = 13
    selected_style.abilities[0] = selected_style.abilities[2]
    urpina_attack = urpina.attack(selected_style, cross_break, skill_rank, weapon, formation, equips,
                                   mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                   weapon_stone)
    cross_break.power_number = 36
    dual_whirlwind_attack = urpina.attack(selected_style, cross_break, skill_rank, weapon, formation, equips,
                                   mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                   weapon_stone)
    # Fancy Lass
    json_character = {'name': 'Final Empress', 'id': '00003'}
    fancy_lass = Character.Character(json_character)
    fancy_lass.add_styles(styles)
    fancy_lass.update_base_stats(125)
    selected_style = [style for style in fancy_lass.styles if style.style_name == "[One Special Summer Day]"][0]
    lunar_blade = [skill for style in fancy_lass.styles for skill in style.skills if skill.name == 'Lunar Blade'][0]
    fancy_lass_attack = fancy_lass.attack(selected_style, lunar_blade, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)
    elegant_sands = [skill for skill in selected_style.skills if skill.name == 'Elegant Sands'][0]
    elegant_sands_attack = fancy_lass.attack(selected_style, elegant_sands, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
    # Fancy Lad
    json_character = {'name': 'Final Emperor', 'id': '00003'}
    fancy_lad = Character.Character(json_character)
    fancy_lad.add_styles(styles)
    fancy_lad.update_base_stats(125)
    selected_style = [style for style in fancy_lad.styles if style.style_name == "[At the Victory Banquet]"][0]
    imperial_sword = [skill for style in fancy_lad.styles for skill in style.skills if skill.name == 'Imperial Sword'][0]
    imperial_sword.power_number = 28
    imperial_sword_attack = fancy_lad.attack(selected_style, imperial_sword, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
    imperial_sword.power_number = 39
    wheel_swing_attack = fancy_lad.attack(selected_style, imperial_sword, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
    # Noel
    json_character = {'name': 'Noel', 'id': '00003'}
    noel = Character.Character(json_character)
    noel.add_styles(styles)
    noel.update_base_stats(125)
    selected_style = [style for style in noel.styles if style.style_name == "[Fallen Hero]"][0]
    steel_wave = [skill for style in noel.styles for skill in style.skills if skill.name == 'Steel Wave'][0]
    steel_wave_attack = noel.attack(selected_style, steel_wave, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
    # Gustave
    json_character = {'name': 'Gustave', 'id': '00003'}
    gustave = Character.Character(json_character)
    gustave.add_styles(styles)
    gustave.update_base_stats(125)
    selected_style = [style for style in gustave.styles if style.style_name == "[Leading the Steel Forces]"][0]
    gustave_attack = gustave.attack(selected_style, steel_wave, skill_rank, weapon, formation, equips,
                                          mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                          weapon_stone)
    silver_damage = sum(silver_attack) // 10
    urpina_damage = sum(urpina_attack) // 10
    dual_whirlwind_damage = sum(dual_whirlwind_attack) // 10
    fancy_lass_damage = sum(fancy_lass_attack) // 10
    elegant_sands_damage = sum(elegant_sands_attack) // 10
    imperial_sword_damage = sum(imperial_sword_attack) // 10
    wheel_swing_damage = sum(wheel_swing_attack) // 10
    steel_wave_damage = sum(steel_wave_attack) // 10
    gustave_damage = sum(gustave_attack) // 10
    print(f'Storm Roar:  {silver_damage}')
    print(f'Holy Shining Sword:  {urpina_damage}')
    print(f'Dual Whirlwind:  {dual_whirlwind_damage}')
    print(f'Lunar Blade+:  {fancy_lass_damage}')
    print(f'Elegant Sands:  {elegant_sands_damage}')
    print(f'Imperial Sword:  {imperial_sword_damage}')
    print(f'Wheel Swing+:  {wheel_swing_damage}')
    print(f'Steel Wave (Noel):  {steel_wave_damage}')
    print(f'Steel Wave (Gustave):  {gustave_damage}')


def test_shining_holy_sword():
    shining_sword = {7025, 6750, 6704, 6842}
    find_skill_power('Urpina', "[I'm Ready]", 'Holy Shining Sword', 6, 41, 221, 0, 0, shining_sword)


def georg_test():
    styles = load_styles()
    json_character = {'name': 'Georg', 'id': '00003'}
    georg = Character.Character(json_character)
    georg.add_styles(styles)
    georg.update_base_stats(125)
    ss_style = [style for style in georg.styles if style.style_name == "[Burden of Royalty]"][0]
    final_strike = [skill for skill in ss_style.skills if skill.name == 'Final Strike'][0]
    final_strike.power_number = 39
    equips = Equipment.EquipmentBonus()
    equips.str = 18
    weapon = Equipment.Weapon("Khamsin")
    weapon.type = Common.WeaponType.Greatsword
    weapon.max_wp = 45
    formation = Common.FormationBonus()
    formation.str = 50
    skill_rank = 99
    enemy_end = 213
    enemy_will = 213
    mastery_rank = 41
    enemy_resist = -35
    turn_number = 1
    full_hp = turn_number == 1
    weapon_stone = 20
    final_strike_attack = sum(georg.attack(ss_style, final_strike, skill_rank, weapon, formation, equips,
                                  mastery_rank, enemy_end, enemy_will, enemy_resist, turn_number, full_hp,
                                  weapon_stone)) // 10
    print(f'Final Strike: {final_strike_attack}')


if __name__ == '__main__':
    test_fire_feather()
    test_vortex_breaker()
    test_luna_fulgur()
    test_doll_dance()
    luna_fulgur_v_cross_break()
    test_cross_break()
    test_shining_holy_sword()
    lunar_blade_vs_urps()
    georg_test()
