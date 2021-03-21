import os
from pathlib import Path

from box import Box
from box.converters import yaml

from src.monitoring import report, shorten_path

def _join_path(loader, node):
    seq = loader.construct_sequence(node)
    return Path().joinpath(*seq)

def _get_from_env(loader, node):
    return os.environ.get(node.value, None)

yaml.SafeLoader.add_constructor('!join_path', _join_path)
yaml.SafeLoader.add_constructor('!env', _get_from_env)

def _get_file_path(filename):
    path = Path(".").resolve()
    while not path == path.root:
        file_path = path / filename
        if file_path.exists():
            return file_path
        path = path.parent
    return None

params = Box(box_dots=True)
config = Box(box_dots=True)

def load_configs():
    for name in ["params", "config"]:
        filename = _get_file_path(f"{name}.yaml")
        try:
            loaded = Box.from_yaml(
                filename=filename,
                box_dots=True,
                Loader=yaml.SafeLoader,
            )
            report("config", f"Loaded {name} from [!path]{shorten_path(filename)}[/]")
            globals()[name].merge_update(loaded)
        except Exception as e:
            report("config", f"Exception [!alert]{type(e).__name__}({e})[/] occured while parsing [!path]{shorten_path(filename)}[/]")

load_configs()
