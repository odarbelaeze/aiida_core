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
from aiida import orm
from aiida.engine import run_get_node, run_get_pk

ArithmeticAddCalculation = CalculationFactory('arithmetic.add')
result, node = run_get_node(ArithmeticAddCalculation, x=orm.Int(1), y=orm.Int(2))
result, pk = run_get_pk(ArithmeticAddCalculation, x=orm.Int(1), y=orm.Int(2))
