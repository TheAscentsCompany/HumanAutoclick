import ctypes
import random
import time


MIN_DELAY_SECONDS = 0.500
MAX_DELAY_SECONDS = 0.700
CLICK_HOLD_MIN_SECONDS = 0.015
CLICK_HOLD_MAX_SECONDS = 0.035

VK_F6 = 0x75
VK_F8 = 0x77

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

user32 = ctypes.WinDLL("user32", use_last_error=True)


def was_key_pressed(vk_code: int) -> bool:
    """Return True once when the key has been pressed since the last check."""
    return bool(user32.GetAsyncKeyState(vk_code) & 0x0001)


def left_click() -> None:
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(random.uniform(CLICK_HOLD_MIN_SECONDS, CLICK_HOLD_MAX_SECONDS))
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def wait_with_hotkeys(seconds: float) -> str | None:
    end_time = time.perf_counter() + seconds

    while True:
        remaining = end_time - time.perf_counter()
        if remaining <= 0:
            return None

        if was_key_pressed(VK_F6):
            return "toggle"

        if was_key_pressed(VK_F8):
            return "quit"

        time.sleep(min(0.02, remaining))


def print_header() -> None:
    print("Autoclick Minecraft")
    print("-------------------")
    print("F6 : demarrer / arreter")
    print("F8 : quitter")
    print(f"Delai aleatoire : {MIN_DELAY_SECONDS * 1000:.0f}-{MAX_DELAY_SECONDS * 1000:.0f} ms")
    print()


def main() -> None:
    active = False
    click_count = 0
    print_header()

    while True:
        if was_key_pressed(VK_F6):
            active = not active
            print("Autoclick ACTIVE" if active else "Autoclick ARRETE")

        if was_key_pressed(VK_F8):
            print("Fermeture.")
            break

        if not active:
            time.sleep(0.03)
            continue

        left_click()
        delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
        click_count += 1
        print(f"Clic #{click_count} - delai: {delay * 1000:.0f} ms", flush=True)
        action = wait_with_hotkeys(delay)

        if action == "toggle":
            active = False
            print("Autoclick ARRETE")
        elif action == "quit":
            print("Fermeture.")
            break


if __name__ == "__main__":
    main()
