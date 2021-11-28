from .Common import DamageType, WeaponType


class TypeBoost:
    def __init__(self, value, weapon_type: WeaponType=None, damage_type: DamageType=None):
        self.weapon_type = weapon_type
        self.damage_type = damage_type
        self.full_hp = False
        self.weak_point = False
        self.number_of_turns = 0
        self.value = value


class Ability:
    _roman = {'Ⅳ': 4, 'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅴ': 5}
    _hardy_names = ['Hardy Wallop', 'Robust Tension']
    _weak_names = ['Weak Point Focus', 'Weak Tension']
    _fired_names = {'Fired Up': -1, 'Weak Tension': 15, 'Robust Tension': 15, 'Battle Tension': 15, 'Over Tension': 15,
                    'Strengthened Energy': 10, 'Prowess': 0, ' Amp ': 0}
    _engage_names = {'Engage'}

    def __init__(self, json_object):
        self.name = json_object['name'].strip()
        self.id = json_object['id']
        self.boost = self._fired_up()
        self.hardy_boost = self._full_hp()
        self.weak_boost = self._weak_point()
        self.engage_boost = self._engage_damage()

    def _match_name(self, ability_name):
        return any([name in self.name for name in ability_name])

    def _rank(self):
        digit = self.name[-1]
        if digit in self._roman.keys():
            return self._roman[digit]
        else:
            return 0

    def _fired_up(self):
        name_match = [name for name in self._fired_names if name in self.name]
        if name_match:
            rank = self._rank()
            if rank:
                name_match = name_match[0]
                rank += self._fired_names[name_match]
                return 2.5 if rank == 0 else 5 * rank
            else:
                return self._fired_names[self.name]
        else:
            return 0

    def _weak_point(self):
        rank = self._rank()
        if rank:
            return 5 * rank
        else:
            return 10

    def _full_hp(self):
        rank = self._rank()
        if rank:
            return 5 * rank
        else:
            return 10

    def _engage_damage(self):
        return 0

    def damage_increase(self, full_hp=False, weak_point=False):
        boost = 0
        if self._match_name(self._fired_names):
            boost += self._fired_up()
        if full_hp and self._match_name(self._hardy_names):
            boost += self._full_hp()
        if weak_point and self._match_name(self._weak_names):
            boost += self._weak_point()
        return boost


def get_abilities(filename):
    from json import loads
    with open(filename, 'r', encoding='utf8') as ability_file:
        ability_list = loads(ability_file.read())
    abilities = []
    for ability in ability_list:
        abilities.append(Ability(ability))
    return abilities
