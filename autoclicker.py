import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import threading
import time
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Listener, KeyCode

mouse = MouseController()

click_delay = 100  # ms
click_type_index = 0
click_types = ["Normal Click", "Double Click"]
hotkey = KeyCode(char='f6')
is_clicking = False
waiting_for_key = False

def click_loop():
    global is_clicking
    while True:
        if is_clicking:
            if click_types[click_type_index] == "Normal Click":
                mouse.click(Button.left, 1)
            else:
                mouse.click(Button.left, 2)
            time.sleep(click_delay / 1000.0)
        else:
            time.sleep(0.01)

def on_press(key):
    global hotkey, is_clicking, waiting_for_key
    if waiting_for_key:
        hotkey = key
        waiting_for_key = False
    elif key == hotkey:
        is_clicking = not is_clicking

# Start background click thread
threading.Thread(target=click_loop, daemon=True).start()
# Start hotkey listener
Listener(on_press=on_press).start()

# Setup ImGui window
if not glfw.init():
    exit()

window = glfw.create_window(400, 200, "Auto Clicker", None, None)
glfw.make_context_current(window)

imgui.create_context()
impl = GlfwRenderer(window)

# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    imgui.begin("Auto Clicker")

    changed, click_delay = imgui.slider_int("Click Delay (ms)", click_delay, 1, 1000)

    clicked, click_type_index = imgui.combo(
        "Click Type", click_type_index, click_types
    )

    imgui.text(f"Current Hotkey: {hotkey}")
    if imgui.button("Rebind Hotkey"):
        waiting_for_key = True

    imgui.text(f"Clicking: {'ON' if is_clicking else 'OFF'}")

    imgui.end()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)

impl.shutdown()
glfw.terminate()
