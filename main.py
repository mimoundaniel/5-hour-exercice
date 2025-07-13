import os
import subprocess
from jinja2 import Environment, FileSystemLoader

def get_user_input():
    print("=== AWS EC2 + ALB DEPLOYER ===\n")

    ami_choice = input("Choose AMI (ubuntu / amazon-linux): ").strip().lower()
    ami_options = {
        "ubuntu": "ami-02bf8ce06a8ed6092",         # Ubuntu AMI for us-east-2
        "amazon-linux": "ami-00399ec92321828f5"    # Amazon Linux AMI for us-east-2
    }

    if ami_choice in ami_options:
        ami = ami_options[ami_choice]
    else:
        print("Invalid AMI choice. Defaulting to ubuntu.")
        ami = ami_options["ubuntu"]

    instance_type = input("Choose instance type (t3.small / t3.medium): ").strip()
    if instance_type not in ["t3.small", "t3.medium"]:
        print("Invalid instance type. Defaulting to t3.small.")
        instance_type = "t3.small"

    lb_name = input("Enter Load Balancer name: ").strip()
    if not lb_name or not lb_name.replace("-", "").isalnum() or lb_name.endswith("-"):
        print("Invalid Load Balancer name. Using 'default-lb'.")
        lb_name = "default-lb"

    return {
        "ami": ami,
        "instance_type": instance_type,
        "region": "us-east-2",
        "availability_zone_a": "us-east-2a",
        "availability_zone_b": "us-east-2b",
        "load_balancer_name": lb_name
    }

def render_template(context):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('main.tf.j2')
    output = template.render(context)
    with open("main.tf", "w") as f:
        f.write(output)
    print("main.tf generated successfully.")

def run_terraform():
    print("Running Terraform...")
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        print("Terraform apply failed.")
        print(e)

def main():
    user_input = get_user_input()
    render_template(user_input)
    run_terraform()

if __name__ == "__main__":
    main()
