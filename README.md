# focusmouse

focusmouse is a utility that allows you to quickly move your mouse cursor to the center of specific application windows using customizable hotkeys. This tool is particularly useful for multi-monitor setups or when working with multiple applications simultaneously.

## Features

- Set custom hotkeys for different applications
- Automatically move the mouse cursor to the center of the specified window
- Easy-to-use graphical interface
- System tray support for background operation
- Search and select from running programs
- Save and load hotkey configurations

## Installation

### Windows Users

1. Go to the [Releases](https://github.com/alexpervushin/focusmouse/releases) page.
2. Download the latest `focusmouse.exe` file.
3. Run the executable to start the application.

### For Developers

If you want to run the script from source:

1. Clone this repository:
   ```
   git clone https://github.com/alexpervushin/focusmouse.git
   ```
2. Change to the project directory:
   ```
   cd focusmouse
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the script:
   ```
   python main.py
   ```

## Usage

1. Launch the application.
2. Enter a hotkey combination (e.g., "ctrl+f1").
3. Enter the process name or click "Select" to choose from running programs.
4. Click "Set Hotkey" to save the configuration.
5. Use the set hotkey to move the mouse to the center of the specified window.

## System Requirements

- Windows 10 or later (Tested on Windows 11)
- Python 3.6+ (if running from source)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [keyboard](https://github.com/boppreh/keyboard)
- [psutil](https://github.com/giampaolo/psutil)
- [pywin32](https://github.com/mhammond/pywin32)
- [Pillow](https://python-pillow.org/)
- [pystray](https://github.com/moses-palmer/pystray)
