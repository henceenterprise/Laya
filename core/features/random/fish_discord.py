# core/fishing.py

import threading
import time
import pyautogui
import keyboard

fishing_mode = False
fishing_thread = None
hotkey_thread = None
current_window = None  # Will hold reference to MainWindow

def toggle_fishing(window=None):
    global fishing_mode, fishing_thread, current_window

    if window:
        current_window = window  # Update reference in case hotkey called

    fishing_mode = not fishing_mode

    if fishing_mode:
        if current_window:
            current_window.voice.say("Fishing started.")
            current_window.fish_button.setText("Stop Fishing (F8)")
            current_window.showMinimized()
        fishing_thread = threading.Thread(target=fishing_loop)
        fishing_thread.daemon = True
        fishing_thread.start()
    else:
        if current_window:
            current_window.voice.say("Fishing stopped.")
            current_window.fish_button.setText("Start Fishing (F8)")

def fishing_loop():
    while fishing_mode:
        try:
            time.sleep(0.3)
            pyautogui.typewrite("/fish")
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(3)
        except Exception as e:
            print(f"[ERROR] During fishing: {e}")
            break

def get_fish_label():
    return "Stop Fishing (F8)" if fishing_mode else "Start Fishing (F8)"

def start_hotkey_listener(window):
    global hotkey_thread, current_window

    current_window = window

    def hotkey_worker():
        keyboard.add_hotkey('f8', lambda: toggle_fishing())
        keyboard.wait()  # keeps thread alive

    hotkey_thread = threading.Thread(target=hotkey_worker)
    hotkey_thread.daemon = True
    hotkey_thread.start()

def stop_hotkey_listener():
    try:
        keyboard.unhook_all_hotkeys()
    except Exception as e:
        print(f"[ERROR] Stopping hotkeys: {e}")
