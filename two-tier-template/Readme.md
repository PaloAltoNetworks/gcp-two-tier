# Sample two-tier gcp template

1. Clone this repo

2. Edit the two-tier-template.py to add your parameters.
    #Variables
    zone = #Enter the zone where you want to deploy this template
    region = ##Enter the region where you want to deploy this template
    sshkey = #Enter your ssh key and append your username at the end of the key
    bootstrap_bucket = #Bootstrap storage bucket.
    serviceaccount = ###GCP service account (the default one should suffice)
    image = #Image name of the vm-series fw. Refer to the beta guide for more info


3. Download and install the gcloud SDK and initialize it https://cloud.google.com/sdk/gcloud/

4. Deploy the template from command line as follows:
    gcloud deployment-manager deployments create deployment1 --config two-tier-sample.yaml

