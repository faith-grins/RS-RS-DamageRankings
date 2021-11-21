import data.model as model
import urllib.request
import os.path


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


def main_weapon():
    weapon_data = model.get_weapons('ingest/weapon.json')
    print(len(weapon_data))
    for w in weapon_data:
        print(weapon_data[w])
        print('    Max WP: {0}'.format(weapon_data[w].max_wp))
        print('    Max SP: {0}'.format(weapon_data[w].max_sp))
        print('    Justsu Types: {0}'.format(weapon_data[w].magic_types))


def main_skills():
    skill_data = model.get_skills('ingest/skills.json', 'ingest/skill_power.json')
    print(len(skill_data))
    for s in skill_data:
        print(skill_data[s].name)


def ingest():
    for ingestion_file_object in get_ingest_files(ingest_directory):
        ingestion_file_object.ingest()
        ingestion_file_object.write(ingest_directory)


def build():
    return



def dedupe_skills():
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
    print(dupe_names)
    dupe_skills = {}
    for s in skill_data:
        if s['name'] in dupe_names:
            if s['name'] not in dupe_skills:
                dupe_skills[s['name']] = [s]
            else:
                dupe_skills[s['name']].append(s)
    for skill_name in dupe_skills:
        '''
        the "good" one is the one with a nonzero bp cost.  if they all have 0 bp cost, then it's either a normal attack
        or it's not player usable, in which case take the first in the list arbitrarily
        '''
        
        for s in dupe_skills[skill_name]:
            if
                print(s)
    for dupe in dupe_skills:
        print(dupe)
    for skill_to_remove in remove_list:
        skill_data.remove(skill_to_remove)
    with open(skill_file_path, 'w') as skills_file:
        dump(skill_data, skills_file)


def cleanup():
    # fix known errors in the ingestion files
    dedupe_skills()


if __name__ == '__main__':
    cleanup()
