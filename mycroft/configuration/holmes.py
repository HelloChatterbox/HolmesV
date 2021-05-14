"""This file will check a system level HolmesV specific config file

The holmes config is json with comment support like the regular mycroft.conf

Default locations tried by order until a file is found
- /etc/HolmesV/holmes.conf
- /etc/mycroft/holmes.conf

XDG locations are then merged over the select default config (if found)

Examples config:

{
   // check xdg directories OR only check old style hardcoded paths
   // the default value is False so the default behaviour is the same as mycroft-core
   // once MycroftAI/mycroft-core/pull/2794 is merged the default value will change to True
   "xdg": true,

   // the "name of the core",
   //         eg, OVOS, Neon, Chatterbox...
   //  all XDG paths should respect this
   //        {xdg_path}/{base_folder}/some_resource
   // "mycroft.conf" paths are derived from this
   //        ~/.{base_folder}/mycroft.conf
   "base_folder": "HolmesV",

   // the filename of "mycroft.conf",
   //      eg, ovos.conf, chatterbox.conf, neon.conf...
   // "mycroft.conf" paths are derived from this
   //        ~/.{base_folder}/{config_filename}
   "config_filename": "mycroft.conf",

   // override the default.conf location, allows changing the default values
   //     eg, disable backend, disable skills, configure permissions
   "default_config_path": "/etc/HolmesV/default_mycroft.conf",

   // this is intended for derivative products, if a module name is present
   // in sys.modules then the values below will be used instead
   //     eg, chatterbox/mycroft/ovos/neon can coexist in the same machine
   "module_overrides": {
        "chatterbox": {
            "xdg": false,
            "base_folder": "chatterbox",
            "config_filename": "chatterbox.conf",
            "default_config_path": "/opt/chatterbox/chatterbox.conf"
        },
        "ovos": {
            "xdg": true,
            "base_folder": "ovos",
            "config_filename": "ovos.conf"
        },
        "neon_core": {
            "xdg": true,
            "base_folder": "neon",
            "config_filename": "neon.conf",
            "default_config_path": "/opt/neon/neon.conf"
        }
   },
   // essentially aliases for the above, useful for microservice architectures
   "submodule_mappings": {
        "chatterbox_stt": "chatterbox",
        "chatterbox_playback": "chatterbox",
        "chatterbox_admin": "chatterbox",
        "chatterbox_blockly": "chatterbox",
        "chatterbox_gpio_service": "chatterbox"
   }
}
"""
from importlib.util import find_spec
from os.path import isfile, dirname, join

import xdg.BaseDirectory
from mycroft.util.json_helper import load_commented_json, merge_dict


def get_holmes_config():
    config = {"xdg": False,
              "base_folder": "mycroft",
              "config_filename": "mycroft.conf",
              "default_config_path": join(dirname(__file__), "mycroft.conf")}

    if isfile("/etc/HolmesV/holmes.conf"):
        config = merge_dict(config,
                            load_commented_json("/etc/HolmesV/holmes.conf"))
    elif isfile("/etc/mycroft/holmes.conf"):
        config = merge_dict(config,
                            load_commented_json("/etc/mycroft/holmes.conf"))

    # This includes both the user config and
    # /etc/xdg/HolmesV/holmes.conf
    for p in xdg.BaseDirectory.load_config_paths("HolmesV"):
        if isfile(join(p, "holmes.conf")):
            xdg_cfg = load_commented_json(join(p, "holmes.conf"))
            config = merge_dict(config, xdg_cfg)

    # let's check for derivatives specific configs
    # the assumption is that these cores are exclusive to each other,
    # this will never find more than one override
    # TODO this works if using dedicated .venvs what about system installs?
    cores = config.get("module_overrides") or {}
    for k in cores:
        if find_spec(k):
            config = merge_dict(config, cores[k])
            break
    else:
        subcores = config.get("submodule_mappings") or {}
        for k in subcores:
            if find_spec(k):
                config = merge_dict(config, cores[subcores[k]])
                break

    return config


def is_using_xdg():
    return get_holmes_config().get("xdg", False)
