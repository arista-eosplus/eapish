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

"""Shell command for Arista EOS command API (eAPI)

TODO: Add description and examples
"""
import argparse
import hashlib
import json
import re

import pyeapi

def cmd_line_parser(args):
    """Parse the command line options and return an args dict
    """

    parser = argparse.ArgumentParser(description=('Shell command for Arista '
                                                  'EOS command API (eAPI)'))

    parser.add_argument('cmd',
                        nargs='+',
                        help='Command to send using eAPI')

    parser.add_argument('--config',
                        action='store_true',
                        default=False,
                        help='Run commands from global configuration mode')

    parser.add_argument('--hosts',
                        default='localhost',
                        help='Specifies comma seperated list of EOS nodes '
                             'to run the command (default=localhost)')

    parser.add_argument('--text',
                        action='store_true',
                        default=False,
                        help='Return text format. Default is json. Ignored '
                             'if config parameter set.')

    return parser.parse_args(args)

def remove_hdr(response):
    """Extract the header lines from the config. This ensures that a
       startup config that is the same as the running config will have
       the same hash.
    """
    return re.sub(r'^!.*! device:', '! device:', response,
                  flags=re.DOTALL|re.IGNORECASE)

def gen_hash_string(response):
    hsh = hashlib.sha256()
    hsh.update(response)
    return '\nSHA256 HASH: %s\n' % hsh.hexdigest()

def get_config(node, cmd):
    response = node.get_config(cmd, as_string=True)
    response = remove_hdr(response)
    response += gen_hash_string(response)
    return response

def run_cmds(node, config, cmds, encoding):
    if len(cmds) == 1 and cmds[0] == 'get_configs':
        response = get_config(node, 'startup-config')
        response += get_config(node, 'running-config')
        print response
    else:
        if config:
            response = node.config(cmds)
        else:
            response = node.enable(cmds, encoding=encoding)

        # Print output from command
        print json.dumps(response, sort_keys=True, indent=4,
                         separators=(',', ': '))

def main(args=None):
    """Main execution routine for eapish command

    Parse the command line options, create a pyeapi connection to each host,
    send the commands, print the output from each host.

    Args:
        args (list): The list of args from the command line

    Returns:
        0: If the command completed successfully
        2: If the command did not complete successfully
    """

    args = cmd_line_parser(args)

    # Build the command
    cmds = ' '.join(args.cmd)

    # Set the response encoding
    encoding = 'text' if args.text else 'json'

    # Parse the list of hosts
    hosts = args.hosts.split(',')

    # For each host send the commands and store in the responses dict:
    for host in hosts:
        print '\nHost: %s' % host

        # Create connection to host
        node = pyeapi.connect_to(host)

        if node is None:
            print 'Error: "%s" connection profile not found' % host
            return 2

        run_cmds(node, args.config, cmds.split(','), encoding)

    return 0
