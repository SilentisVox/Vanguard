from core.Receiver              import *
from core.Relationships         import *
from core.TextAssets            import *

import socket
import time
import random
import threading

class ClientHandler:
        def __init__(
                self, 
                client: socket.socket
        ) -> None:
                self.client             = client
                self.running            = True
                self.recv_thread        = None
                self.receiver           = Receiver()

        def set_up(self) -> None:
                self.client.in_use      = True
                self.recv_thread        = threading.Thread(
                        target          = self.recv,
                        daemon          = True
                )

        def begin_communication(self) -> None:
                info("Begininng communication. (type 'CTRL+C' to quit)")
                self.sprint(self.client.pending)
                self.client.pending = b""
                self.recv_thread.start()

                try:
                        while self.running:
                                self.client.connection.send((input() + "\n").encode())

                except KeyboardInterrupt:
                        info("Backgrounding client...")
                        self.thwart()

                except Exception as exception:
                        error("Exception: {}".format(exception))
                        self.thwart()

        def recv(self) -> None:
                while self.running:
                        if data := self.receiver.recv(self.client.connection, 1024).decode("utf-8", errors="replace"):
                                print(data, end="", flush=True)

        def sprint(self, data: bytes) -> None:
                print(data.decode("utf-8", errors="replace"), end="", flush=True)

        def thwart(self) -> None:
                self.running            = False
                self.client.in_use      = False