# =======================================================================================================================
#                                           Honeypot                                                                    #
# =======================================================================================================================

# Libraries

import socket
import threading
import logging
import paramiko

# ── Host Key ────────────────────────────────────────────
host_key = paramiko.RSAKey.generate(2048)

# ── Logging Setup ───────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ── SSH Server Interface ────────────────────────────────
class HoneypotServer(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.attemps_counter = {}
        self.threshold = randon.randint(2, 5)

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):

    # first time seeing this username?
        if username not in self.attempts_counter:
            self.attempts_counter[username] = 0
            self.thresholds[username] = random.randint(2, 5)

        # increment counter
        self.attempts_counter[username] += 1

        # check against threshold
        if self.attempts_counter[username] >= self.thresholds[username]:
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED

# ── Handle One Connection ───────────────────────────────
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

# ── Main Server ─────────────────────────────────────────
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