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
from __future__ import print_function
from __future__ import absolute_import
from aiida.engine import run

from serialize_workchain import SerializeWorkChain

if __name__ == '__main__':
    print(run(
        SerializeWorkChain,
        a=1, b=1.2, c=True
    ))
    # Result: {'a': 1, 'b': 1.2, 'c': True}
