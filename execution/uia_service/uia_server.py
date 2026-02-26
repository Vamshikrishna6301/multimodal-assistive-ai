import socket
import json
import pythoncom
from pywinauto import Desktop

HOST = "127.0.0.1"
PORT = 56789

desktop = None

INTERACTIVE_TYPES = {
    "Button",
    "MenuItem",
    "TabItem",
    "Hyperlink",
    "CheckBox",
    "RadioButton",
    "ComboBox"
}

MAX_DEPTH = 4
MAX_ELEMENTS = 50


# =====================================================
# ACTIVE WINDOW
# =====================================================

def get_active_window():
    try:
        return desktop.window(active_only=True)
    except Exception:
        return None


# =====================================================
# COLLECT INTERACTIVE ELEMENTS
# =====================================================

def collect_elements(window):
    elements = []

    def traverse(element, depth=0):
        if depth > MAX_DEPTH:
            return
        if len(elements) >= MAX_ELEMENTS:
            return

        try:
            children = element.children()
        except Exception:
            return

        for child in children:
            try:
                name = child.window_text()
                control_type = child.element_info.control_type

                if name and control_type in INTERACTIVE_TYPES:
                    elements.append(child)

                traverse(child, depth + 1)

            except Exception:
                continue

    traverse(window)
    return elements


# =====================================================
# READ SCREEN
# =====================================================

def read_screen():
    window = get_active_window()
    if not window:
        return {"status": "error", "message": "No active window"}

    try:
        title = window.window_text()
        elements = collect_elements(window)

        response_elements = []
        for idx, element in enumerate(elements, start=1):
            response_elements.append({
                "index": idx,
                "type": element.element_info.control_type,
                "name": element.window_text()
            })

        return {
            "status": "success",
            "window": title,
            "elements": response_elements
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# =====================================================
# CLICK BY INDEX
# =====================================================

def click_by_index(index):
    window = get_active_window()
    if not window:
        return {"status": "error", "message": "No active window"}

    elements = collect_elements(window)

    if not isinstance(index, int):
        return {"status": "error", "message": "Invalid index"}

    if index < 1 or index > len(elements):
        return {"status": "error", "message": "Invalid index"}

    target = elements[index - 1]

    try:
        target.invoke()
    except Exception:
        try:
            target.click_input()
        except Exception:
            return {"status": "error", "message": "Element not clickable"}

    return {"status": "success", "message": f"Clicked {target.window_text()}"}


# =====================================================
# CLICK BY NAME
# =====================================================

def click_by_name(name_query):
    window = get_active_window()
    if not window:
        return {"status": "error", "message": "No active window"}

    elements = collect_elements(window)

    if not name_query:
        return {"status": "error", "message": "Invalid name"}

    name_query = name_query.lower()

    for element in elements:
        element_name = element.window_text().lower()

        if name_query in element_name:
            try:
                element.invoke()
            except Exception:
                try:
                    element.click_input()
                except Exception:
                    return {"status": "error", "message": "Element not clickable"}

            return {
                "status": "success",
                "message": f"Clicked {element.window_text()}"
            }

    return {"status": "error", "message": "No matching element found"}


# =====================================================
# HANDLE REQUEST
# =====================================================

def handle_request(data):
    action = data.get("action")

    if action == "read_screen":
        return read_screen()

    if action == "click_index":
        return click_by_index(data.get("index"))

    if action == "click_by_name":
        return click_by_name(data.get("name"))

    return {"status": "error", "message": "Unknown action"}


# =====================================================
# SERVER
# =====================================================

def start_server():
    global desktop

    pythoncom.CoInitialize()
    desktop = Desktop(backend="uia")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("UIA Service Running on port", PORT)

    while True:
        conn, addr = server.accept()
        data = conn.recv(4096).decode()

        if not data:
            conn.close()
            continue

        try:
            request = json.loads(data)
            response = handle_request(request)
            conn.send(json.dumps(response).encode())
        except Exception as e:
            conn.send(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())

        conn.close()


if __name__ == "__main__":
    start_server()