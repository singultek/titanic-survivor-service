from classification_model.config.core import PACKAGE_ROOT, init_config
import logging
import os


logging.getLogger(init_config().app_config.package_name).addHandler(logging.NullHandler())

with open(os.path.join(PACKAGE_ROOT, "VERSION")) as version_file:
    __version__ = version_file.read().strip()
