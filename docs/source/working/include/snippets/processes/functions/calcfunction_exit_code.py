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
from aiida.engine import calcfunction, ExitCode
from aiida.orm import Int

@calcfunction
def divide(x, y):
    if y == 0:
        return ExitCode(100, 'cannot divide by 0')

    return x / y

result = divide(Int(1), Int(0))
