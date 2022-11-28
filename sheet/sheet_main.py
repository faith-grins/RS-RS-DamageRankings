from sheet.sheet_login import login, SPREADSHEET_ID
from sheet.style_data import write_style_data
from sheet.style_stats import write_stats_data
from sheet.skill_data import write_skills_data
from data.ingest import load_characters, load_styles, load_skills
from data.dataset import retrieve_styles, retrieve_characters


def update_style_data_tab(styles_list, characters_list):
    auth = login()
    write_style_data(auth, SPREADSHEET_ID, styles_list, characters_list)


def update_style_stats_tab(styles_list, characters_list):
    auth = login()
    write_stats_data(auth, SPREADSHEET_ID, styles_list, characters_list)


def update_skills_tab(skills_list):
    auth = login()
    write_skills_data(auth, SPREADSHEET_ID, skills_list)


if __name__ == '__main__':
    style_file = '../data/dataset/styles_with_updated_stats.json'
    character_file = '../data/dataset/character_objects.json'
    styles = retrieve_styles(style_file)
    characters = retrieve_characters(character_file)
    # skills = load_skills()
    update_style_data_tab(styles, characters)
    update_style_stats_tab(styles, characters)
    # update_skills_tab(skills)
