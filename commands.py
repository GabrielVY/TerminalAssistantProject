import subprocess
import webbrowser

# ================================
#  ADD YOUR CUSTOM COMMANDS HERE
# ================================

# You need the absolute path, and you also need to add the program to the prompt
programs = {
    "Chrome": "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "Steam": "D:\Programs\Steam\steam.exe",
    "Notepad": "notepad",
}

class Commands:

    # Debugging
    def print_text(self, msg):
        print('[Command] {}'.format(msg))

    # Change mouse color
    def change_mouse_color(self, color):
        pass

    # Open url in a new page
    def open_webpage(self, link):
        webbrowser.open(link, new=2)

    # Open any listed program
    def open_program(self, name):
        program = programs[name]
        subprocess.Popen([program])
