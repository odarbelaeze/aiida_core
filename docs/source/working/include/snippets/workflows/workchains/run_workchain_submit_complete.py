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
from aiida.engine import WorkChain, ToContext


class SomeWorkChain(WorkChain):

    @classmethod
    def define(cls, spec):
        super(SomeWorkChain, cls).define(spec)
        spec.outline(
            cls.submit_workchain,
            cls.inspect_workchain,
        )

    def submit_workchain(self):
        future = self.submit(SomeWorkChain)
        return ToContext(workchain=future)

    def inspect_workchain(self):
        assert self.ctx.workchain.is_finished_ok
