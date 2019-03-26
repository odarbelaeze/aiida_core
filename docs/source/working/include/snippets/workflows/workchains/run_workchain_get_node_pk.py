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
from aiida.engine import run_get_node, run_get_pk
from aiida.orm import Int

result, node = run_get_node(AddAndMultiplyWorkChain, a=Int(1), b=Int(2), c=Int(3))
result, pk = run_get_pk(AddAndMultiplyWorkChain, a=Int(1), b=Int(2), c=Int(3))
