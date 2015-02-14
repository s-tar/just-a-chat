#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
import os, sys
import kernel.server


path = os.path.dirname(os.path.abspath(__file__))
if 'APPDIR' not in os.environ:
    os.environ['APPDIR'] = path

sys.path.append(path)
os.chdir(path)

if __name__ == '__main__':
    kernel.server.run()
else:
    kernel.server.run(run=False)

application = kernel.server.app