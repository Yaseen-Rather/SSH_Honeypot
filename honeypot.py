# ==============================================================================================================================
#                                           Honeypot                                                                           #
# ==============================================================================================================================

# Libraries

import socket

import threading

import logging

import paramiko

from Database.log_database import create_database

from server import HoneypotServer

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
        channel.send(b"Welcome to Ubuntu 22.04 TLS\r\n")
        channel.close()


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