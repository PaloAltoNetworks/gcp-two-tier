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
#Variables
zone = "us-west1-a"
region = "us-west1"
sshkey = 'niyengar:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCdkWALTta/QvGRSfGf8LS4CoNHuNR6ifjLMGnC0Gd5ubvU8SMNusGnY4SY/xUMuLRhmgxCFQ54mSck4zAmFQMf0ro3GDzb9UZYWAr9eQXpogNjiEY2AykYN8+E1g30WRsWdia9G2+QZ+8oCRwh2uIkTBFVtVosMOeUip2Wx+ivYtKx5ZUh9zMl4Jztr720qVlcX+NYncCYyZ8iRpnWmRf4mvggQ1jFTfKQJSNy7YAY1x+lTR5Sg6FZdaAhuxjnNzl5LL7xYqG3cbRfG+uiAEWzjdD5g07Nr+3D9G8KWBDBiQ64XabIiZDSe+Vjs57bALwcGMDBDLPzoBpPcpEL7yIe2NlXDCz8ArYPzmXwwd5GyyzhoFrSqmyAA5bPaMogQVGZjv2VMRbPz5gSnp2poO1h5YxOwvBWq0VgiDXamYiD15Sug3vyZkR7ZVQyCTe13I8H4hY7U+xSfPaqYrxAJnybFvzYtHxZcNGX6vanWEcyWzM4TEUAdWw/ApTiQQUotAg5Kw5e4j5CD+sVyAliwZNqJVIE85/iQH+Vem/B8VEU/T4J6lMbDsnQworgbdetbMSWOs8bnXAO7jNyH2m1G0Lm6FDuIv885mctJNzjG2z0dN7Dl5zA/x+nsb2Y5vZ7+BKFJOE1rPRMweUEgKGe6nZVMzr8mL4XMD1jryJboYzNNw== niyengar@paloaltonetworks.com'
bootstrap_bucket = 'narayan-storage'
serviceaccount = '201389370779-compute@developer.gserviceaccount.com'
image = "vmseries-fw-bpest"

mgmt_network = "mgmt-network"
mgmt_subnet = "mgmt-subnet"
web_network = "web-network"
web_subnet = "web-subnet"
untrust_network = "untrust-network"
untrust_subnet = "untrust-subnet"
db_network = "db-network"
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
