from itertools import combinations
from data.ingest import load_skills
from data import model


def find_dual_damage_skills():
    skill_list = load_skills()
    dual_damage_types = {c: [] for c in combinations(model.DamageType, 2)}
    for damage_type_pair in dual_damage_types:
        for skill in skill_list:
            if damage_type_pair[0] in skill.damage_types and damage_type_pair[1] in skill.damage_types:
                dual_damage_types[damage_type_pair].append(skill)
    return dual_damage_types


if __name__ == '__main__':
    type_pairs = find_dual_damage_skills()
    for pair in type_pairs:
        print('{0}/{1} skills: {2}'.format(pair[0].name, pair[1].name, len(type_pairs[pair])))
        if pair[0].name == 'Slash' and pair[1].name == 'Blunt':
            for skill in type_pairs[pair]:
                print('  {0}'.format(skill.name))
