#=========================================================================================================================================
#                                                    Configuration                                                                       #
#=========================================================================================================================================


# Libraries

from dotenv import load_dotenv

import os


load_dotenv(dotenv_path="./Server/.env")


Decoy_ip        = os.getenv("Decoy_ip")
Decoy_port      = os.getenv("Decoy_port")
Decoy_username  = os.getenv("Decoy_username")
Decoy_password  = os.getenv("Decoy_password")
Honeypot_Port   = os.getenv("Honeypot_Port")