from enum import Enum
from .Common import WeaponType


class StyleBonusType(Enum):
    STR = 1
    END = 2
    DEX = 3
    AGI = 4
    INT = 5
    WIL = 6
    LOV = 7
    CHA = 8
    All_Attributes = 9
    Ability1 = 31
    Ability2 = 32
    Ability3 = 33
    Mastery_Level_EXP = 37


class Style:
    def __init__(self, style_json_object):
        self.id = style_json_object['id']
        self.character_name = style_json_object['name']
        self.style_name = style_json_object['another_name']
        self.level_50_str_mod = style_json_object['bonus_rate_max_str'] - 100
        self.level_50_end_mod = style_json_object['bonus_rate_max_end'] - 100
        self.level_50_dex_mod = style_json_object['bonus_rate_max_dex'] - 100
        self.level_50_agi_mod = style_json_object['bonus_rate_max_agi'] - 100
        self.level_50_int_mod = style_json_object['bonus_rate_max_int'] - 100
        self.level_50_wil_mod = style_json_object['bonus_rate_max_wil'] - 100
        self.level_50_lov_mod = style_json_object['bonus_rate_max_lov'] - 100
        self.level_50_cha_mod = style_json_object['bonus_rate_max_cha'] - 100
        self.str_bonus = 0
        self.end_bonus = 0
        self.dex_bonus = 0
        self.agi_bonus = 0
        self.int_bonus = 0
        self.wil_bonus = 0
        self.lov_bonus = 0
        self.cha_bonus = 0
        self.base_str_bonus = 0
        self.base_end_bonus = 0
        self.base_dex_bonus = 0
        self.base_agi_bonus = 0
        self.base_int_bonus = 0
        self.base_wil_bonus = 0
        self.base_lov_bonus = 0
        self.base_cha_bonus = 0
        self.weapon_type = WeaponType(style_json_object['weapon_type'])
        rank = style_json_object['rarity']
        self.rank = 'A' if rank == 3 else 'S' if rank == 4 else 'SS'
        self.skills = []
        self.abilities = []
        self._skill_ids = style_json_object['skill_ids']

    def update_skills(self, skills_list):
        for skill in skills_list:
            if skill.id in self._skill_ids:
                self.skills.append(skill)

    def handle_level_ups(self, level_up_json_list, abilities_list):
        for level_up in level_up_json_list:
            if level_up['style_id'] != self.id:
                continue
            bonus_type = StyleBonusType(level_up['style_bonus_type'])
            bonus_value = level_up['style_bonus_value']
            if bonus_type == StyleBonusType.STR:
                self.str_bonus += bonus_value
            if bonus_type == StyleBonusType.END:
                self.end_bonus += bonus_value
            if bonus_type == StyleBonusType.DEX:
                self.dex_bonus += bonus_value
            if bonus_type == StyleBonusType.AGI:
                self.agi_bonus += bonus_value
            if bonus_type == StyleBonusType.INT:
                self.int_bonus += bonus_value
            if bonus_type == StyleBonusType.WIL:
                self.int_bonus += bonus_value
            if bonus_type == StyleBonusType.LOV:
                self.lov_bonus += bonus_value
            if bonus_type == StyleBonusType.CHA:
                self.cha_bonus += bonus_value
            if bonus_type == StyleBonusType.All_Attributes:
                self.str_bonus += bonus_value
                self.end_bonus += bonus_value
                self.dex_bonus += bonus_value
                self.agi_bonus += bonus_value
                self.int_bonus += bonus_value
                self.wil_bonus += bonus_value
                self.lov_bonus += bonus_value
                self.cha_bonus += bonus_value
            if bonus_type in (StyleBonusType.Ability1, StyleBonusType.Ability2, StyleBonusType.Ability3):
                for ability in abilities_list:
                    if ability.id == bonus_value:
                        self.abilities.append(ability)

    def get_base_stat_bonus(self, stat_caps_list):
        stat_cap_object = [sc for sc in stat_caps_list if sc['styleId'] == self.id]
        if stat_cap_object:
            stat_cap_object = stat_cap_object[0]
            if stat_cap_object['modifier_char_str'] is None or stat_cap_object['modifier_str'] is None:
                print(self.style_name)
            else:
                self.base_str_bonus = stat_cap_object['modifier_char_str'] + stat_cap_object['modifier_str']
                self.base_end_bonus = stat_cap_object['modifier_char_end'] + stat_cap_object['modifier_end']
                self.base_dex_bonus = stat_cap_object['modifier_char_dex'] + stat_cap_object['modifier_dex']
                self.base_agi_bonus = stat_cap_object['modifier_char_agi'] + stat_cap_object['modifier_agi']
                self.base_int_bonus = stat_cap_object['modifier_char_int'] + stat_cap_object['modifier_int']
                self.base_wil_bonus = stat_cap_object['modifier_char_wil'] + stat_cap_object['modifier_wil']
                self.base_lov_bonus = stat_cap_object['modifier_char_lov'] + stat_cap_object['modifier_lov']
                self.base_cha_bonus = stat_cap_object['modifier_char_cha'] + stat_cap_object['modifier_cha']

    def pretty_print(self):
        print('{0} {1} - {2}'.format(self.rank, self.character_name, self.style_name))
        print('  STR: {0}% +{1}'.format(self.level_50_str_mod, self.str_bonus))
        print('  END: {0}% +{1}'.format(self.level_50_end_mod, self.end_bonus))
        print('  DEX: {0}% +{1}'.format(self.level_50_dex_mod, self.dex_bonus))
        print('  AGI: {0}% +{1}'.format(self.level_50_agi_mod, self.agi_bonus))
        print('  INT: {0}% +{1}'.format(self.level_50_int_mod, self.int_bonus))
        print('  WIL: {0}% +{1}'.format(self.level_50_wil_mod, self.wil_bonus))
        print('  LOV: {0}% +{1}'.format(self.level_50_lov_mod, self.lov_bonus))
        print('  CHA: {0}% +{1}'.format(self.level_50_cha_mod, self.cha_bonus))
        print('  Skill1: {0}'.format(self.skills[0]))
        print('  Skill2: {0}'.format(self.skills[1]))
        print('  Skill3: {0}'.format(self.skills[2]))
        print('  Ability1: {0}'.format(self.abilities[0]))
        print('  Ability2: {0}'.format(self.abilities[1]))
        print('  Ability3: {0}'.format(self.abilities[2]))

    def __str__(self):
        return self.style_name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            skills_match = all([s in other.skills for s in self.skills])
            abilities_match = all([a in other.abilities for a in self.abilities])
            are_equal = self.style_name == other.style_name and self.rank == other.rank \
                        and self.character_name == other.character_name and self.weapon_type == other.weapon_type \
                        and self.str_bonus == other.str_bonus and self.end_bonus == other.end_bonus \
                        and self.dex_bonus == other.dex_bonus and self.agi_bonus == other.agi_bonus \
                        and self.int_bonus == other.int_bonus and self.wil_bonus == other.wil_bonus \
                        and self.lov_bonus == other.lov_bonus and self.cha_bonus == other.cha_bonus \
                        and self.level_50_str_mod == other.level_50_str_mod \
                        and self.level_50_end_mod == other.level_50_end_mod \
                        and self.level_50_dex_mod == other.level_50_dex_mod \
                        and self.level_50_agi_mod == other.level_50_agi_mod \
                        and self.level_50_int_mod == other.level_50_int_mod \
                        and self.level_50_wil_mod == other.level_50_wil_mod \
                        and self.level_50_lov_mod == other.level_50_lov_mod \
                        and self.level_50_cha_mod == other.level_50_cha_mod \
                        and skills_match \
                        and abilities_match
            return are_equal


def get_styles(style_filename):
    from json import load
    with open(style_filename, 'r') as style_file:
        styles = load(style_file)
    style_list = []
    for style_json in styles:
        style = Style(style_json)
        style_list.append(style)
    return style_list


def merge_styles_with_skill_data(styles_list, skills_list):
    dud_styles = []
    for style in styles_list:
        style.update_skills(skills_list)
        if len(style.skills) != 3:
            dud_styles.append(style)
    for dud_style in dud_styles:
        styles_list.remove(dud_style)


def merge_styles_with_level_up_data(styles_list, level_up_file, abilities_list):
    from json import load
    with open(level_up_file, 'r') as level_up:
        level_up_data = load(level_up)
    dud_styles = []
    for style in styles_list:
        style.handle_level_ups(level_up_data, abilities_list)
        if len(style.abilities) != 3:
            dud_styles.append(style)
    for dud_style in dud_styles:
        styles_list.remove(dud_style)


def merge_styles_with_base_stat_mods(styles_list, stat_mod_filename):
    from json import load
    with open(stat_mod_filename, 'r') as stat_file:
        stat_mod_data = load(stat_file)
    for style in styles_list:
        style.get_base_stat_bonus(stat_mod_data)
