#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from aiida.orm import Bool, Float, Int
from aiida.engine import run
from simple_parent import SimpleParentWorkChain

if __name__ == '__main__':
    result = run(SimpleParentWorkChain, a=Int(1), b=Float(1.2), c=Bool(True))
    print(result)
    # {u'e': 1.2, u'd': 1, u'f': True}
