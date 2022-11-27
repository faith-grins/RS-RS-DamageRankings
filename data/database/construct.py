from data import load_styles
from jsonpickle import encode
from json import dump
from data.database.find_missing_base_stats import update_base_style_stats


def construct_styles(output_file):
    styles = load_styles()
    with open(output_file, 'w') as style_file:
        json_strings = encode(styles, indent=2)
        style_file.write(json_strings)


def update_styles(output_file):
    updated_styles = update_base_style_stats('base_style_stats.csv')
    with open(output_file, 'w') as style_file:
        json_strings = encode(updated_styles, indent=2)
        style_file.write(json_strings)


if __name__ == '__main__':
    update_styles('styles_with_updatedd_stats.json')
