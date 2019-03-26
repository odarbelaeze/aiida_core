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

class ComplexParentWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super(ComplexParentWorkChain, cls).define(spec)
        spec.expose_inputs(ChildWorkChain, include=['a'])
        spec.expose_inputs(ChildWorkChain, namespace='child_1', exclude=['a'])
        spec.expose_inputs(ChildWorkChain, namespace='child_2', exclude=['a'])
        spec.outline(cls.run_children, cls.finalize)
        spec.expose_outputs(ChildWorkChain, include=['e'])
        spec.expose_outputs(ChildWorkChain, namespace='child_1', exclude=['e'])
        spec.expose_outputs(ChildWorkChain, namespace='child_2', exclude=['e'])


    def run_children(self):
        child_1_inputs = self.exposed_inputs(ChildWorkChain, namespace='child_1')
        child_2_inputs = self.exposed_inputs(ChildWorkChain, namespace='child_2', agglomerate=False)
        child_1 = self.submit(ChildWorkChain, **child_1_inputs)
        child_2 = self.submit(ChildWorkChain, a=self.inputs.a, **child_2_inputs)
        return ToContext(child_1=child_1, child_2=child_2)

    def finalize(self):
        self.out_many(
            self.exposed_outputs(
                self.ctx.child_1,
                ChildWorkChain,
                namespace='child_1'
            )
        )
        self.out_many(
            self.exposed_outputs(
                self.ctx.child_2,
                ChildWorkChain,
                namespace='child_2',
                agglomerate=False
            )
        )
