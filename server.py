#===================================================================================================================================================
#                                                   SSH Server                                                                                     #
#===================================================================================================================================================


# libraries

import logging

import paramiko

import random

from Database.log_database import log_attempt


# SSH Server Interface

class HoneypotServer(paramiko.ServerInterface):


    def __init__(self, client_ip):

        self.client_ip = client_ip
        self.attempts_counter = {}
        self.thresholds = {}


    def check_channel_request(self, king, chanid):

        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


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

        


