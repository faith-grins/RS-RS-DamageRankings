from .Common import DamageType
from re import match


_roman = {'Ⅳ': 4, 'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅴ': 5}


class TypeBoost:
    def __init__(self, value, damage_type=None):
        self.damage_type = damage_type
        self.full_hp = False
        self.weak_point = False
        self.number_of_turns = 0
        self.value = value

    def match_inputs(self, damage_type: DamageType, full_hp: bool, weak_point: bool, turn_number: int):
        return self.match_type(damage_type) and self.match_hp(full_hp) and self.match_weak(weak_point)\
               and self.match_turn(turn_number)

    def match_type(self, damage_type: DamageType):
        return not self.damage_type or self.damage_type == damage_type

    def match_hp(self, full_hp: bool):
        return not self.full_hp or full_hp

    def match_weak(self, weak_point: bool):
        return not self.weak_point or weak_point

    def match_turn(self, turn_number):
        return not self.number_of_turns or turn_number <= self.number_of_turns


class Ability:
    def __init__(self, json_object):
        self.name = json_object['name'].strip()
        self.id = json_object['id']
        self.boosts = []
        self.bp_start = 0
        self.bp_gain = 0

    def _match_name(self, ability_name):
        return any([name in self.name for name in ability_name])

    def damage_increase(self, damage_types, turn_number: int, full_hp=False, weak_point=False):
        value = 0
        for boost in self.boosts:
            for damage_type in damage_types:
                if boost.match_inputs(damage_type, full_hp, weak_point, turn_number):
                    value += boost.value
        return value

    def import_damage_boost(self, list_of_damage_dicts):
        for damage in list_of_damage_dicts:
            if match(damage['NamePattern'], self.name):
                damage_value = int(damage['DamageValue'])
                if damage_value < 5:
                    rank = _roman[self.name[-1]] + damage_value
                    if rank == 0:
                        damage_value = 2.5
                    else:
                        damage_value = 5 * rank
                boost = TypeBoost(damage_value)
                boost.full_hp = damage['FullHp'] == 'True'
                boost.weak_point = damage['WeakPoint'] == 'True'
                boost.number_of_turns = int(damage['NumberOfTurns'])
                boost.damage_type = DamageType(int(damage['DamageType'])) if damage['DamageType'] != '0' else None
                self.boosts.append(boost)

    def import_bp_boost(self, list_of_bp_boosts):
        for bp in list_of_bp_boosts:
            if match(bp['NamePattern'], self.name):
                bp_value = int(bp['Bp'])
                if bp_value == 0:
                    bp_value = _roman[self.name[-1]]
                if bp['StartOfBattle'] == 'True':
                    self.bp_start += bp_value
                if bp['EveryTurn'] == 'True':
                    self.bp_gain += bp_value

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.name == other.name and self.id == other.id


def get_abilities(ability_filename, damage_filename, bp_filename):
    from json import loads
    from csv import DictReader
    with open(ability_filename, 'r', encoding='utf8') as ability_file:
        ability_list = loads(ability_file.read())
    with open(damage_filename, 'r') as damage_file:
        damage_dict = DictReader(damage_file)
        damage_corrections = [line for line in damage_dict]
    with open(bp_filename, 'r') as bp_file:
        bp_dict = DictReader(bp_file)
        bp_corrections = [line for line in bp_dict]
    abilities = []
    for ability in ability_list:
        a = Ability(ability)
        a.import_damage_boost(damage_corrections)
        a.import_bp_boost(bp_corrections)
        abilities.append(a)
    return abilities
