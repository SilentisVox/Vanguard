from core.Receiver      import *

import socket
import time

# One solution for organization of server components and client accessibility is to
# use classes. Classes offer public memory addresses that can offer ease of use and
# a "standardized" organization of components.

class ServerComponents:
        def __init__(self) -> None:
                self.bind_agent         = None
                self.running            = False
                self.shutdown           = False

class ClientComponents:
        def __init__(self) -> None:
                self.connection         = None
                self.identifier         = None
                self.ip                 = None
                self.port               = None
                self.thread             = None
                self.status             = "Active"
                self.in_use             = False
                self.pending            = b""
                self.receiver           = Receiver()

        # In case any data may continue to send, or data gets sent in between using
        # the individual clients. We acknowledge the data and save it when entering
        # a session with the client.

        def slake(self) -> None:
                while self.status == "Active":
                        time.sleep(1)

                        if self.in_use:
                                continue

                        if not self.peek():
                                continue

                        if self.status == "Lost":
                                break

                        self.pending   += self.receiver.recvall(self.connection, 1024)

        def peek(self) -> bool:
                try:
                        return self.connection.recv(1, socket.MSG_PEEK)

                except BlockingIOError:
                        return False

                except Exception:
                        self.connection.close()
                        self.status     = "Lost"
                        return False