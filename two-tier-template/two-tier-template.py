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
"""Creates the Compute Engine."""
import uuid
#Variables
zone = ###ZONE
region = ###Region
sshkey = ## ssh key PUBLIC
bootstrap_bucket = ###bootstrap bucket
scripts_bucket = ###Bucket where gcp template files are stored. Can be bootstrap bucket
serviceaccount = ###GCP service account
project_name = ###GCP project name
image = ####FW image name

mgmt_network = "mgmt-network-"+uuid.uuid4().hex[:4].upper()
mgmt_subnet = "mgmt-subnet"
web_network = "web-network-"+uuid.uuid4().hex[:4].upper()
web_subnet = "web-subnet"
untrust_network = "untrust-network-"+uuid.uuid4().hex[:4].upper()
untrust_subnet = "untrust-subnet"
db_network = "db-network-"+uuid.uuid4().hex[:4].upper()
db_subnet = "db-subnet"
imageWeb = "debian-8"
machineType = "n1-standard-4"
machineTypeWeb = "f1-micro"


def GenerateConfig(unused_context):
  """Creates the Compute Engine with multiple templates."""
  resources = [
  {
      'name': 'vm-series',
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
      'name': 'web-vm',
      'type': 'webserver-template.py',
      'properties': {
          'name': 'web-vm',
          'zone': zone,
          'machineTypeWeb': machineTypeWeb,
          'web-network': web_network,
          'web-subnet': web_subnet,
          'imageWeb': imageWeb,
          'bootstrapbucket': scripts_bucket,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount
      }
  },
    {
      'name': 'db-vm',
      'type': 'dbserver-template.py',
      'properties': {
          'name': 'db-vm',
          'zone': zone,
          'machineTypeWeb': machineTypeWeb,
          'db-network': db_network,
          'db-subnet': db_subnet,
          'imageWeb': imageWeb,
          'bootstrapbucket': scripts_bucket,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount
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
      'name': 'web-route',
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
      'name': 'db-route',
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
      'name': 'management-firewall',
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
      'name': 'untrust-firewall',
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
      'name': 'web-firewall',
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
      'name': 'db-firewall',
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
