#!/usr/bin/env python3
import json
from collections import defaultdict

def print_wrapped(text):
    width = 80
    index = width
    while text:
        while 0 <= index < len(text) and not text[index].isspace():
            index -= 1
        print(text[:index])
        text = text[index+1:]

def print_scene(scene, inventory):
    print_wrapped(scene.get('description', ''))
    if 'goto' in scene:
        input('press enter to continue...')
        return scene['goto']
    print()
    return prompt_options(scene, inventory)

def prompt_options(scene, inventory):
    visibleOptions = []
    index = 1
    for option in scene.get('options', []):
        showOption = True
        if 'if has' in option:
            invItem = option['if has']
            if invItem not in inventory or inventory[invItem]['amount'] == 0:
                showOption = False
        elif 'unless has' in option:
            invItem = option['unless has']
            if invItem in inventory or inventory[invItem]['amount'] != 0:
                showOption = False
        if showOption:
            print(index, option['description'])
            visibleOptions.append(option)
            index += 1
    selection = input('select an option: ')
    selection = int(selection) - 1
    return visibleOptions[selection]['goto']

def give(item, inventory):
    inventory[item]['amount'] += 1

def take(item, inventory):
    inventory[item]['amount'] -= 1

def main():
    with open('scenes.json') as f:
        scenes = json.load(f)

    with open('items.json') as f:
        items = json.load(f)

    inventory = defaultdict(lambda: {'amount': 0})
    next_scene = 'START'

    while next_scene != 'EXIT':
        scene = scenes[next_scene]
        if 'give' in scene:
            give(scene['give'], inventory)
        if 'take' in scene:
            take(scene['take'], inventory)
        next_scene = print_scene(scene, inventory)
        #print(inventory)
        print()


if __name__ == '__main__':
    main()

