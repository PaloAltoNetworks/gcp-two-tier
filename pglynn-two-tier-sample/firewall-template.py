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
    """Creates the firewall."""

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
                    'sourceImage': context.properties['sourceimage'],
                }
            }],
            'metadata': {
                'items': [{
                    'key': 'vmseries-bootstrap-gce-storagebucket',
                    'value': context.properties['bootstrapbucket']
                },{
                    'key': 'ssh-keys',
                    'value': context.properties['sshkey']
                }]
            },
            'serviceAccounts': [{
               'email': context.properties['serviceaccount'],
               'scopes': [
                          'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                          'https://www.googleapis.com/auth/devstorage.read_only',
                          'https://www.googleapis.com/auth/logging.write',
                          'https://www.googleapis.com/auth/monitoring.write',
               ]}
            ],
            'canIpForward': True,
            'networkInterfaces': [{
                    'network': '$(ref.management.selfLink)',
                    'subnetwork': '$(ref.management-subnet.selfLink)',
                    'networkIP': '10.5.0.4',
                    'accessConfigs': [{
                        'name': 'mgmt access',
                        'type': 'ONE_TO_ONE_NAT'
                    }]
                },{
                    'network': '$(ref.untrust.selfLink)',
                    'subnetwork': '$(ref.untrust-subnet.selfLink)',
                    'networkIP': '10.5.1.4',
                    'accessConfigs': [{
                        'name': 'ext access',
                        'type': 'ONE_TO_ONE_NAT'
                    }]
                },{
                    'network': '$(ref.web.selfLink)',
                    'subnetwork': '$(ref.web-subnet.selfLink)',
                    'networkIP': '10.5.2.4'
                },{
                    'network': '$(ref.db.selfLink)',
                    'subnetwork': '$(ref.db-subnet.selfLink)',
                    'networkIP': '10.5.3.4'
            }]
        }
    }]
    return {'resources': resources}
