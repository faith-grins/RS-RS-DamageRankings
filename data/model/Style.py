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
        self.level_50_str_mod = style_json_object['bonus_rate_max_str'] / 100 - 1
        self.level_50_end_mod = style_json_object['bonus_rate_max_end'] / 100 - 1
        self.level_50_dex_mod = style_json_object['bonus_rate_max_dex'] / 100 - 1
        self.level_50_agi_mod = style_json_object['bonus_rate_max_agi'] / 100 - 1
        self.level_50_int_mod = style_json_object['bonus_rate_max_int'] / 100 - 1
        self.level_50_wil_mod = style_json_object['bonus_rate_max_wil'] / 100 - 1
        self.level_50_lov_mod = style_json_object['bonus_rate_max_lov'] / 100 - 1
        self.level_50_cha_mod = style_json_object['bonus_rate_max_cha'] / 100 - 1
        self.str_bonus = 0
        self.end_bonus = 0
        self.dex_bonus = 0
        self.agi_bonus = 0
        self.int_bonus = 0
        self.wil_bonus = 0
        self.lov_bonus = 0
        self.cha_bonus = 0
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


def get_styles(style_filename):
    from json import load
    with open(style_filename, 'r') as style_file:
        styles = load(style_file)
    style_list = []
    for style_json in styles:
        style = Style(style_json)
        style_list.append(style)
    return style_list


def merge_styles_with_level_up_data(styles_list, level_up_file, abilities_list):
    from json import load
    with open(level_up_file, 'r') as level_up:
        level_up_data = load(level_up)
    for style in styles_list:
        style.handle_level_ups(level_up_data, abilities_list)
