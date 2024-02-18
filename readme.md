# Ten-way Relay Control

This Python script provides a graphical user interface (GUI) for controlling a ten-way relay. The script uses the Tkinter library for the GUI and sockets for communication with the relay.

## Features

- Ten switches that can be toggled on and off.
- Each switch sends a message to the server when toggled, indicating its state.
- A text field for sending custom messages to the server.
- A "Get Live" button for requesting the current status of the relay.
- A text area for displaying messages received from the server.

## Usage

1. Ensure that you have Python and Tkinter installed on your machine.
2. Run the script with `python main.py`.
3. The GUI will appear, and you can interact with the switches and buttons.

## Note

This script assumes that the server is running on the same machine (localhost) and listening on port 14754. If your server is running on a different machine or port, you will need to modify the `client_socket.connect(('localhost', PORT))` line accordingly.