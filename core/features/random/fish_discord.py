import threading
import time
import pyautogui
import pywinauto
import pythoncom
import keyboard
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer

fishing_mode = False
fishing_detection_active = False
fishing_thread = None
detect_channel_thread = None
hotkey_registered = False
last_detected_channel = ""

TARGET_CHANNEL_NAME = "#🐟️⃗lake | Hence - Discord"

def toggle_fishing(window):
    global fishing_mode, fishing_detection_active, detect_channel_thread, hotkey_registered

    if not fishing_mode and not fishing_detection_active:
        window.voice.say("Activating fishing protocol.")
        window.showMinimized()
        fishing_detection_active = True
        window.fish_button.setText(get_fish_label())

        detect_channel_thread = threading.Thread(target=wait_for_correct_channel, args=(window,))
        detect_channel_thread.daemon = True
        detect_channel_thread.start()

        if not hotkey_registered:
            keyboard.add_hotkey('f8', lambda: toggle_fishing(window))
            hotkey_registered = True

    else:
        window.voice.say("Deactivating fishing protocol.")
        full_cancel(window)

def get_fish_label():
    return "Stop Fishing (F8)" if fishing_mode or fishing_detection_active else "Start Fishing (F8)"

def wait_for_correct_channel(window):
    global fishing_mode, fishing_detection_active, last_detected_channel

    pythoncom.CoInitialize()
    while fishing_detection_active:
        hwnd = get_discord_window()
        if hwnd:
            try:
                title = hwnd.window_text()

                if title != last_detected_channel:
                    print(f"[DEBUG] Current Window Title: {title}")
                    last_detected_channel = title

                if "lake" in title and "Hence" in title:
                    if not fishing_mode:
                        if is_discord_focused(hwnd):
                            window.voice.say("Channel verified. Starting fishing.")
                            start_fishing_loop(window)
                            fishing_mode = True
                        else:
                            print("[INFO] Waiting for Discord to be focused to start fishing...")
                else:
                    if fishing_mode:
                        window.voice.say("Wrong text channel. Pausing fishing.")
                        pause_fishing(window)
            except Exception as e:
                print(f"[ERROR] Cannot read window title: {e}")
        else:
            window.voice.say("Discord is not open to fish.")
            full_cancel(window)
            break

        time.sleep(1)

def start_fishing_loop(window):
    global fishing_thread

    fishing_thread = threading.Thread(target=fishing_loop, args=(window,))
    fishing_thread.daemon = True
    fishing_thread.start()

def fishing_loop(window):
    global fishing_mode

    pythoncom.CoInitialize()

    while fishing_mode:
        try:
            hwnd = get_discord_window()
            if hwnd:
                active_title = hwnd.window_text()

                if "lake" not in active_title or "Hence" not in active_title:
                    window.voice.say("Wrong text channel. Pausing fishing.")
                    pause_fishing(window)
                    break

                if not is_discord_focused(hwnd):
                    print("[INFO] Discord lost focus, pausing fishing.")
                    pause_fishing(window)
                    break

                time.sleep(0.5)
                pyautogui.typewrite("/fish")
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(3)
            else:
                window.voice.say("Discord is not open to fish.")
                pause_fishing(window)
                break

        except Exception as e:
            print(f"[ERROR] During fishing loop: {e}")
            window.voice.say("Fishing loop error.")
            pause_fishing(window)
            break

def pause_fishing(window):
    global fishing_mode

    fishing_mode = False

    def safe_pause():
        window.fish_button.setText(get_fish_label())

    QTimer.singleShot(0, safe_pause)

def full_cancel(window):
    global fishing_mode, fishing_detection_active, last_detected_channel

    fishing_mode = False
    fishing_detection_active = False
    last_detected_channel = ""

    def safe_full_cancel():
        window.fish_button.setText(get_fish_label())
        QMessageBox.warning(window, "Fishing Canceled", "Fishing stopped.")

    QTimer.singleShot(0, safe_full_cancel)

def get_discord_window():
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Discord.*")
        window = app.top_window()
        return window
    except Exception:
        return None

def is_discord_focused(hwnd):
    try:
        active_window = pywinauto.findwindows.find_element(active_only=True)
        return active_window.name == hwnd.element_info.name
    except Exception as e:
        print(f"[ERROR] Checking active window: {e}")
        return False
