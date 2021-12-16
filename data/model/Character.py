from .Common import WeaponType


class Character:
    def __init__(self, json_object):
        self.name = json_object['name']
        self.id = json_object['id']
        self.styles = []
        self.max_base_str_value = 0
        self.max_base_end_value = 0
        self.max_base_dex_value = 0
        self.max_base_agi_value = 0
        self.max_base_int_value = 0
        self.max_base_wil_value = 0
        self.max_base_lov_value = 0
        self.max_base_cha_value = 0
        self.base_stat_cap = 0

    def update_base_stats(self, stat_cap):
        self.base_stat_cap = stat_cap
        for style in self.styles:
            if style.str_bonus > self.max_base_str_value:
                self.max_base_str_value = style.str_bonus
            if style.end_bonus > self.max_base_end_value:
                self.max_base_end_value = style.end_bonus
            if style.dex_bonus > self.max_base_dex_value:
                self.max_base_dex_value = style.dex_bonus
            if style.agi_bonus > self.max_base_agi_value:
                self.max_base_agi_value = style.agi_bonus
            if style.int_bonus > self.max_base_int_value:
                self.max_base_int_value = style.int_bonus
            if style.wil_bonus > self.max_base_wil_value:
                self.max_base_wil_value = style.wil_bonus
            if style.lov_bonus > self.max_base_lov_value:
                self.max_base_lov_value = style.lov_bonus
            if style.cha_bonus > self.max_base_cha_value:
                self.max_base_cha_value = style.cha_bonus

    def add_styles(self, styles_list):
        for style in styles_list:
            if style.character_name == self.name:
                self.styles.append(style)

    def attack(self, style, skill, weapon, formation_boost, equipment_mods, mastery_level,
               enemy_end, enemy_wil, enemy_resist, turn_number, full_hp):
        rank = 99
        skill_power = skill.power_number
        rank_modifier = (skill_power - 5) * (100 + rank) / 100
        final_str = int((self.base_stat_cap + self.max_base_str_value) * (100 + style.level_50_str_mod +
                        formation_boost) / 100 + style.str_bonus + equipment_mods.str)
        final_agi = int((self.base_stat_cap + self.max_base_agi_value) * (100 + style.level_50_agi_mod +
                        formation_boost) / 100 + style.agi_bonus + equipment_mods.agi)
        final_dex = int((self.base_stat_cap + self.max_base_dex_value) * (100 + style.level_50_dex_mod +
                        formation_boost) / 100 + style.dex_bonus + equipment_mods.dex)
        final_int = int((self.base_stat_cap + self.max_base_int_value) * (100 + style.level_50_int_mod +
                        formation_boost) / 100 + style.int_bonus + equipment_mods.int)
        if skill.weapon_type == WeaponType.Fist:
            stat_factor = 1 + 2 * final_str + 2.5 * final_agi - 1.2 * enemy_end
            weapon_factor = weapon.max_wp
        elif skill.weapon_type == WeaponType.Gun:
            stat_factor = 1 + 3.6 * final_dex - 1.25 * enemy_end
            weapon_factor = 1.9 * weapon.max_wp
        else:
            weapon_factor = 1.5 * weapon.max_wp
            if skill.weapon_type == WeaponType.Spell:
                stat_factor = 1 + 4 * final_int - 1.5 * enemy_wil
            elif skill.weapon_type == WeaponType.IntFist:
                stat_factor = 1 + 4 * final_int - 1.5 * enemy_end
            elif skill.weapon_type in (WeaponType.Bow, WeaponType.Epee):
                stat_factor = 1 + 4 * final_dex - 1.5 * enemy_end
            else:
                stat_factor = 1 + 4 * final_str - 1.5 * enemy_end
        resist_factor = 1 / (1 + 0.008 * enemy_resist)
        weak_point = enemy_resist <= -35
        ability_factor = sum([a.damage_increase(skill.damage_types, turn_number, full_hp, weak_point)
                              for a in style.abilities])
        mastery_factor = round((mastery_level - 1) / 2) * 0.5
        random_factors = range(1, 11)
        damage_values = []
        for r in random_factors:
            random_factor = 1 + (ability_factor + mastery_factor + r - 6) / 100
            technique_factor = weapon_factor + skill_power + rank_modifier
            damage = technique_factor * stat_factor * resist_factor * random_factor / 10
            damage_values.append(int(damage))
        # return int(sum(damage_values) / len(damage_values))
        return damage_values


def get_characters(character_filename, styles_list):
    from json import load
    with open(character_filename, 'r') as character_file:
        character_json_list = load(character_file)
    character_list = []
    for json_character in character_json_list:
        character = Character(json_character)
        character.add_styles(styles_list)
        character_list.append(character)
    return character_list
