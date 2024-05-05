import os, sys, threading, socket, socketserver, itertools, http, random, string, re, subprocess, time, ipaddress
from threading import Thread
from http.server import SimpleHTTPRequestHandler

def bold(text):
    return "\033[1m{}\033[0m".format(text)

def underline(text):
    return "\033[4m{}\033[0m".format(text)

def gray_red(text):
    return "\x1b[38;2;193;66;66m{}\x1b[0m".format(text)

def red(text):
    return "\x1b[38;2;200;0;0m{}\x1b[0m".format(text)

def white(text):
    return "\x1b[38;2;255;255;255m{}\x1b[0m".format(text)

def gray(text):
    return "\x1b[38;2;132;132;132m{}\x1b[0m".format(text)

def interpolate_color(start_color, end_color, factor: float):
    return tuple([int(start_color[i] + (end_color[i] - start_color[i]) * factor) for i in range(3)])

def generate_gradient_colors(start_color, end_color, steps):
    colors = []
    for step in range(steps):
        factor = (step/float(steps-1)) if steps>1 else step
        colors.append(interpolate_color(start_color, end_color, factor))
    return colors

def apply_gradient(text, start_color=(200, 0, 40), end_color=(200, 10, 0)):
    text_lines = text.split('\n')
    colors = generate_gradient_colors(start_color, end_color, len(text_lines))
    colored_text = []
    for line, color in zip(text_lines, colors):
        color_code = f'\x1b[38;2;{color[0]};{color[1]};{color[2]}m'
        colored_text.append(color_code + line + '\x1b[0m')
    return '\n'.join(colored_text)

logo = f"""                                                                                 
                                                                             
                    ▒▓▓▓▓▓▓▒                                     
               ▓▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓                                
           ▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓                            
         ▓▓▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▓▓▓                          
        ▓▒▒▓▓▓▒▒▒░░░▒▒▒▒▒▒▒▒▒▒░░░▒▒▒▒▓▓▓▓                        
       ▓▒▒▒▓▓▒▒░░ ░░▒▒▒▒▒▒░░░    ░▒▒▓▓▓▓▓▓▓                      
      ▓▒▒▒▓▓▓▒░░  ░▒▒▒▒▒░░      ░▒▒▒▓▓▓███▓▓                     
     ▓▒▒▒▒▓▓▒▒░   ░▒▒▒▒▒░        ░▒▒▓█▓███▓▓▓                    
     ▓▒▒▒▒▓▒▒▒▒░ ░▒▒▒▒▒▒░░       ░░▒▓██████▓█▓██▓    {white("┳   ┳ ┏━━━┓ ┳━┓ ┏ ┏━━━┓ ┳   ┳ ┏━━━┓ ┳━━━┓ ┳━━━┓")}
    ▓▓▓▒▒▒▓▒▒▒▒░░░▒▒▒▒▒▒▒░▒▒▒▒▒▒▒▒▓▓▓██████▓███▓     {white("┃   ┃ ┃   ┃ ┃ ┃ ┃ ┃     ┃   ┃ ┃   ┃ ┃   ┃ ┃   ┃")}
    ▓███████▓▓████████████████▓▓▓▓▓██████▓████▓      {white("┗┓ ┏┛ ┣━━━┫ ┃ ┃ ┃ ┃  ━┳ ┃   ┃ ┣━━━┫ ┣━┳━┛ ┃   ┃")}
    ▓▓▓▓▓▓▓▓▓█▓▓▒▒▒▒▒▒▒▒▒▒▒░▒▒░░▒▓▓███████▓███▓      {white(" ┃ ┃  ┃   ┃ ┃ ┃ ┃ ┃   ┃ ┃   ┃ ┃   ┃ ┃ ┗┓  ┃   ┃")}
     ▒▓▓▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▒▒▓▓▓▓▓▓█████████▓██▓        {white(" ┗━┛  ┛   ┗ ┛ ┗━┻ ┗━━━┛ ┗━━━┛ ┛   ┗ ┻  ┻━ ┻━━━┛")}
      ▓█▓▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████▓███                                         S I L E N T I S
      ▓███▓▓▒▒▓▓██▓▓███▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓                     
       ▓██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓██▓▓▓▓▓▓▓▓                     
       ▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓█▓▓▓██▓▓▓▒                    
       ▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓                     
        ▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓                            
        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                 
         ▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓                                      
         ▓▓▓▓▒▒▒▒▒▒▒▓                                           
           ▓▒▒▒▒▒                                               
           ▒▒
"""

logo = apply_gradient(logo)

prompt = bold(underline("Vanguard")+" > ") 

n = red("[*]")

e = red("[!]")

i = red("[i]")

null_bar = [set(i) for r in range(1, len(['\n', '\t', ' '])+1) for i in itertools.combinations(['\n', '\t', ' '], r)]

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False
    
def validate_port(port_str):
    try:
        return 1<int(port_str)<65536
    except:
        return False

def flush():
    os.system('cls')
    
