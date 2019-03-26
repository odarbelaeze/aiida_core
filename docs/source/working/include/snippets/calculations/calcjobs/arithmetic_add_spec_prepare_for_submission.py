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
from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.engine import CalcJob

class ArithmeticAddCalculation(CalcJob):
    """Implementation of CalcJob to add two numbers for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        super(ArithmeticAddCalculation, cls).define(spec)
        spec.input('x', valid_type=orm.Int, help='The left operand.')
        spec.input('y', valid_type=orm.Int, help='The right operand.')
        spec.output('sum', valid_type=orm.Int, help='The sum of the left and right operand.')

    def prepare_for_submission(self, folder):
        """Write the input files that are required for the code to run.

        :param folder: an `~aiida.common.folders.Folder` to temporarily write files on disk
        :return: `~aiida.common.datastructures.CalcInfo` instance
        """
        input_x = self.inputs.x
        input_y = self.inputs.y

        # Write the input file based on the inputs that were passed
        with folder.open(self.options.input_filename, 'w', encoding='utf8') as handle:
            handle.write(u'{} {}\n'.format(input_x.value, input_y.value))

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['-in', self.options.input_filename]
        codeinfo.stdout_name = self.options.output_filename
        codeinfo.code_uuid = self.inputs.code.uuid

        calcinfo = CalcInfo()
        calcinfo.uuid = str(self.node.uuid)
        calcinfo.codes_info = [codeinfo]
        calcinfo.retrieve_list = []
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []

        return calcinfo
