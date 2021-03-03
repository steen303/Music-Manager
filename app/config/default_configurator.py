from configparser import ConfigParser

config = ConfigParser(allow_no_value=True)
config.optionxform = str


def restore():
    set_default_config()
    write_file()


def write_file():
    config.write(open('conf/settings.cfg', 'w'))


def set_default_config():
    config['DEFAULT'] = {'readOnlySection': 'false', }
    config['youtube'] = {}
    config['youtube']['API'] = 'LpYGwMzazdfdxAHCTRZhStSPMeyEVGNMYynuACzD'

    config['database'] = {}
    database = config['database']
    database['useLocalDB'] = 'yes'
    database['dbFileLocation'] = '../resources/music.db'
    database['url'] = ''
    database['username'] = ''
    database['password'] = ''
    database['readOnlySection'] = 'true'

    config['music-library'] = {}
    music_lib = config['music-library']
    music_lib['run_filescan'] = 'true'
    music_lib['library-root'] = 'D:\Music\GOA\Old School'
    music_lib['artist-albums-dir'] = '%(library-root)s\Artist Releases'
    music_lib['artist-albums-dir-test'] = '%(library-root)s\Artist Releases\Adrenalin Drum'
