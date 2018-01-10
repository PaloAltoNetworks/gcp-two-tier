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
      'name': 'web-route',
      'type': 'compute.beta.route',
      'properties': {
        'priority': 100,
        'network': '$(ref.web.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '10.5.2.4'
      }
  },{
      'name': 'db-route',
      'type': 'compute.beta.route',
      'properties': {
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
            'ports': [80, 22]
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
            'ports': [3305, 22]
          }]
      }
  }]
  return {'resources': resources}
