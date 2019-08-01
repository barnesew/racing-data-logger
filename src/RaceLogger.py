from .utils import SettingsUtils
from .utils import FileUtils
from .DataMonitor import DataMonitor


def launch():
    track_data = FileUtils.load_json_from_file(
        SettingsUtils.get('dev_settings', 'environment_settings', 'tracks_folder') +
        SettingsUtils.get('current_track_file')
    )
    monitor = DataMonitor()
    monitor.set_track(track_data)
    monitor.start_monitoring()
