#! /usr/bin/python
# -*- coding: utf8 -*-
import dmenu_extended
import os
import sys


def run():

    d = dmenu_extended.dmenu()

    cache = d.cache_load()
    out = d.menu(cache,'Open:')

    if len(out) > 0:

        # Needs fixing
        # Check if the action should modify the store
        # if out[0] == '+' or out[0] == '-':
        #     d.file_modify(d.path_store, out[1:], True if out[0] == '+' else False)

        # Check if the action relates to a plugin
        plugins = dmenu_extended.load_plugins()
        plugin_hook = False
        for plugin in plugins:
            if hasattr(plugin['plugin'], 'is_submenu') and plugin['plugin'].is_submenu == True:
                pluginTitle = d.submenu_indicator + plugin['plugin'].title
            else:
                pluginTitle = plugin['plugin'].title

            if out[:len(pluginTitle)] == pluginTitle:
                plugin_hook = plugin["plugin"]

        if plugin_hook != False:
            plugin_hook.run(out[len(pluginTitle):])

        elif out == "rebuild cache":
            result = d.cache_save(d.cache_build())
            if result == 0:
                d.menu(['Cache could not be saved'])
            elif result == 2:
                d.menu(['Issues encoundered while saving cache'])
            else:
                d.menu(['Success'])

        elif out[0] == ';' or out[-1] == ';':
            for command in out.split('&&'):
                d.open_terminal(command.replace(';',''))

        elif out[:7] == 'http://' or out[:8] == 'https://':
            f.open_url(out)

        elif out.find('/') != -1:

            if out.find(' ') != -1:
                parts = out.split(' ')
                if parts[0] in d.scan_binaries():
                    d.execute(out)
                    sys.exit()

            if os.path.isdir(out):
                d.open_directory(out)
            else:
                d.open_file(out)
        else:
            d.execute(out)


if __name__ == '__main__':
    run()