# ==============================================================================================================================
#                                           Honeypot                                                                           #
# ==============================================================================================================================

# Libraries

import socket

import threading

import logging

import paramiko

from Database.log_database import create_database

from server import HoneypotServer, connect_to_decoy, forward_data

# Host Key 

host_key = paramiko.RSAKey.generate(2048)

# Loggers

logging.basicConfig(

    format="%(asctime)s - %(levelname)s - %(message)s",

    level=logging.INFO,
    handlers=[
        logging.FileHandler("./Logs/honeypot.log"),
        logging.StreamHandler()
    ]
)

# Handle One Connection 

def handle_connection(client_socket, client_address):

    ip = client_address[0]
    logging.info(f"New connection from {ip}")

    transport = None

    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)

        server = HoneypotServer(ip)
        transport.start_server(server=server)

        channel = transport.accept(20)

        if channel is None:
            logging.warning(f"{ip} connected but never opened a channel")
            return

        logging.info(f"{ip} opened a shell channel")
        
        ssh_client, decoy_channel = connect_to_decoy()

        if decoy_channel is None:
            attacker_channel.send(b"Service unavailable\r\n")
            attacker_channel.close()
            return

        thread1 = threading.Thread(
            target=forward_data,
            args=(attacker_channel, decoy_channel, "attacker_to_decoy", ip)
        )

        thread2 = threading.Thread(
            target=forward_data,
            args=(decoy_channel, attacker_channel, "decoy_to_attacker", ip)
        )

        thread1.daemon = True
        thread2.daemon = True


        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()


    except Exception as e:
        logging.error(f"Error with {ip}: {e}")

    finally:
        try:
            if transport:
                transport.close()
        except:
            pass
        try:
            client_socket.close()
        except:
            pass

# Main Server 

def start_server():

    create_database()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 2222))
    server.listen(100)
    logging.info("Honeypot listening on port 2222...")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(
            target=handle_connection,
            args=(client_socket, client_address)
        )
        thread.daemon = True
        thread.start()

start_server()