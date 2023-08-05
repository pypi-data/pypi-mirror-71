import argparse
from .input import ProcessInputYaml, ProcessInputWords
from .gen_logo import Logo
from .categories import Categories
from .output import ProcessOutputYaml


def main():
    """
    Function to kick off the show.
    Accepts a YAML file as input
    """
    logo = Logo()
    logo.generate_logo()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml",
        help="an input YAML doc of bio and geographical data of the target")
    parser.add_argument(
        "words",
        help="an input text document containing a word list e.g. Linux/Unix words ")
    parser.add_argument(
        "encryption",
        help="list of encryption to be used in output ")

    args = parser.parse_args()
    plugins = plugin_processor('pata_password_cracker.encryption', args.encryption)
    process_input(args.yaml, args.words, plugins)


def plugin_processor(cat, plugins):
    """
    Return a list of plugins
    to use
    """
    plugins_to_use = {}
    plugins_to_use[cat] = plugins.split(',')
    return plugins_to_use


def process_input(yaml_file, words_file, plugins):
    """
    Create a new YAML parsing object
    and dump the content out as a dict
    """
    print ("Processing input YAML")
    yaml_to_dict = ProcessInputYaml()
    yaml_to_dict = yaml_to_dict.yaml_processor(yaml_file)
    words_to_list = ProcessInputWords()
    words_to_list = words_to_list.words_processor(words_file)

    for i in yaml_to_dict:
        for x in i['individuals']:
            generate_password_list(x, words_to_list, plugins)


def generate_password_list(individual, words_to_list, plugins):
    """
    Kick off the password list generation
    """
    individuals_passwords = Categories(
        individual, words_to_list, plugins).process_categories()
    dict_to_yaml = ProcessOutputYaml()
    dict_to_yaml.output_processor(individuals_passwords)


if __name__ == "__main__":
    main()
