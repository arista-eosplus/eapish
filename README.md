# Arista eAPI Client Shell

[![Build Status](https://travis-ci.org/arista-eosplus/eapish.svg?branch=develop)](https://travis-ci.org/arista-eosplus/eapish)
[![Coverage
Status](https://coveralls.io/repos/arista-eosplus/eapish/badge.svg?branch=develop)](https://coveralls.io/r/arista-eosplus/eapish?branch=develop)

The Arista eAPI Client Shell is provides an implementation on top of the Python
Client for eAPI for sending commands to remote EOS nodes across eAPI.  The
eapish application uses pyeapi to establish a connection and forwards one or
more commands to the destination node and displays the outout on STDOUT.

This library is freely provided to the open source community for building
robust applications using Arista EOS.  Support is provided as best effort
through [Github issues](http://github.com/arista-eosplus/eapish/issues).

## Requirements

* Python Client for eAPI 
* Python 2.7 
* Arista EOS 4.12 or later with eAPI enabled

# GETTING STARTED

Getting started with eapish is fairly quick and easy.  Before sending commands
to the remote nodes, the nodes must have eAPI enabled and are accessible using
pyeapi.  

```
# send 'show version' to a single remote node
$ eapish show version --hosts veos01

# send 'show version' and 'show hostname' to remote node
$ eapish show version, show hostname --hosts veos01

# send 'show version to multiple hosts
$ eapish show version --hosts veos01,veos02,veos03

# send configuration commands to multple hosts
$ eapish vlan 100, name TEST_VLAN --hosts veos01,veos02,veos03 --config
```

# INSTALLATION

The source code for eapish is provided on Github at
http://github.com/arista-eosplus/eapish.  All current development is done in
the 'develop' branch.  Stable versions for release are tagged in the master
branch and uploaded to PyPi

* To install the latest stable versio of eapish, simply run ``pip install
  eapish`` (or ``pip install --upgrade eapish``)
* To install the latest development version from Github, simply clone the
  develop branch and run ``python setup.py install`` from the cloned folder.

# TESTING

The client shell provides unit tests for all functionality.  The unit tests can
be run without an EOS node.  In order to setup your enivornment for running the
tests, use the ``dev-requirements.txt`` file with PIP.  Then to run the unit 
tests, simply run ``make tests`` from the root of the eapish folder.

```
$ pip install -r dev-requirements.txt
$ make tests
```

# CONTRIBUTING

Contributing pull requests are gladly welcomed for this repository.  Please
note that all contributions that modify the client behavior require
corresponding test cases otherwise the pull request will be rejected.

# LICENSE

Copyright (c) 2015, Arista Networks EOS+
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the Arista nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
