# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Creates the network."""

def GenerateConfig(context):
    """Creates the webserver."""

    resources = [{
        'name': context.properties['hostname'],
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join(['zones/', context.properties['zone'], '/machineTypes/',context.properties['instanceSize']]),
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-9'
                }
            }],
            'metadata': {
                'items': [{
                    'key': 'ssh-keys',
                    'value': context.properties['sshkey']
                }]
            },
            'networkInterfaces': [{
                'network': '$(ref.web.selfLink)',
                'subnetwork': '$(ref.web-subnet.selfLink)',
                'networkIP': '10.5.2.5'
            }]
        }
    }]
    return {'resources': resources}

