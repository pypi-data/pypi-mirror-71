import os
import configparser


def read_config(filepath):
    if os.path.isfile(filepath):
        config = configparser.ConfigParser()
        config.read(filepath)
        return config
    raise FileNotFoundError(filepath)


def get_config_section(config_file, conftext, moduel_name):
    """
    Get config section
    
    First check the loaded config to see if we have more than one section to choose from. Only if we
    do, we move on to use conftext to select the appropriate config section.
    """
    section_name = None
    
    if config_file.sections():
        if conftext:
            if moduel_name in conftext:
                section_name = conftext[moduel_name].get("environment")
            else:
                section_name = conftext["conftext"].get("environment")
    elif config_file.defaults():
        section_name = configparser.DEFAULTSECT
    
    if not section_name:
        raise configparser.NoSectionError(section_name)
    
    return config_file[section_name]
