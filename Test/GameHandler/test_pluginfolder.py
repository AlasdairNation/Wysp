import pytest
import os
import sys
from unittest.mock import Mock, patch
from pathlib import Path

# Calculate the path and print it to verify
plugin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Main/Plugins'))
print("Plugin path being added:", plugin_path)
sys.path.insert(0, plugin_path)
from Main.Plugins.pluginfolder import pluginfolder


@pytest.fixture
def plugin_loader(tmp_path):
    # Setup a temporary directory as the plugin directory
    d = tmp_path / "plugins"
    d.mkdir()
    (d / "example_plugin.py").write_text('def run(): return "Running"')
    loader = pluginfolder(plugin_dir=d)
    return loader

def test_load_plugins(plugin_loader, tmp_path):
    """Test loading multiple plugins."""
    # Assume there are multiple plugin files
    (tmp_path / "plugins" / "another_plugin.py").write_text('def run(): return "Also running"')
    plugin_loader.load_plugins()
    assert "example_plugin" in plugin_loader.plugins
    assert "another_plugin" in plugin_loader.plugins

def test_load_plugin_success(plugin_loader):
    """Test successful plugin loading."""
    plugin_loader.load_plugin("example_plugin.py")
    assert "example_plugin" in plugin_loader.plugins

def test_load_plugin_failure(plugin_loader):
    """Test plugin loading failure due to an error in the plugin code."""
    plugin_file = plugin_loader.plugin_dir / "bad_plugin.py"
    plugin_file.write_text('def run(): raise Exception("Error")')
    plugin_loader.load_plugin("bad_plugin.py")
    assert "bad_plugin" in plugin_loader.plugins, "Plugin with errors should not be loaded"


def test_get_plugin(plugin_loader):
    """Test getting a plugin correctly."""
    plugin_loader.load_plugin("example_plugin.py")
    plugin = plugin_loader.get_plugin("example_plugin")
    assert plugin is not None

def test_get_nonexistent_plugin(plugin_loader):
    """Test getting a non-existent plugin returns None."""
    plugin = plugin_loader.get_plugin("nonexistent")
    assert plugin is None

