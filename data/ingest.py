import data.model as model
import urllib.request
import os.path
import pickle


ingest_directory = os.path.join(os.path.dirname(__file__), 'ingest')
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


def write_local_data_file(filename, dump_object):
    output_directory = os.path.join(ingest_directory, 'local', filename)
    with open(output_directory, 'wb') as file_out:
        pickle.dump(dump_object, file_out)


def load_data_file(filename):
    local_path = os.path.join(ingest_directory, 'local', filename)
    if os.path.exists(local_path):
        with open(local_path, 'rb') as data_file:
            data = pickle.load(data_file)
        return data
    else:
        return None


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
    local_weapon_file = load_data_file('weapon.pkl')
    if local_weapon_file:
        return local_weapon_file
    else:
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
        return weapon_data


def load_skills(debug=False, reload=False):
    if not reload:
        local_skill_file = load_data_file('skills.pkl')
        if local_skill_file:
            skill_data = local_skill_file
    if reload or not skill_data:
        skill_filename = os.path.join(ingest_directory, 'skills.json')
        skill_power_filename = os.path.join(ingest_directory, 'skill_power.json')
        skill_data = [s for s in model.get_skills(skill_filename, skill_power_filename).values()]
        write_local_data_file('skills.pkl', skill_data)
    if debug:
        print(len(skill_data))
        for s in skill_data:
            print(s.name)
    return skill_data


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
    english_regex = compile(r'[A-Za-z]')
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


def load_abilities(debug=False, reload=False):
    if not reload:
        local_abilities = load_data_file('abilities.pkl')
        if local_abilities:
            return local_abilities
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
    write_local_data_file('abilities.pkl', abilities)
    return abilities


def load_styles(debug=False, reload=False):
    if not reload:
        local_styles = load_data_file('styles.pkl')
        if local_styles:
            styles = local_styles
    if reload or not styles:
        # initial load of styles
        style_filename = os.path.join(ingest_directory, 'style.json')
        styles = model.get_styles(style_filename)
        # add abilities and static stat bonuses to styles
        abilities = load_abilities(False)
        level_up_file = os.path.join(ingest_directory, 'style_bonus.json')
        model.merge_styles_with_level_up_data(styles, level_up_file, abilities)
        # add skills to styles
        skills = load_skills(False)
        model.merge_styles_with_skill_data(styles, skills)
        # add base stat mods to styles
        stat_cap_file = os.path.join(ingest_directory, 'style_stat_cap.json')
        model.merge_styles_with_base_stat_mods(styles, stat_cap_file)
        # serialize
        write_local_data_file('styles.pkl', styles)
    if debug:
        for style in styles:
            style.pretty_print()
    return styles


def dedupe_styles(styles, debug=False):
    import operator
    styles_by_name = {}
    for style in styles:
        if style.style_name not in styles_by_name:
            styles_by_name[style.style_name] = [style]
        else:
            styles_by_name[style.style_name].append(style)
    for name in styles_by_name:
        if len(styles_by_name[name]) > 1:
            dupes = []
            for s in styles_by_name[name]:
                if debug:
                    s.pretty_print()
                if any([sty for sty in styles_by_name[name] if sty == s and sty is not s]):
                    dupes.append(s)
            if len(dupes) == len(styles_by_name[name]):
                for i, dupe in enumerate(dupes):
                    if i == 0:
                        continue
                    styles.remove(dupe)
            else:
                for dupe in dupes:
                    styles.remove(dupe)
    write_local_data_file('styles.pkl', styles)


def remove_dead_skills(skill_list, style_list, debug=False):
    dead_skills = []
    exception_names = ['Fang Breaker', 'Cyclone Kick', 'Unsheathe', 'Jolt Counter', 'Whirlpool']
    for skill in skill_list:
        found = False
        for style in style_list:
            if skill in style.skills:
                found = True
                break
        if not found and skill.name[-1] != '+' and skill.name not in exception_names and 'Normal Attack' not in skill.name:
            dead_skills.append(skill)
    for skill in dead_skills:
        if debug:
            print(skill)
        skill_list.remove(skill)
    write_local_data_file('skills.pkl', skill_list)


def remove_dead_abilities(ability_list, style_list, debug=False):
    dead_abilities = []
    for ability in ability_list:
        found = False
        for style in style_list:
            if ability in style.abilities:
                found = True
                break
        if not found:
            dead_abilities.append(ability)
    for ability in dead_abilities:
        if debug:
            print(ability)
        ability_list.remove(ability)
    write_local_data_file('abilities.pkl', ability_list)


def cleanup():
    # fix known errors in the ingestion files
    abilities = load_abilities()
    cleanup_skills()
    skills = load_skills(reload=True)
    weapons = load_weapons()
    styles = load_styles(reload=True)
    dedupe_styles(styles)
    remove_dead_skills(skills, styles)
    remove_dead_abilities(abilities, styles, True)


if __name__ == '__main__':
    cleanup()
