from .Common import WeaponType
from .Common import MagicType


class EquipmentBonus:
    def __init__(self):
        self.str = 0
        self.end = 0
        self.dex = 0
        self.agi = 0
        self.int = 0
        self.wil = 0
        self.lov = 0
        self.cha = 0


class Weapon:
    def __init__(self, weapon_name):
        self.name = weapon_name
        self.rank = 'B'
        self.type = WeaponType.Sword
        self.max_wp = 0
        self.max_sp = 0
        self.magic_types = []
        self.base_str = 0
        self.max_str = 0
        self.base_end = 0
        self.max_end = 0
        self.base_dex = 0
        self.max_dex = 0
        self.base_agi = 0
        self.max_agi = 0
        self.base_int = 0
        self.max_int = 0
        self.wil = 0
        self.lov = 0
        self.cha = 0

    def update(self, json_object, initializing=False):
        json_str = json_object['add_str']
        json_end = json_object['add_end']
        json_dex = json_object['add_dex']
        json_agi = json_object['add_agi']
        json_int = json_object['add_int']
        json_wil = json_object['add_wil']
        json_lov = json_object['add_lov']
        json_cha = json_object['add_cha']
        json_wp = json_object['weapon_power'] + 4
        json_sp = json_object['jutsu_power']
        json_sp = json_sp + 4 if json_sp else 0
        self.max_wp = json_wp if json_wp > self.max_wp else self.max_wp
        self.max_sp = json_sp if json_sp > self.max_sp else self.max_sp
        self.max_str = json_str if json_str > self.max_str else self.max_str
        self.max_end = json_end if json_end > self.max_end else self.max_end
        self.max_dex = json_dex if json_dex > self.max_dex else self.max_dex
        self.max_agi = json_agi if json_agi > self.max_agi else self.max_agi
        self.max_int = json_int if json_int > self.max_int else self.max_int
        self.wil = json_wil
        self.lov = json_lov
        self.cha = json_cha
        if initializing:
            self.base_str = json_str
            self.base_end = json_end
            self.base_dex = json_dex
            self.base_agi = json_agi
            self.base_int = json_int
            self.type = WeaponType(json_object['weapon_type'])
            self.magic_types = [MagicType(mt) for mt in json_object['jutsu_types']]
        else:
            for mt in json_object['jutsu_types']:
                if MagicType(mt) not in self.magic_types:
                    self.magic_types.append(MagicType(mt))

    def __str__(self):
        return '{0}:"{1}"'.format(self.type, self.name)


def get_weapons(filename):
    from json import loads
    from re import compile
    name_regex = compile(r'\([^)]*\)')
    with open(filename, 'r') as weapon_file:
        weapon_list = loads(weapon_file.read())
    weapons = {}
    for weapon in weapon_list:
        weapon_name = name_regex.sub('', weapon['name']).strip()
        if weapon_name not in weapons:
            this_weapon = Weapon(weapon_name)
            this_weapon.update(weapon, initializing=True)
            weapons[weapon_name] = this_weapon
        else:
            weapons[weapon_name].update(weapon)
    return weapons
