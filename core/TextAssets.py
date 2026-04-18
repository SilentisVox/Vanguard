import sys
import time
import datetime

RED                                     = "\x1B[38;2;200;000;000m"
YELLOW                                  = "\x1B[38;2;227;176;000m"
GREEN                                   = "\x1B[38;2;090;220;100m"
BLUE                                    = "\x1B[38;2;100;180;230m"
UNDER                                   = "\x01\x1B[4m\x02"
END                                     = "\x1B[0m"

class Banner:
        def __init__(self) -> None:
                self.SCREEN             = [" " * 27 * 5]
                self.BANNER             = [
                        " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " ", " ", " ", " ", " ", " ", " ", "\n",
                        " ", " ", "┬", " ", "┬", "┌", "─", "┐", "┬",
                        "┐", "┬", "┌", "─", "┐", "┬", " ", "┬", "┌",
                        "─", "┐", "┬", "─", "┐", "┬", "─", "┐", "\n",
                        " ", " ", "│", "┌", "┘", "├", "─", "┤", "│",
                        "│", "│", "│", " ", "┬", "│", " ", "│", "├",
                        "─", "┤", "├", "┬", "┘", "│", " ", "│", "\n",
                        " ", " ", "└", "┘", " ", "┴", " ", "┴", "│",
                        "└", "┘", "└", "─", "┘", "└", "─", "┘", "┴",
                        " ", "┴", "│", "└", " ", "┴", "─", "┘", "\n",
                        " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " ", " ", " ", " ", " ", " ", " ", "\n"
                ]
                self.NEXT_STEP          = {}

        def setup_step_calculator(self) -> None:
                PRE_EXISTENCE           = 800
                TO_SHINE                = 210
                IN_SHINE                = 10
                FROM_SHINE              = 210
                POST_EXISTENCE          = 400
        
                LIFE_BEFORE             = PRE_EXISTENCE
                LIFE_COMING             = LIFE_BEFORE + TO_SHINE
                LIFE_IN                 = LIFE_COMING + IN_SHINE
                LIFE_GOING              = LIFE_IN + FROM_SHINE
                LIFE_AFTER              = LIFE_GOING + POST_EXISTENCE


                for step in range(LIFE_BEFORE):
                        current         = step
                        color           = 0x7D8185 << 24
                        data            = color | (step + 1)

                        self.NEXT_STEP[step] = data

                for step in range(LIFE_BEFORE, LIFE_COMING):
                        current         = step - LIFE_BEFORE
                        color           = self.interpret_fade(0x7D8185, 0xB0B7BF, 210, current) << 24
                        data            = color | (step + 1)

                        self.NEXT_STEP[step] = data

                for step in range(LIFE_COMING, LIFE_IN):
                        current         = step - LIFE_COMING
                        color           = 0xF0F8FF << 24
                        data            = color | (step + 1)

                        self.NEXT_STEP[step] = data

                for step in range(LIFE_IN, LIFE_GOING):
                        current         = step - LIFE_IN
                        color           = self.interpret_fade(0xB0B7BF, 0x7D8185, 210, current) << 24
                        data            = color | (step + 1)

                        self.NEXT_STEP[step] = data

                for step in range(LIFE_GOING, LIFE_AFTER):
                        current         = step
                        color           = 0x7D8185 << 24
                        data            = color | (step + 1)

                        self.NEXT_STEP[step] = data


                self.NEXT_STEP[LIFE_AFTER] = 0x73787D << 24 | LIFE_AFTER

        def interpret_fade(
                self,
                color_start: int,
                color_end: int,
                total_steps: int,
                step: int
        ) -> int:
                if step + 1 == total_steps:
                        return color_end

                start_red               = (color_start & 0xFF0000) >> 16
                start_green             = (color_start & 0x00FF00) >> 8
                start_blue              = (color_start & 0x0000FF)

                end_red                 = (color_end & 0xFF0000) >> 16
                end_green               = (color_end & 0x00FF00) >> 8
                end_blue                = (color_end & 0x0000FF)

                difference_red          = start_red   - end_red
                difference_green        = start_green - end_green
                difference_blue         = start_blue  - end_blue

                amount_red              = int((difference_red   / total_steps) * (step + 1))
                amount_green            = int((difference_green / total_steps) * (step + 1))
                amount_blue             = int((difference_blue  / total_steps) * (step + 1))

                desired_red             = (start_red   - amount_red)   << 16
                desired_green           = (start_green - amount_green) << 8
                desired_blue            = (start_blue  - amount_blue)

                return desired_red | desired_green | desired_blue

        def colorify(
                self,
                character: str, 
                color: int
        ) -> str:
                red                     = (color & 0xFF0000) >> 16
                green                   = (color & 0x00FF00) >> 8
                blue                    = (color & 0x0000FF)

                return "\x1B[38;2;{};{};{}m{}\x1B[0m".format(red, green, blue, character)

        def setup_screen(self) -> None:
                HEIGHT                  = 5
                WIDTH                   = 27
                RESOLUTION              = HEIGHT * WIDTH
                TEMP                    = [""] * RESOLUTION

                for _ in range(27):
                        character               = self.BANNER[_]
                        step                    = (860 - (12 * 5)) - (12 * (27 - _))
                        data                    = self.NEXT_STEP[step]
                        colored                 = self.colorify(character, data >> 24)
                        TEMP[_]                 = (character, colored, data)

                for _ in range(27, 27 * 2):
                        character               = self.BANNER[_]
                        step                    = (860 - (12 * 4)) - (12 * ((27 * 2) - _))
                        data                    = self.NEXT_STEP[step]
                        colored                 = self.colorify(character, data >> 24)
                        TEMP[_]                 = (character, colored, data)

                for _ in range(27 * 2, 27 * 3):
                        character               = self.BANNER[_]
                        step                    = (860 - (12 * 3)) - (12 * ((27 * 3) - _))
                        data                    = self.NEXT_STEP[step]
                        colored                 = self.colorify(character, data >> 24)
                        TEMP[_]                 = (character, colored, data)

                for _ in range(27 * 3, 27 * 4):
                        character               = self.BANNER[_]
                        step                    = (860 - (12 * 2)) - (12 * ((27 * 4) - _))
                        data                    = self.NEXT_STEP[step]
                        colored                 = self.colorify(character, data >> 24)
                        TEMP[_]                 = (character, colored, data)

                for _ in range(27 * 4, 27 * 5):
                        character               = self.BANNER[_]
                        step                    = (860 - (12 * 1)) - (12 * ((27 * 5) - _))
                        data                    = self.NEXT_STEP[step]
                        colored                 = self.colorify(character, data >> 24)
                        TEMP[_]                 = (character, colored, data)

                self.SCREEN                  = TEMP

        def update_screen(self) -> None:
                LOCAL_SCREEN            = self.SCREEN[:]
                HEIGHT                  = 5
                WIDTH                   = 27
                RESOLUTION              = HEIGHT * WIDTH
                TEMP                    = [""] * RESOLUTION

                for index, item in enumerate(LOCAL_SCREEN):
                        character       = item[0]
                        colored         = item[1]
                        data            = item[2]

                        step            = data & 0xFFFF
                        next_data       = self.NEXT_STEP[step]
                        next_color      = self.colorify(character, next_data >> 24)
                        TEMP[index]     = (character, next_color, next_data)

                self.SCREEN             = TEMP

        def display(self) -> None:
                LOCAL_SCREEN            = self.SCREEN[:]
                DISPLAY                 = ""

                for ITEM in LOCAL_SCREEN:
                        COLORED                 = ITEM[1]
                        DISPLAY                += COLORED

                sys.stdout.write(DISPLAY)
                sys.stdout.write("\x1B[5A\x1B[27D")

        def qp(self) -> None:
                LOCAL_SCREEN            = self.SCREEN[:]
                DISPLAY                 = ""

                for ITEM in LOCAL_SCREEN:
                        COLORED                 = ITEM[1]
                        DISPLAY                += COLORED

                sys.stdout.write(DISPLAY)
                sys.stdout.write("\x1B[1A\x1B[18C")
                sys.stdout.write(self.colorify("silentis\n\n", 0xFFFFFF))

def bannerfy() -> None:
        banner = Banner()
        banner.setup_step_calculator()
        banner.setup_screen()

        cursor_off()

        for _ in range(500):
                time.sleep(0.0012)
                banner.update_screen()
                banner.display()

        banner.qp()
        cursor_on()

def get_help():
        menu                            = """
        \r Command        Description
        \r --------------------------------------------------------------
        \r
        \r start     [+]  Starts a given service with parameters.
        \r kill      [+]  Kills a given service.
        \r generate  [+]  Generates a payload to the handler specified.
        \r options        Displays current services running.
        \r sessions       Displays all sessions with clients.
        \r session   [+]  Begin communication with a given client.
        \r end       [+]  Kills a connection with a specified client.
        \r eradicate      Kills all current sessions.
        \r help      [+]  Displays this menu or command details.
        \r clear          Clears the terminal window.
        \r exit           Exits Vanguard.

        """

        sys.stdout.write(menu)
        sys.stdout.flush()

def get_command_help(description):
        menu                            = """
        \r Command               Description
        \r --------------------------------------------------------------
        \r {}\n""".format(description)

        sys.stdout.write(menu)
        sys.stdout.flush()

def jobs(
        tcp_server: object, 
        http_server: object
) -> None:
        job_list = """
        \r Jobs                       Status
        \r ----------------------------------
        \r"""

        job_info                        = " {}  {} \n"

        untcp_service                   = "TCP://{}:{}".format(tcp_server.bind_address, tcp_server.bind_port) + " " * 16
        tcp_service                     = untcp_service[:25]
        tcp_active                      = green("Started") if tcp_server.server.running else red("Stopped")
        tcp_info                        = job_info.format(
                tcp_service, 
                tcp_active
        )
        unhttp_service                  = "HTTP://{}:{}".format(http_server.bind_address, http_server.bind_port) + " " * 16
        http_service                    = unhttp_service[:25]
        http_active                     = green("Started") if http_server.server.running else red("Stopped")
        http_info                       = job_info.format(
                http_service, 
                http_active
        )

        job_list                       += tcp_info
        job_list                       += http_info
        job_list                       += "\n"
        sys.stdout.write(job_list)
        sys.stdout.flush()

def sessions(clients: dict) -> None:
        all_sessions                    = """     
        \r Client ID       IP Address       Status
        \r ---------------------------------------
        \r"""

        client_info = " {}  {}  {} \n"

        for client_id in clients.keys():
                client                  = clients[client_id]
                client_unendpoint       = client.ip + " " * 16
                client_endpoint         = client_unendpoint[:15]
                client_status           = green("Active") if client.status == "Active" else red("Lost")
                client_row              = client_info.format(
                        client_id,
                        client_endpoint,
                        client_status
                )
                all_sessions           += client_row

        all_sessions                   += "\n"
        sys.stdout.write(all_sessions)
        sys.stdout.flush()

def white(user_input: str) -> str:
        return "\x1B[38;2;255;255;255m{}\x1B[0m".format(user_input)

def red(user_input: str) -> str:
        return "\x1B[38;2;219;37;40m{}\x1B[0m".format(user_input)

def yorange(user_input: str) -> str:
        return "\x1B[38;2;219;165;22m{}\x1B[0m".format(user_input)

def green(user_input: str) -> str:
        return "\x1B[38;2;59;219;46m{}\x1B[0m".format(user_input)

def teal(user_input: str) -> str:
        return "\x1B[38;2;0;219;163m{}\x1B[0m".format(user_input)

def blue(user_input: str) -> str:
        return "\x1B[38;2;71;156;219m{}\x1B[0m".format(user_input)

def gray(user_input: str) -> str:
        return "\x1B[38;2;80;80;80m{}\x1B[0m".format(user_input)

def custom(user_input: str, color: tuple[int, int, int]) -> str:
        return "\x1B[38;2;{};{};{}m{}\x1B[0m".format(color[0], color[1], color[2], user_input)

def timey() -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

def info(user_input: str, prompt_needed: bool = False) -> None:
        sys.stdout.write("\r[{}] [{}] {}\n".format(teal(timey()), blue("INFO"), user_input))

        if prompt_needed:
                sys.stdout.write(prompt())

        sys.stdout.flush()

def debug(user_input: str, prompt_needed: bool = False) -> None:
        sys.stdout.write("\r[{}] [{}] {}\n".format(teal(timey()), yorange("DBUG"), user_input))

        if prompt_needed:
                sys.stdout.write(prompt())

        sys.stdout.flush()

def success(user_input: str, prompt_needed: bool = False) -> None:
        sys.stdout.write("\r[{}] [{}] {}\n".format(teal(timey()), green("DONE"), user_input))

        if prompt_needed:
                sys.stdout.write(prompt())

        sys.stdout.flush()

def error(user_input: str, prompt_needed: bool = False) -> None:
        sys.stdout.write(("\r[{}] [{}] {}\n".format(teal(timey()), red("FAIL"), user_input)))

        if prompt_needed:
                sys.stdout.write(prompt())

        sys.stdout.flush()

def prompt() -> str:
        return "\r{}Vanguard{}> ".format(UNDER, END)

def cursor_on():
        sys.stdout.write("\x1B[?25h")
        sys.stdout.flush()

def cursor_off():
        sys.stdout.write("\x1B[?25l")
        sys.stdout.flush()

if __name__ == "__main__":
        bannerfy()
