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
from aiida.engine import ToContext, WorkChain, run
from child import ChildWorkChain


class SimpleParentWorkChain(WorkChain):

    @classmethod
    def define(cls, spec):
        super(SimpleParentWorkChain, cls).define(spec)
        spec.expose_inputs(ChildWorkChain)
        spec.expose_outputs(ChildWorkChain)
        spec.outline(cls.run_child, cls.finalize)

    def run_child(self):
        child = self.submit(ChildWorkChain, **self.exposed_inputs(ChildWorkChain))
        return ToContext(child=child)

    def finalize(self):
        self.out_many(
            self.exposed_outputs(self.ctx.child, ChildWorkChain)
        )
