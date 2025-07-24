import pygame as pg
import sys
import xml.etree.ElementTree as ET

# screen + style
screen_width = 320
screen_height = 240
font_size = 20
button_height = font_size + 4
background_color = (255, 255, 255)
highlight_color = (37, 165, 245)
font_color = (0, 0, 0)

# state
menu_history_stack = []
selected = 0

# parse XML
def load_menu_from_xml(xml_file):
    tree = ET.parse(xml_file)
    return tree.getroot()

# extract items from XML element
def get_menu_items(xml_element):
    items = []
    for item in xml_element.findall('item'):
        items.append({
            'label': item.attrib.get('label', 'Unnamed'),
            'action': item.attrib.get('action'),
            'filter': item.attrib.get('filter'),
            'submenu': item.find('submenu'),
            'element': item
        })
    return items

# main loop
def main():
    global selected

    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("mpPi")
    clock = pg.time.Clock()
    font = pg.font.Font('assets/Sans.ttf', font_size)

    # load root menu
    root_menu = load_menu_from_xml("menu.xml")
    current_menu = root_menu
    menu_items = get_menu_items(current_menu)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pg.K_RETURN:
                    item = menu_items[selected]
                    if item['submenu'] is not None:
                        # Push current menu to history
                        menu_history_stack.append((current_menu, selected))
                        current_menu = item['element'].find('submenu')
                        menu_items = get_menu_items(current_menu)
                        selected = 0
                    elif item['action']:
                        print(f"Running action: {item['action']}, filter: {item['filter']}")
                elif event.key == pg.K_LEFT:
                    # Go back
                    if menu_history_stack:
                        current_menu, selected = menu_history_stack.pop()
                        menu_items = get_menu_items(current_menu)

        # draw menu
        screen.fill(background_color)
        for i, item in enumerate(menu_items):
            if i == selected:
                pg.draw.rect(screen, highlight_color, (10, button_height + i*button_height, 300, 30))
            text = font.render(item['label'], True, font_color)
            screen.blit(text, (20, button_height + i*button_height))

        pg.display.flip()
        clock.tick(60)

# run
if __name__ == "__main__":
    main()
