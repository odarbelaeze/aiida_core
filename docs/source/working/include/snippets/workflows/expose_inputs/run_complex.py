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
from complex_parent import ComplexParentWorkChain

if __name__ == '__main__':
    result = run(
        ComplexParentWorkChain,
        a=Int(1),
        child_1=dict(b=Float(1.2), c=Bool(True)),
        child_2=dict(b=Float(2.3), c=Bool(False))
    )
    print(result)
    # {
    #     u'e': 1.2,
    #     u'child_1.d': 1, u'child_1.f': True,
    #     u'child_2.d': 1, u'child_2.f': False
    # }
