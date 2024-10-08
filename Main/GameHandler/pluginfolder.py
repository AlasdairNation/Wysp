import os
import importlib.util
import sys

class pluginfolder:

    # A class to loan and manage plugins from a specific directory

    def __init__(self, plugin_dir):
        
        self.plugin_dir = plugin_dir
        self.plugins = {}
    
    def load_plugins(self):

        plugin_files = [f for f in os.listdir(self.plugin_dir) if f.endswith('.py') and f != '__init__.py']

        for file in plugin_files:
            self.loan_plugin(file)
    
    def load_plugin(self, filename):
        path = os.path.join(self.plugin_dir, filename)
        name = os.path.splitext(filename)[0]

        # import the module from the given file path

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)

        try:
            #execute the module in its own namespace
            spec.loader.exec_module(module)
            self.plugins[name] = module
            print(f"Successfully loaded plugin: {name}")
        except Exception as e:
            # handle exceptions that occur during module loading
            print(f"Failed to load plug {name}: {e}")

    def get_plugin(self,name):
        return self.plugins.get(name)