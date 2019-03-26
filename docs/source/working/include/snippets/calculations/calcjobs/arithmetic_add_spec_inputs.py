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
from aiida.engine import CalcJob

class ArithmeticAddCalculation(CalcJob):
    """Implementation of CalcJob to add two numbers for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        super(ArithmeticAddCalculation, cls).define(spec)
        spec.input('x', valid_type=orm.Int, help='The left operand.')
        spec.input('y', valid_type=orm.Int, help='The right operand.')
