'''
This script is used to create IAM users from a csv file.

The format of the csv file will be:

UserID,IAM_User_Name,Programatic_Access,Console_Access,PolicyARN
1,user1,No,Yes,arn:aws:iam::aws:policy/AdministratorAccess
2,user2,Yes,No,arn:aws:iam::aws:policy/AmazonEC2FullAccess
3,user3,Yes,Yes,arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess

'''
import boto3
import string
import sys
import csv

from random import choice

class IAM_User():
    def __init__(self):
        self.iam_con = boto3.client("iam")

    def create_user(self, username):
        return self.iam_con.create_user(UserName = username)

    def create_login_profile(self, username, password):
        return self.iam_con.create_login_profile(UserName = username, Password = password, PasswordResetRequired = True)

    def create_access_key(self, username):
        return self.iam_con.create_access_key(UserName = username)

    def attach_policy(self, username, arn):
        return self.iam_con.attach_user_policy(UserName = username, PolicyArn = arn)

def random_password(size = 16, chars = string.ascii_letters + string.digits + "!@#$%^&*()"):
    return ''.join(choice(chars) for each_char in range(size))

def get_user_from_csv(csvfile):
    with open(csvfile, "r") as users:
        reader = csv.DictReader(users)
        user_list = list(reader)
        
    return user_list

def main():
    user = IAM_User()
    user_list = get_user_from_csv("user.csv")
    for each_user in user_list:
        username = each_user["IAM_User_Name"]
        password = random_password()
        policy_arn = each_user["PolicyARN"]
        try:
            user.create_user(username)
            print(f"The user {username} is created")
        except Exception as e:
            print(e)
            sys.exit(0)
        
        if each_user["Console_Access"] == "Yes":
            user.create_login_profile(username, password)
            print(f"The console login password is {password}")

        if each_user["Programatic_Access"] == "Yes":
            response = user.create_access_key(username)
            print(f"AccessKeyId = {response['AccessKey']['AccessKeyId']}\nSecretAccessKey = {response['AccessKey']['SecretAccessKey']}")
        
        user.attach_policy(username, policy_arn)
        print(f"This user has {policy_arn.split('/')[1]} permission")
        print("===========================================")

if __name__ == "__main__":
    main()