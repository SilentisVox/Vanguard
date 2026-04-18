from core.Receiver              import *
from core.Relationships         import *
from core.TextAssets            import *

import socket
import time
import random
import threading

# The server starts an attempts accepting any clients. If a client is accepted, they
# are saved and mapped to a thread for validation / initiation. When we validate new
# clients, we drop any that are not a real reverse-shell; Identifiers are saved with
# each client for differentiation. 

class TCPHandler:
        def __init__(self) -> None:
                self.server             = ServerComponents()
                self.clients            = {}
                self.manager            = None
                self.bind_address       = None
                self.bind_port          = None
                self.receiver           = Receiver()

        def start(self) -> bool:
                info("Starting TCP Handler at:   TCP://0.0.0.0:{}.".format(self.bind_port))
                local_bind              = socket.socket()

                try:
                        local_bind.bind((self.bind_address, self.bind_port))
                        local_bind.listen()

                except Exception as exception:
                        error("Exception: {}".format(exception))
                        return False

                self.server.shutdown    = False
                self.server.thread      = threading.Thread(
                        target          = self.accept,
                        args            = (local_bind,),
                        daemon          = True
                )
                self.server.thread.start()
                self.server.bind_agent  = local_bind
                self.server.running     = True
                self.manager            = threading.Thread(
                        target          = self.client_manager,
                        daemon          = True
                )
                self.manager.start()

                return self.server.thread.is_alive() and self.manager.is_alive()

        def accept(
                self, 
                listener: socket.socket
        ) -> None:
                while not self.server.shutdown:
                        try:
                                client, address = listener.accept()
                                client.setblocking(False)
                                client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b"\x01\x00\x00\x00\x00\x00\x00\x00")
                                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                        except Exception as exception:
                                error("Exception: {}".format(exception))
                                return

                        initiater = threading.Thread(
                                target  = self.initiate,
                                args    = (client,),
                                daemon  = True
                        )
                        initiater.start()

        def initiate(
                self,
                client: socket.socket
        ) -> None:
                if not self.validate(client):
                        client.close()
                        return
                        
                struct                  = ClientComponents()
                struct.connection       = client
                struct.identifier       = self.get_id()
                struct.ip               = client.getpeername()[0]
                struct.port             = client.getpeername()[1]
                struct.thread           = threading.Thread(
                        target          = struct.slake,
                        daemon          = True
                )
                struct.thread.start()

                self.clients[struct.identifier] = struct
                success("New client [{}] verified. (type 'sessions' for more info)".format(green(struct.identifier)), self.quick_check())

        def validate(
                self,
                client: socket.socket
        ) -> bool:
                incoming = self.receiver.peekall(client, 64).decode().upper()
                return "WINDOWS" in incoming or "LINUX" in incoming

        def get_id(self) -> str:
                return "-".join("".join(random.choices("ABCDEF0123456789", k=4)) for _ in range(3))

        def client_manager(self) -> None:
                while True:
                        self.track_clients()
                        time.sleep(1)

        def track_clients(self) -> None:
                for client_id, client in self.clients.items():
                        if client.status == "Lost":
                                continue

                        if client.in_use:
                                continue

                        if self.receiver.peek(client.connection):
                                continue

                        client.status = "Lost"

        def quick_check(self) -> bool:
                for client_id, client in self.clients.items():
                        if client.in_use:
                                return False

                return True

        def kill(self) -> None:
                for client_id, client in self.clients.items():
                        client.connection.shutdown(socket.SHUT_WR)

                self.server.running     = False
                self.server.shutdown    = True
                self.server.bind_agent.close()