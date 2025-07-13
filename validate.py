import boto3
import json

def get_latest_instance():
    ec2 = boto3.client('ec2')

    try:
        response = ec2.describe_instances(
            Filters=[{
                'Name': 'tag:Name',
                'Values': ['WebServer']
            }]
        )

        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)

        # Trier par date de lancement pour récupérer la plus récente
        instances = sorted(instances, key=lambda x: x['LaunchTime'], reverse=True)

        if not instances:
            return None

        instance = instances[0]
        return {
            "instance_id": instance["InstanceId"],
            "instance_state": instance["State"]["Name"],
            "public_ip": instance.get("PublicIpAddress", "N/A")
        }

    except Exception as e:
        print("EC2 validation error:", e)
        return None

def get_load_balancer_dns():
    elb = boto3.client('elbv2')
    try:
        response = elb.describe_load_balancers()
        lbs = response['LoadBalancers']
        if not lbs:
            return "N/A"

        # Prend le dernier load balancer créé
        lb = sorted(lbs, key=lambda x: x['CreatedTime'], reverse=True)[0]
        return lb['DNSName']

    except Exception as e:
        print("ELB validation error:", e)
        return "N/A"

def main():
    ec2_data = get_latest_instance()
    lb_dns = get_load_balancer_dns()

    if ec2_data:
        output = {
            "instance_id": ec2_data["instance_id"],
            "instance_state": ec2_data["instance_state"],
            "public_ip": ec2_data["public_ip"],
            "load_balancer_dns": lb_dns
        }

        with open("aws_validation.json", "w") as f:
            json.dump(output, f, indent=4)

        print("Validation complete. File 'aws_validation.json' created.")
        print(json.dumps(output, indent=4))
    else:
        print("No instance found.")

if __name__ == "__main__":
    main()
