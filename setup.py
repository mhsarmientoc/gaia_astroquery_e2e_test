#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 28 Aug. 2020
"""

from distutils.dir_util import copy_tree, remove_tree
import os
import shutil
import logging as log
from pathlib import Path

from_directory = "src"
to_directory = f"target/lib/{from_directory}"
copy_tree(from_directory, to_directory)
mdir = None
for mdir in ["assembly", "main/filters", "non-packaged-resources"]:
    rm_dir = f"target/lib/src/{mdir}"
    remove_tree(rm_dir)

# Clean old logs
logsDir = f'logs/'

files_in_directory = os.listdir(logsDir)
filtered_files = [file for file in files_in_directory if file.endswith('.log')]
for file in filtered_files:
    path_to_file = os.path.join(logsDir, file)
    os.remove(path_to_file)