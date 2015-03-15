#
# Copyright (c) 2015, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#pylint: disable=R0904

import unittest
import shlex

from mock import patch, Mock

import eapish.app

class TestEapish(unittest.TestCase):
    ''' Test the eapish command parsing. The command is executed using
        the os.system() call and the exit code is verified.
        The tests are data driven by a test table.
    '''

    def test_parser_optional_params(self):
        ''' Test optional command line parameters that should succeed '''

        test_params = [
            "show vlan",
            "show management api http-commands",
            "'show version, show ip route'",
            "'show version, show hostname' --hosts sw1,sw2,sw3",
            "--hosts sw1,sw2,sw3 show vlan",
            "--hosts sw1,sw2,sw3 'show vlan, show version'",
            "--config --hosts sw1,sw2,sw3 hostname NAME",
            "--config --hosts sw1,sw2,sw2 'vlan 100, name TEST'",
            "--hosts sw1,sw2,sw3 show running-config"
        ]

        for cmd_line in test_params:
            args = shlex.split(cmd_line)
            result = eapish.app.cmd_line_parser(args)
            msg = 'Could not parse command line option: %s' % ' '.join(cmd_line)
            self.assertIsInstance(vars(result), dict, msg)

    @patch('pyeapi.connect_to')
    def test_run_cmd_with_invalid_host(self, pyeapi_mock):
        pyeapi_mock.return_value = None

        args = shlex.split("show vlan --hosts test")
        result = eapish.app.main(args)

        self.assertEqual(result, 2)

    @patch('pyeapi.connect_to')
    def test_run_cmd_with_enable_and_json(self, pyeapi_mock):
        node = Mock(name='node')
        pyeapi_mock.return_value = node
        node.enable.return_value = 'enable'

        args = shlex.split("show vlan --hosts test")
        result = eapish.app.main(args)

        self.assertEqual(result, 0)
        node.enable.assert_called_once_with('show vlan', encoding='json')

    @patch('pyeapi.connect_to')
    def test_run_cmd_with_enable_and_text(self, pyeapi_mock):
        node = Mock(name='node')
        pyeapi_mock.return_value = node
        node.enable.return_value = 'enable'

        args = shlex.split("show vlan --hosts test --text")
        result = eapish.app.main(args)

        self.assertEqual(result, 0)
        node.enable.assert_called_once_with('show vlan', encoding='text')

    @patch('pyeapi.connect_to')
    def test_run_cmd_with_config(self, pyeapi_mock):
        node = Mock(name='node')
        pyeapi_mock.return_value = node
        node.config.return_value = 'config'

        args = shlex.split("hostname NAME --hosts test --config")
        result = eapish.app.main(args)

        self.assertEqual(result, 0)
        node.config.assert_called_once_with('hostname NAME')

    @patch('pyeapi.connect_to')
    def test_run_cmd_with_get_config(self, pyeapi_mock):
        node = Mock(name='node')
        pyeapi_mock.return_value = node
        node.get_config.return_value = 'config'

        args = shlex.split("get_configs --hosts test")
        result = eapish.app.main(args)

        self.assertEqual(result, 0)
        node.get_config.assert_any_call('startup-config', as_string=True)
        node.get_config.assert_any_call('running-config', as_string=True)





if __name__ == '__main__':
    unittest.main()

