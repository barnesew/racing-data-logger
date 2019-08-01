from . import FileUtils


def get(*argv):
    settings = FileUtils.load_json_from_file("./data/settings.json")
    for setting in argv:
        if setting in settings:
            settings = settings[setting]
        else:
            return None
    return settings
