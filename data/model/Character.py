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

    def update_base_stats(self):
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

    def attack(self, style, skill, weapon, formation_boost, equipment_mods, enemy_defense, enemy_resist):
        rank = 99
        skill_power = skill.power_number
        rank_modifier = (skill_power - 5) * ((100 + rank) / 100)
        if weapon.type == WeaponType.Fist:
            stat_factor = 1 +
