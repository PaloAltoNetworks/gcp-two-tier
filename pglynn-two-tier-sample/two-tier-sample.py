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

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
  """Creates the network."""

  resources = [{
      'name': 'management',
      'type': 'compute.v1.network',
      'properties': {
          'autoCreateSubnetworks': False
      }
  },{
      'name': 'untrust',
      'type': 'compute.v1.network',
      'properties': {
          'autoCreateSubnetworks': False
      }
  },{
      'name': 'web',
      'type': 'compute.v1.network',
      'properties': {
          'autoCreateSubnetworks': False
      }
  },{
      'name': 'db',
      'type': 'compute.v1.network',
      'properties': {
          'autoCreateSubnetworks': False
      }
  },{
      'name': 'management-subnet',
      'type': 'compute.v1.subnetwork',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.management.selfLink)',
          'ipCidrRange': '10.5.0.0/24'
      }
  },{
      'name': 'untrust-subnet',
      'type': 'compute.v1.subnetwork',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.untrust.selfLink)',
          'ipCidrRange': '10.5.1.0/24'
      }
  },{
      'name': 'web-subnet',
      'type': 'compute.v1.subnetwork',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.web.selfLink)',
          'ipCidrRange': '10.5.2.0/24'
      }
  },{
      'name': 'db-subnet',
      'type': 'compute.v1.subnetwork',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.db.selfLink)',
          'ipCidrRange': '10.5.3.0/24'
      }
  },{
      'name': 'web-route',
      'type': 'compute.v1.route',
      'properties': {
        'description': '$(ref.web-subnet.selfLink)',
        'priority': 100,
        'network': '$(ref.web.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '10.5.2.4'
      }
  },{
      'name': 'db-route',
      'type': 'compute.v1.route',
      'properties': {
        'description': '$(ref.db-subnet.selfLink)',
        'priority': 100,
        'network': '$(ref.db.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '10.5.3.4'
      }
  },{
      'name': 'management-firewall',
      'type': 'compute.v1.firewall',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.management.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [22, 443]
          }]
      }
  },{
      'name': 'untrust-firewall',
      'type': 'compute.v1.firewall',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.untrust.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [80, 221, 222]
          }]
      }
  },{
      'name': 'web-firewall',
      'type': 'compute.v1.firewall',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.web.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            },{
            'IPProtocol': 'udp',
            },{
            'IPProtocol': 'icmp'
          }]
      }
  },{
      'name': 'db-firewall',
      'type': 'compute.v1.firewall',
      'properties': {
          'region': context.properties['region'], 
          'network': '$(ref.db.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            },{
            'IPProtocol': 'udp',
            },{
            'IPProtocol': 'icmp'
          }]
      }
  },{
        'name': 'firewall',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join(['zones/', context.properties['zone'], '/machineTypes/n1-standard-4']),
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
                },{
                    'key': 'serial-port-enable',
                    'value': 'true' 
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
    },{
        'name': 'dbserver',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join(['zones/', context.properties['zone'], '/machineTypes/f1-micro']),
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-8'
                }
            }],
            'metadata': {
                'items': [{
                    'key': 'ssh-keys',
                    'value': context.properties['sshkey']
                },{
                    'key': 'startup-script-url',
                    'value': ''.join(['gs://', context.properties['startupbucket'], '/dbserver-startup.sh'])
                }]
            },
            'serviceAccounts': [{
               'email': context.properties['serviceaccount'],
               'scopes': [
                          'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                          'https://www.googleapis.com/auth/devstorage.read_only',
                          'https://www.googleapis.com/auth/logging.write',
                          'https://www.googleapis.com/auth/monitoring.write',
                          'https://www.googleapis.com/auth/compute.readonly',
               ]}
            ],
            'networkInterfaces': [{
                'network': '$(ref.db.selfLink)',
                'subnetwork': '$(ref.db-subnet.selfLink)',
                'networkIP': '10.5.3.5'
            }]
        }
    },{
        'name': 'webserver',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': ''.join(['zones/', context.properties['zone'], '/machineTypes/f1-micro']),
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/debian-cloud/global/images/family/debian-8'
                }
            }],
            'metadata': {
                'items': [{
                    'key': 'ssh-keys',
                    'value': context.properties['sshkey']
                },{
                    'key': 'startup-script-url',
                    'value': ''.join(['gs://', context.properties['startupbucket'], '/webserver-startup.sh'])
                }]
            },
            'serviceAccounts': [{
               'email': context.properties['serviceaccount'],
               'scopes': [
                          'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                          'https://www.googleapis.com/auth/devstorage.read_only',
                          'https://www.googleapis.com/auth/logging.write',
                          'https://www.googleapis.com/auth/monitoring.write',
                          'https://www.googleapis.com/auth/compute.readonly',
               ]}
            ],
            'networkInterfaces': [{
                'network': '$(ref.web.selfLink)',
                'subnetwork': '$(ref.web-subnet.selfLink)',
                'networkIP': '10.5.2.5'
            }]
        }
    }]
  return {'resources': resources}
