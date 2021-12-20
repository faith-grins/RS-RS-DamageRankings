from .Common import WeaponType, MagicType, DamageType, SkillRange


_int_fist_indicator_text = '*M. Arts Special Skill (INT)'


class Skill:
    def __init__(self, skill_name):
        self.name = skill_name
        self.power_rank = 'E'
        self.power_number = 0
        self.weapon_type = WeaponType.Sword
        self.magic_type = None
        self.range = SkillRange.OneEnemy
        self.damage_types = [DamageType.Slash]
        self.is_spell = False
        self.bp_cost = 0
        self.lp_cost = 0
        self.awakens = 0
        self.min_hits = 1
        self.max_hits = 1
        self.has_amplify = False
        self.id = 0

    def update(self, json_object):
        self.power_rank = json_object['power_grade']
        self.id = json_object['id']
        if json_object['battle_type'] > 10:
            self.weapon_type = WeaponType.Spell
            self.magic_type = MagicType(json_object['battle_type'])
        else:
            self.weapon_type = WeaponType(json_object['battle_type'])
        if _int_fist_indicator_text in json_object['flavor_text']:
            self.weapon_type = WeaponType.IntFist
        self.bp_cost = json_object['consume_bp']
        self.lp_cost = json_object['consume_lp']
        self.awakens = json_object['max_awakening_count']
        self.min_hits = json_object['min_action_time']
        self.max_hits = json_object['max_action_time']
        self.is_spell = json_object['skill_type'] == 2
        self.damage_types = [DamageType(t) for t in json_object['attack_attributes']]

    def __str__(self):
        return '{0}: {1} (Id={2})'.format(self.name, self.power_rank, self.id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.name == other.name and self.power_rank == other.power_rank \
                   and self.power_number == other.power_number and  self.weapon_type == other.weapon_type \
                   and self.magic_type == other.magic_type and self.range == other.range \
                   and self.is_spell == other.is_spell and self.bp_cost == other.bp_cost \
                   and self.lp_cost == other.lp_cost and self.awakens == other.awakens \
                   and self.min_hits == other.min_hits and self.max_hits == other.max_hits


def get_skills(skill_filename, skill_power_filename):
    from json import load
    with open(skill_filename, 'r') as skill_file:
        skill_list = load(skill_file)
    skill_dict = {}
    for skill in skill_list:
        skill_id = skill['id']
        if skill_id not in skill_dict:
            this_skill = Skill(skill['name'])
            this_skill.update(skill)
            skill_dict[skill_id] = this_skill
    with open(skill_power_filename, 'r') as skill_file:
        skill_power_list = load(skill_file)
    for skill_power in skill_power_list:
        if skill_power['skillId'] in skill_dict:
            skill_dict[skill_power['skillId']].power_number = skill_power['power']
    return skill_dict
