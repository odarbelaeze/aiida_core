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
from aiida.engine import calcfunction
from aiida.orm import Int

@calcfunction
def add_multiply(x, y, z=None):
    if z is None:
        z = Int(3)

    return (x + y) * z

result = add_multiply(Int(1), Int(2))
result = add_multiply(Int(1), Int(2), Int(3))
