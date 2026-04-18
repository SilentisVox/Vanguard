from core.Receiver      import *
from core.Relationships import *
from core.TextAssets    import *

import socket
import time
import random
import threading

class HTTPServer:
        def __init__(self) -> None:
                self.server             = ServerComponents()
                self.bind_address       = None
                self.bind_port          = None
                self.payload            = ""
                self.receiver           = Receiver()

        # "Serving" to a client entails allowing a client
        # to connect, verify it was a valid request, then
        # send the client data in HTTP format.

        # We bind and listen for a connection on a given
        # port. Oncle a client has connected, verify its 
        # a valid HTTP request, then send our payload.

        def start(self) -> bool:
                info("Starting HTTP Handler at: HTTP://0.0.0.0:{}.".format(self.bind_port))
                local_bind              = socket.socket()

                try:
                        local_bind.bind((self.bind_address, self.bind_port))
                        local_bind.listen()

                except Exception as exception:
                        # ERROR
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

                return self.server.thread.is_alive()

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

                info("Successful request to HTTP server.", True)

                response                = self.get_response()
                client.send(response.encode())
                client.close()

        # We sepcify the appropriate request look like
        # a standard GET / HTTP/1.1 this is the root of
        # HTTP for requesting information.

        def validate(self, client):
                correct_request         = b"GET / HTTP/1.1"
                data                    = self.receiver.recvall(client, 14)
                request                 = data[:14]

                return request == correct_request

        # Create a custom, valid HTTP response.

        def get_response(self):
                http_response           = "HTTP/1.0 200 OK"
                http_server             = "Server: Vanguard Server"
                date_now                = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
                http_date               = "Date: " + date_now
                http_content_type       = "Content-Type: application/octet-stream" # "Content-Type: text/html" ← For html streams.
                content_length          = str(len(self.payload) + 2)
                http_content_length     = "Content-Length: " + content_length
                http_last_modified      = "Last-Modified: " + date_now
                last_line               = "\r\n\r\n"

                http_header             = [
                        http_response,
                        http_server,
                        http_date,
                        http_content_type,
                        http_content_length,
                        http_last_modified,
                        last_line
                ]

                http_header             = "\r\n".join(http_header)
                full_response           = http_header + self.payload + "\r\n"

                return full_response

        def kill(self) -> None:
                self.server.running     = False
                self.server.shutdown    = True
                self.server.bind_agent.close()