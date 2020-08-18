import boto3

class EC2_Instance():
    def __init__(self):
        self.ec2_con_cli = boto3.client("ec2")

    def list_instances(self):
        response = self.ec2_con_cli.describe_instances()["Reservations"]
        for each_item in response:
            for each_instances in each_item["Instances"]:
                print("Instance ID: {}, Instance Type: {}, Launch time: {}, State: {}"
                .format(each_instances["InstanceId"], each_instances["InstanceType"], 
                each_instances["LaunchTime"].strftime("%d/%m/%Y"), each_instances["State"]["Name"]))
    
    def instance_waiter(self, state, instance_id):
        waiter = self.ec2_con_cli.get_waiter(state)
        waiter.wait(InstanceIds = instance_id)

    def start_instances(self, instance_id, state = "instance_running"):
        self.ec2_con_cli.start_instances(InstanceIds = instance_id)
        self.instance_waiter(state, instance_id)
        response = self.ec2_con_cli.start_instances(InstanceIds = instance_id)
        print("The instance {} is now {}".format(instance_id, response["StartingInstances"][0]["CurrentState"]["Name"]))

    def stop_instances(self, instance_id, state = "instance_stopped"):
        self.ec2_con_cli.stop_instances(InstanceIds = list(instance_id))
        self.instance_waiter(state, instance_id)
        response = self.ec2_con_cli.stop_instances(InstanceIds = instance_id)
        print("The instance {} is now {}".format(instance_id, response["StoppingInstances"][0]["CurrentState"]["Name"]))

    def terminate_instances(self, instance_id, state = "instance_terminated"):
        self.ec2_con_cli.terminate_instances(InstanceIds = instance_id)
        self.instance_waiter(state, instance_id)
        response = self.ec2_con_cli.terminate_instances(InstanceIds = instance_id)
        print("The instance {} is now {}".format(instance_id, response["TerminatingInstances"][0]["CurrentState"]["Name"]))

def perform_action(action):
        ec2 = EC2_Instance()
        ec2.list_instances()
        selection = input(f"Please enter the instance ID(s) for the instance(s) you want to {action}: ")
        instance_id = selection.split(",")
        print(f"{action.capitalize()}ing EC2...")
        if action == "start":
            ec2.start_instances(instance_id)
        elif action == "stop":
            ec2.stop_instances(instance_id)
        elif action == "terminate":
            ec2.terminate_instances(instance_id)
def main():
    while True:
        print("This script can do the following tasks: ")
        print("""
            1. Start 
            2. Stop
            3. Terminate
            4. Exit
            """)
        option = int(input("Which task would you like to perform: "))

        if option == 1:
            perform_action("start")
            
        elif option == 2:
            perform_action("stop")

        elif option == 3:
            perform_action("terminate")

        elif option == 4:
            print("Thanks for using the script!")
            break
        else:
            print("Please choose a valid option.")

main()
