from data import load_styles, load_characters
from jsonpickle import encode, decode
from data.dataset.find_missing_base_stats import update_base_style_stats


def construct_styles(output_file):
    styles = load_styles(reload=True)
    with open(output_file, 'w') as style_file:
        json_strings = encode(styles, indent=2)
        style_file.write(json_strings)


def update_styles(output_file):
    updated_styles = update_base_style_stats('base_style_stats.csv')
    with open(output_file, 'w') as style_file:
        json_strings = encode(updated_styles, indent=2)
        style_file.write(json_strings)


def retrieve_styles(input_file):
    with open(input_file, 'r') as style_file:
        input_string = style_file.read()
    styles = decode(input_string)
    return styles


def construct_characters(style_file, character_file):
    characters = load_characters(retrieve_styles(style_file), reload=True)
    with open(character_file, 'w') as output_file:
        json_string = encode(characters, indent=2)
        output_file.write(json_string)


def retrieve_characters(character_file):
    with open(character_file, 'r') as input_file:
        input_string = input_file.read()
    characters = decode(input_string)
    return characters


if __name__ == '__main__':
    style_filename = 'styles_with_updated_stats.json'
    construct_styles(style_filename)
    update_styles(style_filename)
    test_styles = retrieve_styles(style_filename)
    human_m = test_styles[2]
    human_m.pretty_print()
    construct_characters('styles_with_updated_stats.json', 'character_objects.json')
