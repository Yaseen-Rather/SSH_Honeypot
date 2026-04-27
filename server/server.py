#=========================================================================================================================================
#                                                   SSH Server                                                                           #
#=========================================================================================================================================


# libraries

import logging

import paramiko

import random

from Database.log_database import log_attempt

from Server.server import Decoy_ip, Decoy_port, Decoy_username, Decoy_password

# Data Forwarding

def forward_data(source_channel, dest_channel, direction, attacker_ip):
    
    try:
        while True:
            data = source_channel.recv(1024)
            
            if not data:
                break

            if direction == "attacker_to_decoy":

                logging.info(f"Command from {attacker_ip}: {data.decode('utf-8', errors='ignore').strip()}")

            dest_channel.send(data)

    except Exception:
        pass



# SSH Server Interface

class HoneypotServer(paramiko.ServerInterface):


    def __init__(self, client_ip):

        self.client_ip = client_ip
        self.attempts_counter = {}
        self.thresholds = {}


    def check_channel_request(self, kind, chanid):

        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

    def check_auth_password(self, username, password):

        logging.info(f"Login attempt from {self.client_ip} | {username}:{password}")

        # If user is connecting for the first Time 

        if username not in self.attempts_counter:

            self.attempts_counter[username] = 0
            self.thresholds[username] = random.randint(2, 5)

        # increment the counter

        self.attempts_counter[username] += 1

        # Check threshold for the attempts 

        if self.attempts_counter[username] >= self.thresholds[username]:
            
            logging.info(f"Access granted to {self.client_ip} | {username}:{password}")
            log_attempt(self.client_ip, username, password, accepted=True)
            return paramiko.AUTH_SUCCESSFUL

        log_attempt(self.client_ip, username, password, accepted=False)
        return paramiko.AUTH_FAILED

        
# Connection to Decoy VM

def connect_to_decoy():

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=Decoy_ip,
            port=Decoy_port,
            username=Decoy_username,
            password=Decoy_password
        )

        decoy_channel = ssh_client.invoke_shell()
        logging.info(f"Connected to decoy vm at {Decoy_ip}")
        return ssh_client, decoy_channel

    except Exception as e:
        logging.error(f"Failed to connect to decoy vm: {e}")
        return None, None
