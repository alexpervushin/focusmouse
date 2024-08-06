import pyautogui
import keyboard
import psutil
import win32gui
import win32process
import tkinter as tk
from tkinter import ttk
import json
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading

def get_window(process_name):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                if process.name().lower() == process_name.lower():
                    hwnds.append(hwnd)
            except psutil.NoSuchProcess:
                pass
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def move_mouse_to_window_center(process_name):
    try:
        window_hwnd = get_window(process_name)
        if window_hwnd:
            rect = win32gui.GetWindowRect(window_hwnd)
            center_x = (rect[0] + rect[2]) // 2
            center_y = (rect[1] + rect[3]) // 2
            pyautogui.moveTo(center_x, center_y)
            status_label.config(text=f"Mouse moved to the center of {process_name} window")
        else:
            status_label.config(text=f"{process_name} window not found")
    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")

def set_hotkey():
    new_hotkey = hotkey_entry.get()
    process_name = process_entry.get()
    if new_hotkey and process_name:
        if new_hotkey in hotkeys:
            keyboard.remove_hotkey(new_hotkey)
        hotkeys[new_hotkey] = process_name
        keyboard.add_hotkey(new_hotkey, lambda: move_mouse_to_window_center(process_name))
        status_label.config(text=f"Hotkey {new_hotkey} set for {process_name}")
        update_hotkey_list()
        save_config()
    else:
        status_label.config(text="Please enter a valid hotkey and process name")

def delete_hotkey():
    selection = hotkey_list.curselection()
    if selection:
        index = selection[0]
        hotkey = list(hotkeys.keys())[index]
        keyboard.remove_hotkey(hotkey)
        del hotkeys[hotkey]
        update_hotkey_list()
        save_config()
        status_label.config(text=f"Hotkey {hotkey} deleted")
    else:
        status_label.config(text="Please select a hotkey to delete")

def update_hotkey_list():
    hotkey_list.delete(0, tk.END)
    for hotkey, process in hotkeys.items():
        hotkey_list.insert(tk.END, f"{hotkey}: {process}")

def save_config():
    with open('config.json', 'w') as f:
        json.dump(hotkeys, f)

def load_config():
    global hotkeys
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            hotkeys = json.load(f)
        for hotkey, process in hotkeys.items():
            keyboard.add_hotkey(hotkey, lambda p=process: move_mouse_to_window_center(p))
        update_hotkey_list()

def get_running_programs():
    programs = []
    for proc in psutil.process_iter(['name']):
        try:
            programs.append(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(set(programs))

def select_program():
    program_window = tk.Toplevel(root)
    program_window.title("Select Program")
    
    search_frame = ttk.Frame(program_window)
    search_frame.pack(padx=10, pady=5, fill=tk.X)
    
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    
    program_listbox = tk.Listbox(program_window, width=50, height=20)
    program_listbox.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)
    
    all_programs = get_running_programs()
    
    def update_list(search_term):
        program_listbox.delete(0, tk.END)
        for program in all_programs:
            if search_term.lower() in program.lower():
                program_listbox.insert(tk.END, program)
    
    def on_search(*args):
        update_list(search_entry.get())
    
    search_entry.bind('<KeyRelease>', on_search)
    
    update_list('') 
    
    def on_select():
        selection = program_listbox.curselection()
        if selection:
            selected_program = program_listbox.get(selection[0])
            process_entry.delete(0, tk.END)
            process_entry.insert(0, selected_program)
            program_window.destroy()
    
    select_button = ttk.Button(program_window, text="Select", command=on_select)
    select_button.pack(pady=10)

def create_image():
    image = Image.new('RGB', (64, 64), color = (73, 109, 137))
    return image

def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def quit_window(icon, item):
    icon.stop()
    root.quit()

def run_tray():
    image = create_image()
    menu = Menu(MenuItem('Show GUI', show_window), MenuItem('Exit', quit_window))
    icon = Icon("focusmouse", image, "focusmouse", menu)
    icon.run()

def on_closing():
    root.withdraw()
    threading.Thread(target=run_tray, daemon=True).start()

root = tk.Tk()
root.title("focusmouse")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Enter hotkey:").grid(column=0, row=0, sticky=tk.W, pady=5)
hotkey_entry = ttk.Entry(frame, width=15)
hotkey_entry.grid(column=1, row=0, sticky=tk.W, pady=5)

ttk.Label(frame, text="Enter process name:").grid(column=0, row=1, sticky=tk.W, pady=5)
process_entry = ttk.Entry(frame, width=15)
process_entry.grid(column=1, row=1, sticky=tk.W, pady=5)

select_button = ttk.Button(frame, text="Select", command=select_program)
select_button.grid(column=2, row=1, sticky=tk.W, pady=5, padx=5)

set_button = ttk.Button(frame, text="Set Hotkey", command=set_hotkey)
set_button.grid(column=2, row=0, sticky=tk.W, pady=5, padx=5)

status_label = ttk.Label(frame, text="Set hotkeys for different programs")
status_label.grid(column=0, row=2, columnspan=4, sticky=tk.W, pady=10)

ttk.Label(frame, text="Current Hotkeys:").grid(column=0, row=3, sticky=tk.W, pady=5)
hotkey_list = tk.Listbox(frame, width=30, height=5)
hotkey_list.grid(column=0, row=4, columnspan=3, sticky=(tk.W, tk.E), pady=5)

delete_hotkey_button = ttk.Button(frame, text="Delete", command=delete_hotkey)
delete_hotkey_button.grid(column=3, row=4, sticky=(tk.W, tk.E), pady=5, padx=5)

hotkeys = {}

load_config()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()