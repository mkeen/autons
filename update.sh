#/bin/sh

. /usr/home/mkeen/autons/.env/bin/activate
terraform apply -var-file default.tfvars -auto-approve
deactivate
