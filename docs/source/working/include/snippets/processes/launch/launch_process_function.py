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
def add(x, y):
    return x + y

x = Int(1)
y = Int(2)

result = add(x, y)
result, node = add.run_get_node(x, y)
result, pk = add.run_get_pk(x, y)
