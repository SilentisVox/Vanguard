import socket
import time
import threading

# Because multiple times these same methods are being called, the simpler approach
# is to include them in a more public-accessible area.

# The #1 issue with linux or another operating system alike, is the ability to send
# or prioritize sending packets fragmented. If we grab a chunk of data and the OS
# intended on sending more, we close off immediatetly, rather we should wait for the
# whole chunk of data to be sent over.

class Receiver:
        def __init__(
                self, 
                time_out: int = 2000
        ) -> None:
                self.time               = time_out

        def recvall(
                self, 
                client: socket.socket, 
                length: int
        ) -> bytes:
                data                    = b""
                timer                   = self.start_timer()

                while timer.is_alive() and length:
                        try:
                                recb    = client.recv(length)
                                length -= len(recb)
                                data   += recb
                                timer   = self.start_timer()

                        except BlockingIOError:
                                continue

                        except Exception:
                                break

                return data

        def peekall(
                self,
                client: socket.socket,
                length: int
        ) -> bytes:
                data                    = b""
                new                     = False
                timer                   = self.start_timer()

                while timer.is_alive() and len(data) < length:
                        try:
                                recb    = client.recv(length, socket.MSG_PEEK)
                                new     = recb != data
                                data    = recb

                        except BlockingIOError:
                                continue

                        except Exception:
                                break

                        if new:
                                timer   = self.start_timer()
                                new     = False

                return data

        def start_timer(self) -> threading.Thread:
                timer                   = threading.Thread(
                        target          = self.timeout,
                        daemon          = True
                )
                timer.start()

                return timer

        def timeout(self) -> None:
                seconds                 = self.time / 1000
                time.sleep(seconds)

        def recv(
                self,
                client: socket.socket, 
                length: int
        ) -> bytes:
                try:
                        return client.recv(length)

                except Exception:
                        return  b""

        def peek(
                self,
                client: socket.socket,
        ) -> bool:
                try:
                        return client.recv(1, socket.MSG_PEEK)

                except BlockingIOError:
                        return True

                except Exception:
                        return False