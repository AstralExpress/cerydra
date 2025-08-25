import pathlib
from importlib.util import spec_from_file_location, module_from_spec

import pluggy
from imperium.pathstrider import Pathstrider, PATHSTRIDER_MARKER

from app.download_plugins import download_plugins


class PathstriderOrchestrator:
    def __init__(self, logger):
        self.pm = pluggy.PluginManager(PATHSTRIDER_MARKER)
        self.pm.add_hookspecs(Pathstrider)
        self.logger = logger

    def register_plugin(self, plugin_module):
        self.pm.register(plugin_module)
        messages = self.pm.hook.init_plugin(logger=self.logger)
        for m in messages:
            self.logger.log(m)

    def load_plugins(self, config_path, plugins_dir, github_token):
        self.logger.log("Downloading plugins...")
        download_plugins(config_path, plugins_dir, github_token, self.logger)

        # Iterate over subdirectories in plugins directory
        base = pathlib.Path(plugins_dir)
        for plugin_dir in base.iterdir():
            plugin_file = plugin_dir / "plugin" / "plugin.py"

            # Create a module
            if plugin_file.exists():
                spec = spec_from_file_location(plugin_dir.name, plugin_file)  # create module specification
                module = module_from_spec(spec)  # create module object
                spec.loader.exec_module(module)  # makes the module ready to use

                # Expect a class named <PluginName>Pathstrider
                for attr in dir(module):  # iterate over classes, functions, etc.
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and attr.endswith("Pathstrider"):
                        self.register_plugin(obj())  # register plugin instance
