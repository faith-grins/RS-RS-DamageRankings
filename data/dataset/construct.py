from data import load_styles
from jsonpickle import encode, decode
from data.dataset.find_missing_base_stats import update_base_style_stats


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


def reconstruct_styles(input_file):
    with open(input_file, 'r') as style_file:
        input_string = style_file.read()
    styles = decode(input_string)
    return styles


if __name__ == '__main__':
    test_styles = reconstruct_styles('styles_with_updated_stats.json')
    human_m = test_styles[2]
    human_m.pretty_print()
