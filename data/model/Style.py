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
        self.weapon_type = WeaponType(style_json_object['weapon_type'])
        rank = style_json_object['rarity']
        self.rank = 'A' if rank == 3 else 'S' if rank == 4 else 'SS'
        self.skills = []
        # TODO: rain stores the abilities in a separate json file.  Need to cross-reference to get abilities
        self.abilities = []
        self._skill_ids = style_json_object['skill_ids']


def get_styles(style_filename):
    from json import load
    with open(style_filename, 'r') as style_file:
        styles = load(style_file)
    style_list = []
    for style_json in styles:
        style = Style(style_json)
        style_list.append(style)
    return style_list
