import data.model as model
import urllib.request
import os.path
import pickle


ingest_directory = 'ingest'
ingest_manifest = 'ingest_urls.csv'


class IngestDataFile:
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
        self.data = ''

    def ingest(self):
        self.data = urllib.request.urlopen(self.url).read()
        return self.data

    def write(self, directory):
        full_filename = os.path.join(directory, self.filename)
        with open(full_filename, 'wb') as output_file:
            output_file.write(self.data)


def get_ingest_files(directory):
    full_filename = os.path.join(directory, ingest_manifest)
    with open(full_filename, 'r') as ingest_file:
        ingest_file_rows = [row.split(',') for row in ingest_file.read().split('\n') if row.strip()]
    header = ingest_file_rows[0]
    ingest_file_rows = ingest_file_rows[1:]
    ingest_file_manifest = []
    for ingest_row in ingest_file_rows:
        ingest_file_manifest.append(IngestDataFile(ingest_row[header.index('Filename')], ingest_row[header.index('Url')]))
    return ingest_file_manifest


def load_weapons(debug=False):
    weapon_filename = os.path.join(ingest_directory, 'weapon.json')
    weapon_data = model.get_weapons(weapon_filename)
    if debug:
        print(len(weapon_data))
        for w in weapon_data:
            print(weapon_data[w])
            print('    Max WP: {0}'.format(weapon_data[w].max_wp))
            print('    Max SP: {0}'.format(weapon_data[w].max_sp))
            print('    Justsu Types: {0}'.format(weapon_data[w].magic_types))
    with open(os.path.join(ingest_directory, 'local', 'weapon.pkl'), 'wb') as weapon_file:
        pickle.dump(weapon_data, weapon_file)


def load_skills(debug=False):
    skill_filename = os.path.join(ingest_directory, 'skills.json')
    skill_power_filename = os.path.join(ingest_directory, 'skill_power.json')
    skill_data = model.get_skills(skill_filename, skill_power_filename)
    if debug:
        print(len(skill_data))
        for s in skill_data:
            print(skill_data[s].name)
    with open(os.path.join(ingest_directory, 'local', 'skills.pkl'), 'wb') as skills_file:
        pickle.dump(skill_data, skills_file)


def ingest():
    for ingestion_file_object in get_ingest_files(ingest_directory):
        ingestion_file_object.ingest()
        ingestion_file_object.write(ingest_directory)


def build():
    return


def cleanup_skills(debug=False):
    skill_file_path = os.path.join(ingest_directory, 'skills.json')
    from json import load, dump
    from re import compile
    with open(skill_file_path, 'r', encoding='utf8') as skills_file:
        skill_data = load(skills_file)
    english_regex = compile('[A-Za-z]')
    remove_list = []
    dupe_names = {}
    for s in skill_data:
        if not english_regex.search(s['name']):
            remove_list.append(s)
        elif s['name'] not in dupe_names:
            dupe_names[s['name']] = 1
        else:
            dupe_names[s['name']] += 1
    dupe_names = {d: dupe_names[d] for d in dupe_names if dupe_names[d] > 1}
    if debug:
        print(dupe_names)
    dupe_skills = {}
    for s in skill_data:
        if s['name'] in dupe_names:
            if s['name'] not in dupe_skills:
                dupe_skills[s['name']] = [s]
            else:
                dupe_skills[s['name']].append(s)
    remove_list = []
    for skill_name in dupe_skills:
        '''
        the "good" one is the one with a nonzero bp cost.  if they all have 0 bp cost, then it's either a normal attack
        or it's not player usable, in which case take the first in the list arbitrarily
        '''
        good_skill = None
        temp_remove = []
        for s in dupe_skills[skill_name]:
            if s['consume_bp'] > 0:
                good_skill = s
                if debug:
                    print(s)
            else:
                temp_remove.append(s)
        if good_skill:
            remove_list.extend(temp_remove)
        else:
            temp_remove.pop(0)
            remove_list.extend(temp_remove)
    for skill_to_remove in remove_list:
        skill_data.remove(skill_to_remove)
    with open(skill_file_path, 'w') as skills_file:
        dump(skill_data, skills_file, indent=2)


def cleanup_styles():
    return None


def load_abilities(debug=False):
    import operator
    ability_ingest = os.path.join(ingest_directory, 'ability.json')
    ability_damage = os.path.join(ingest_directory, 'damage_ability_corrections.csv')
    ability_bp = os.path.join(ingest_directory, 'bp_ability_corrections.csv')
    abilities = model.get_abilities(ability_ingest, ability_damage, ability_bp)
    abilities.sort(key=operator.attrgetter('name'))
    if debug:
        for a in abilities:
            if any([b for b in a.boosts]):
                d_type = model.Common.DamageType(1)
                print('{0}: {1}'.format(a.name, a.damage_increase(d_type, 1)))
    ability_file = os.path.join(ingest_directory, 'local', 'abilities.pkl')
    with open(ability_file, 'wb') as a_pickle_file:
        pickle.dump(abilities, a_pickle_file)


def load_styles(debug=False):
    style_filename = os.path.join(ingest_directory, 'style.json')
    styles = model.get_styles(style_filename)
    if debug:
        for style in styles:
            print('{0} {1} - {2}'.format(style.rank, style.character_name, style.style_name))
    style_file = os.path.join(ingest_directory, 'styles.pkl')
    with open(style_file, 'wb') as s_pickle_file:
        pickle.dump(styles, s_pickle_file)


def cleanup():
    # fix known errors in the ingestion files
    # load_abilities()
    # cleanup_skills()
    # load_skills()
    # load_weapons()
    load_styles(True)


if __name__ == '__main__':
    cleanup()
