#!/usr/bin/env python3

# Copyright © 2018 Broadcom. All Rights Reserved. The term “Broadcom” refers to
# Broadcom Inc. and/or its subsidiaries.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may also obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""

:mod:`extension_circuit_modify` - PyFOS util for modifying a circuit object.
********************************************************************************
The :mod:`extension_circuit_modify` Util to modify a circuit.

This module is a stand-alone script that can be used to modify an extension
circuit.

extension_circuit_modify.py: Usage

* Infrastructure options:
    * -i,--ipaddr=IPADDR: IP address of FOS switch.
    * -L,--login=LOGIN: Login name.
    * -P,--password=PASSWORD: Password.
    * -f,--vfid=VFID: VFID to which the request is directed.
    * -s,--secured=MODE: HTTPS mode "self" or "CA"[Optional].
    * -v,--verbose: Verbose mode[Optional].

* Util scripts options:
    * -n,--name=NAME: Set name or slot/port of the circuit.
    * -c,--circuit-id=CIRCUIT-ID: Set circuit-id of the circuit.
    * -S,--local-ip=LOCAL-IP: Set local-ip-address of the circuit.
    * -D,--remote-ip=REMOTE-IP: Set remote-ip-address of the circuit.
    * -b,--min-comm-rate=VALUE: Set minimum-communication-rate in Kb/s.
    * -B,--max-comm-rate=Value: Set maximum-communication-rate in Kb/s.

* Outputs:
    * Python dictionary content with RESTCONF response data.


.. function:: extension_circuit_modify.modify_extension_circuit(session, name,\
cid, local, remote, minB, maxB)

    *Create extension circuit*

        Example usage of the method::

                ret = extension_circuit_modify.modify_extension_circuit(
                session, name, cid, local, remote, minB, maxB)
                print (ret)

        Details::

            circuit = {
                            "name": name,
                            "circuit-id": circuit,
                            "local-ip-address": local,
                            "remote-ip-address" : remote,
                            "minimum-communication-rate": minB,
                            "maximum-communication-rate": maxB,
                      }
            result = extension_circuit_modify._modify_extension_circuit(
            session, circuit)

        * Inputs:
            :param session: Session returned by login.
            :param name: VE port name expressed as slot/port.
            :param cid: Circuit ID.
            :param local: Circuit local IP address.
            :param remote: Circuit Remote IP Address.
            :param minB: Min. comm rate for the circuit.
            :param maxB: Max. comm rate for the circuit.

        * Outputs:
            :rtype: Dictionary of return status matching rest response.

        *Use cases*

         Modify a circuit to an existing tunnel.

"""

import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_util as pyfos_util
from pyfos.pyfos_brocade_extension_tunnel import extension_circuit
import sys
import pyfos.utils.brcd_util as brcd_util

isHttps = "0"


def _modify_extension_circuit(session, cirobject):
    result = cirobject.patch(session)
    return result


def modify_extension_circuit(session, name, cid, local, remote,
                             minB=500000, maxB=50000):
    value_dict = {'name': name, 'circuit-id': cid,
                  'local-ip-address': local,
                  'remote-ip-address': remote,
                  'minimum-communication-rate': minB,
                  'maximum-communication-rate': maxB}
    cirobject = extension_circuit()
    cirobject.load(value_dict, 1)
    result = _modify_extension_circuit(session, cirobject)
    return result


def validate(circobject):
    if circobject.peek_name() is None or \
       circobject.peek_circuit_id() is None:
        return 1
    return 0


def main(argv):
    # myinput = str("-i 10.17.3.70 -n 4/19 -c 0 -S 134.10.10.1" +
    #               " -D 154.10.10.1 -b 100000 -B 100000")
    # argv = myinput.split()
    filters = ["name", "circuit_id", "remote_ip_address", "local_ip_address",
               "maximum_communication_rate", "minimum_communication_rate"]
    inputs = brcd_util.parse(argv, extension_circuit, filters, validate)
    session = brcd_util.getsession(inputs)
    result = _modify_extension_circuit(inputs['session'], inputs['utilobject'])
    pyfos_util.response_print(result)
    pyfos_auth.logout(session)


if __name__ == "__main__":
    main(sys.argv[1:])
