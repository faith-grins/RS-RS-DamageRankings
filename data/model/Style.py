from enum import Enum


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
    def __init__(self, json_object):
        self.id = json_object['id']
        self.character_name = json_object['name']
        self.style_name = json_object['another_name']
        self.level_50_str_mod = json_object['bonus_rate_max_str'] / 100 - 1
        self.level_50_end_mod = json_object['bonus_rate_max_end'] / 100 - 1
        self.level_50_dex_mod = json_object['bonus_rate_max_dex'] / 100 - 1
        self.level_50_agi_mod = json_object['bonus_rate_max_agi'] / 100 - 1
        self.level_50_int_mod = json_object['bonus_rate_max_int'] / 100 - 1
        self.level_50_wil_mod = json_object['bonus_rate_max_wil'] / 100 - 1
        self.level_50_lov_mod = json_object['bonus_rate_max_lov'] / 100 - 1
        self.level_50_cha_mod = json_object['bonus_rate_max_cha'] / 100 - 1
        self.skills = []
        self.abilities = []
