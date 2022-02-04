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


# writes the commands to hunt and battle, adds some varied delay to prevent bot detection
def write():
    time.sleep(17 + (random.random() * 15))
    keyboard.write("owoh")
    keyboard.press("enter")
    time.sleep(1 + (random.random() * 3))
    keyboard.write("owob")
    keyboard.press("enter")


# writes the command to pray, adds some varied delay to prevent bot detection
def pray():
    time.sleep(2 + (random.random() * 5))
    keyboard.write("owopray")
    keyboard.press("enter")


# writes the command to pray, adds some varied delay to prevent bot detection
def reequip():
    time.sleep(3 + (random.random() * 2))
    keyboard.write("owo equip " + gems[gem_to_use])
    keyboard.press("enter")


# plays with the discord bot owo: hunting, battling, reequipping gems, and praying
def play(hunts_left):
    hunts = hunts_left
    find_discord()
    gem_sets_used = 0
    # display how many times the program has hunted so far and how many gems it's used
    layout = [[sg.Text(f"Gem sets used: {gem_sets_used}", key='used')],
              [sg.Text("Hunts using this gem set: 0", key='hunted')]]
    window = sg.Window("Owo bot player", layout)
    events, values = window.read(timeout=1)
    while True:
        for x in range(hunts):
            if events == sg.WIN_CLOSED:
                exit()
            write()
            if x % 15 == 0:
                pray()
            window['hunted'].update(value=f"Hunts using this gem set: {x+1}")
            events, values = window.read(timeout=1)

        reequip()
        gem_sets_used += 1
        window['used'].update(value=f"Gem sets used: {gem_sets_used}")

        # after finishing the first gem, set the number of hunts to the duration of the gem to use
        if hunts != gem_durations[gem_to_use]:
            hunts = gem_durations[gem_to_use]


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
                events, values = window.read(timeout=100)
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
            img = Image.open("discordMessage.PNG")
            xOffset, yOffset = img.size
            pos = (pos[0] + (xOffset/2), pos[1] + (yOffset/2))
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
