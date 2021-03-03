from configparser import ConfigParser, NoSectionError, NoOptionError

import default_configurator as default

conf = ConfigParser(allow_no_value=True)


def start_parser():
    files_to_find = ['settings.cfg', 'conf/settings.cfg', '../conf/settings.cfg']
    found_files = conf.read(files_to_find)
    if len(found_files) < 1:
        default.restore()
        start_parser()
    conf.read(found_files[0])


def get_value(section_name, option):
    start_parser()
    try:
        value = conf.get(section_name, option)
        return value
    except (NoSectionError, NoOptionError):
        return None


# totest test if same as version 1
def get_value2(s, o):
    start_parser()
    return conf.get(s, o) if conf.has_section(s) and conf.has_option(s, o) else None


def set_value(s, o, val):
    start_parser()
    if conf.has_section(s):
        conf.set(s, o, val)
    else:
        conf.add_section(s)


def get_boolean(section_name, option):
    start_parser()
    return conf.getboolean(section_name, option)


def get_values_section(section_name):
    start_parser()
    try:
        configurations = dict(conf.items(section_name))
        configurations.pop('readonlysection')
        return configurations
    except NoSectionError:
        return None


# def get_configuration_section(section_name):
#     start_parser()
#     configurations = dict(config.items(section_name))
#     configurations.pop('readonlysection')
#     print(configurations)
#     return configurations
