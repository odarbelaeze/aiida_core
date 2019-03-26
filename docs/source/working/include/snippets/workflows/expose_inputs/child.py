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
from aiida.orm import Bool, Float, Int
from aiida.engine import WorkChain


class ChildWorkChain(WorkChain):

    @classmethod
    def define(cls, spec):
        super(ChildWorkChain, cls).define(spec)
        spec.input('a', valid_type=Int)
        spec.input('b', valid_type=Float)
        spec.input('c', valid_type=Bool)
        spec.outline(cls.do_run)
        spec.output('d', valid_type=Int)
        spec.output('e', valid_type=Float)
        spec.output('f', valid_type=Bool)

    def do_run(self):
        self.out('d', self.inputs.a)
        self.out('e', self.inputs.b)
        self.out('f', self.inputs.c)
