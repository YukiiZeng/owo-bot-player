import keyboard
import mouse
import PySimpleGUI as sg
import random
import time
from PIL import Image
from python_imagesearch.imagesearch import imagesearch

gems = {
    "Common": "51 65 72",
    "Uncommon": "52 66 73",
    "Rare": "53 67 74",
    "Epic": "54 68 75",
    "Mythic": "55 69 76",
    "Legendary": "56 70 77",
    "Fabled": "57 71 78"
}
gem_durations = {
    "Common": 25,
    "Uncommon": 25,
    "Rare": 50,
    "Epic": 75,
    "Mythic": 75,
    "Legendary": 100,
    "Fabled": 100
}

global gem_to_use
global pos
global gem_sets_used


# writes the given message after the given delay with variance to prevent bot detection
def write(message, delay, variance):
    time.sleep(delay + (random.random() * variance))
    keyboard.write(message)
    keyboard.press("enter")


# the layout displays how many times the program has hunted and how many gems it's used, will be updated as needed
def get_hunting_layout():
    return [[sg.Text(f"Gem sets used: 0", key='used')],
            [sg.Text("Hunts using this gem set: 0", key='hunted')]]


def hunt_battle_pray(num_hunts):
    write("owoh", 17, 15)
    write("owob", 1, 3)
    if num_hunts % 15 == 0:
        write("owopray", 2, 5)


def reequip(window):
    global gem_sets_used
    write("owo equip " + gems[gem_to_use], 3, 2)
    gem_sets_used += 1
    window['used'].update(value=f"Gem sets used: {gem_sets_used}")


def use_gem(hunts, window):
    events, values = window.read(timeout=1)
    for x in range(hunts):
        if events == sg.WIN_CLOSED:
            exit()

        hunt_battle_pray(x)
        window['hunted'].update(value=f"Hunts using this gem set: {x + 1}")
        events, values = window.read(timeout=1)


# plays with the discord bot owo: hunting, battling, reequipping gems, and praying
def play(hunts_left):
    global gem_sets_used
    find_discord()
    window = sg.Window("Owo bot player", get_hunting_layout())
    # finish off the rest of the current gem before using the given gem type
    use_gem(hunts_left, window)
    gem_sets_used = 0
    while True:
        reequip(window)
        use_gem(gem_durations[gem_to_use], window)


# sets the position of discord's text box
def set_pos():
    global pos
    pos = mouse.get_position()
    mouse.unhook_all()


# If it cannot find discord's message box, ask the user to try again or select it manually
def handle_not_found():
    layout = [[sg.Text("Unable to find discord, try again or select manually?")],
              [sg.Button('Try Again'), sg.Button('Select Manually')]]
    window = sg.Window('Find Discord', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == 'Try Again':
            # close the window, search again
            window.close()
            return False
        if event == 'Select Manually':
            # close the window, have the user click on discord
            window.close()
            layout = [[sg.Text('Left click on discord\'s text box.')]]
            window = sg.Window('Select Discord', layout)
            mouse.on_click(lambda: set_pos())
            while pos == [-1, -1]:
                window.read(timeout=100)
            window.close()
            return True


# find discord's text box to start typing in
def find_discord():
    global pos
    found = False
    while not found:
        pos = imagesearch("./discordMessage.png", precision=.8)
        if pos == [-1, -1]:
            if handle_not_found():
                found = True
        else:
            # get the center of the image
            img = Image.open("discordMessage.png")
            xOffset, yOffset = img.size
            pos = (pos[0] + (xOffset / 2), pos[1] + (yOffset / 2))
            found = True

    mouse.move(pos[0], pos[1], absolute=True)
    mouse.click('left')


# creates the startup window, which collects basic information such as what gems to use and
# how many hunts until it is necessary to reequip gems
def startup_window():
    global gem_to_use
    layout = [[sg.Text('What gems to use?')],
              [sg.Combo(['Common', 'Uncommon', 'Rare', 'Epic', 'Mythic', 'Legendary', 'Fabled'], readonly=True)],
              [sg.Text('How many hunts until reequipping?')],
              [sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]
    window = sg.Window('Owo Bot Setup', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            exit()
        if event == 'Ok':
            gem_to_use = values[0]
            window.close()
            return values


if __name__ == '__main__':
    hunts_remaining = int(startup_window()[1])
    play(hunts_remaining)
