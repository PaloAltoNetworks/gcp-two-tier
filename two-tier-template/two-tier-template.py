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

import uuid

"""Creates the Compute Engine."""
#Variables
randstr = uuid.uuid4().hex[:6].upper()
zone = ###ZONE
region = ###Region
sshkey = ## ssh key PUBLIC
bootstrap_bucket = ###bootstrap bucket
scripts_bucket = ###bucket with web and db startup scripts
serviceaccount = ###GCP service account


image = "vmseries-byol-810"
mgmt_network = "mgmt-network-" + randstr
mgmt_subnet = "mgmt-subnet-" + randstr 
web_network = "web-network-" + randstr
web_subnet = "web-subnet-" + randstr
untrust_network = "untrust-network-" + randstr
untrust_subnet = "untrust-subnet-" + randstr
db_network = "db-network-" + randstr
db_subnet = "db-subnet-" + randstr
imageWeb = "debian-8"
machineType = "n1-standard-4"
machineTypeWeb = "f1-micro"
fwname = "vm-series-" + randstr
webserver_name = "web-vm-" + randstr
dbserver_name = "db-vm-" + randstr
mgmt_firewall_rule = "mgmt-firewall-" + randstr
untrust_firewall_rule = "untrust-firewall-" + randstr
web_firewall_rule = "web-firewall-rule-" + randstr
db_firewall_rule = "db-firewall-rule-" + randstr
web_route = "web-route-" + randstr
db_route = "db-route-" + randstr


def GenerateConfig(unused_context):
  """Creates the Compute Engine with multiple templates."""
  resources = [
  {
      'name': fwname,
      'type': 'vm-series-template.py',
      'properties': {
          'name': 'vm-series',
          'zone': zone,
          'machineType': machineType,
          'mgmt-network': mgmt_network,
          'mgmt-subnet': mgmt_subnet,
          'web-network': web_network,
          'web-subnet': web_subnet,
          'untrust-network': untrust_network,
          'untrust-subnet': untrust_subnet,
          'db-network': db_network,
          'db-subnet': db_subnet,
          'image': image,
          'bootstrapbucket': bootstrap_bucket,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount
      }
  },
  {
      'name': webserver_name,
      'type': 'webserver-template.py',
      'properties': {
          'name': webserver_name,
          'zone': zone,
          'machineTypeWeb': machineTypeWeb,
          'web-network': web_network,
          'web-subnet': web_subnet,
          'imageWeb': imageWeb,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount,
          'bootstrapbucket': scripts_bucket,
      }
  },
    {
      'name': dbserver_name,
      'type': 'dbserver-template.py',
      'properties': {
          'name': dbserver_name,
          'zone': zone,
          'machineTypeWeb': machineTypeWeb,
          'db-network': db_network,
          'db-subnet': db_subnet,
          'imageWeb': imageWeb,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount,
          'bootstrapbucket': scripts_bucket,
      }
  },
  {
      'name': mgmt_network,
      'type': 'network-template.py'
  },
  {
      'name': mgmt_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': mgmt_network,
          'ipcidrrange': '10.5.0.0/24',
          'region': region
      }
  },
  {
      'name': web_network,
      'type': 'network-template.py'
  },
  {
      'name': web_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': web_network,
          'ipcidrrange': '10.5.2.0/24',
          'region': region
      }
  },
  {
      'name': untrust_network,
      'type': 'network-template.py'
  },
  {
      'name': untrust_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': untrust_network,
          'ipcidrrange': '10.5.1.0/24',
          'region': region
      }
  },
  {
      'name': db_network,
      'type': 'network-template.py'
  },
   {
      'name': db_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': db_network,
          'ipcidrrange': '10.5.3.0/24',
          'region': region
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },      
      'name': web_route,
      'type': 'compute.v1.route',
      'properties': {
        'priority': 100,
        'network': '$(ref.'+web_network+'.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '$(ref.vm-series.networkInterfaces[2].networkIP)'
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },      
      'name': db_route,
      'type': 'compute.v1.route',
      'properties': {
        'priority': 100,
        'network': '$(ref.'+db_network+'.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '$(ref.vm-series.networkInterfaces[3].networkIP)'
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },
      'name': mgmt_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
          'network': '$(ref.'+mgmt_network+'.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [22, 443]
          }]
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },
      'name': untrust_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
          'network': '$(ref.'+untrust_network+'.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [80, 221, 222]
          }]
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },
      'name': web_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
        'network': '$(ref.'+web_network+'.selfLink)',
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
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, db_network, web_network, untrust_network]
      },      
      'name': db_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
        'network': '$(ref.'+db_network+'.selfLink)',
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
  }
  ]
  return {'resources': resources}
