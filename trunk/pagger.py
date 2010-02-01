#!/usr/bin/env python

import sys
import os.path

sys.path.append(os.path.abspath('./src'))

from main import Main

main = Main()
main.run()
