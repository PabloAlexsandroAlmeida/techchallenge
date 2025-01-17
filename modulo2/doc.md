# Gerar zip das lamabdas
chmod +x sript/packing.sh lamnda-b3
chmod +x sript/packing.sh lamnda-glue


# Provisionar os recursos

aws config  
terraform init  
terraform validate  
terraform plan -out=tfplan  
terraform apply tfplan  

# Deleter os recursos

terraform state list  
terraform plan -destroy -out=destroyplan
terraform apply destroyplan
rm -rf .terraform* terraform.tfstate terraform.tfstate.backup tfplan destroyplan

