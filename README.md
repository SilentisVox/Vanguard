# Vanguard

![image](https://github.com/SilentisVox/Vanguard/assets/165338136/7e26bbd9-3c2a-4bed-8c00-8b9d8cac1c53)

This project includes a robust backdoor and HTTP server setup, providing a detailed and customizable environment for network interactions and security testing. The core functionalities allow for command execution, session handling, and dynamic response generation for testing purposes.

## Prerequisites

Before you can run this project, you will need the following:
- Python 3.x installed on your machine
- Access to command-line or terminal
- Required Python libraries: `socket`, `threading`, `os`, `subprocess`, `random`, `re`, `string`

## Setup

To set up and run this project, follow these steps:

1. Ensure all required Python modules are installed. Most of them are built-in except for a few which might require installation via pip.
2. Clone the repository or download the source code to your local machine.
3. Navigate to the directory containing the script.

## Usage

Run the script using Python from the command line:

```bash
git clone https://github.com/SilentisVox/Vanguard
cd Vanguard
python vanguard.py
```

Once the script is running, it will start both the backdoor and HTTP servers as configured. You can interact with the system using the command-line interface provided by the script. Here are some commands you can use:

![image](https://github.com/SilentisVox/Vanguard/assets/165338136/0e3cafbf-a865-45f0-b057-aa191ad186c4)

- `help`: Displays available commands and options.
- `set [option]`: Change options, such as server addresses or script names.
- `start [server]`: Starts the specified server (http or backdoor).
- `kill [server]`: Stops the specified server.
- `generate [bin|script|shell]`: Generates a binary for injection, custom reverse shell powershell script, or hollowed reverse shell from scvhost.exe
- `sessions`: Displays all active backdoor sessions.
- `exit`: Exits the application.

### Features

- **Dynamic Command Execution**: Ability to dynamically execute commands based on user input.
- **Session Management**: Manage and interact with multiple backdoor sessions.
- **Customizable Settings**: Easily configure server settings and payloads through the command interface.
- **Secure Communication**: Implementations can be extended to include encrypted communications.
