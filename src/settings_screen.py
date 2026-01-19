import pygame
import src.board_vars as bv
from src.config import GameConfig, MULTIPLIER_METADATA
from src.ui_components import InputBox, Button, Tooltip, draw_text_centered, Dropdown, InputDialog

INPUT_BOX_WIDTH = 150
INPUT_BOX_HEIGHT = 35
VERTICAL_SPACING = 65
HEADER_Y = 150

BLUE_COL_X = bv.WIDTH // 6 - INPUT_BOX_WIDTH // 2
RED_COL_X = bv.WIDTH - bv.WIDTH // 6 - INPUT_BOX_WIDTH // 2
GLOBAL_COL_X = bv.WIDTH // 2 - INPUT_BOX_WIDTH // 2
GLOBAL_START_Y = bv.HEIGHT // 2

PRESET_DROPDOWN_Y = 220
PRESET_BUTTON_WIDTH = 120
PRESET_BUTTON_HEIGHT = 40
PRESET_DROPDOWN_WIDTH = 300
PRESET_DROPDOWN_HEIGHT = 40

def settings_loop(screen, clock):
    config = GameConfig()

    title_font = pygame.font.SysFont("Arial", 60, bold=True)
    header_font = pygame.font.SysFont("Arial", 40, bold=True)
    label_font = pygame.font.SysFont("Arial", 18)
    input_font = pygame.font.SysFont("Arial", 20)
    error_font = pygame.font.SysFont("Arial", 24)
    info_font = pygame.font.SysFont("Arial", 30)
    dropdown_font = pygame.font.SysFont("Arial", 18)

    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (80, 80, 80)
    RED = (193, 21, 21)
    BLUE = (118, 77, 230)
    BLACK = (0, 0, 0)

    input_boxes = {}
    active_box = None
    error_message = ""

    blue_multipliers = [k for k, v in MULTIPLIER_METADATA.items()
                       if v['category'] == 'blue_player']
    for i, key in enumerate(blue_multipliers):
        metadata = MULTIPLIER_METADATA[key]
        y_pos = HEADER_Y + i * VERTICAL_SPACING
        input_box = InputBox(
            BLUE_COL_X, y_pos, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
            metadata['label'], metadata['description'],
            config.get_multiplier(key)
        )
        input_boxes[key] = input_box

    red_multipliers = [k for k, v in MULTIPLIER_METADATA.items()
                      if v['category'] == 'red_player']
    for i, key in enumerate(red_multipliers):
        metadata = MULTIPLIER_METADATA[key]
        y_pos = HEADER_Y + i * VERTICAL_SPACING
        input_box = InputBox(
            RED_COL_X, y_pos, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
            metadata['label'], metadata['description'],
            config.get_multiplier(key)
        )
        input_boxes[key] = input_box

    global_multipliers = [k for k, v in MULTIPLIER_METADATA.items()
                         if v['category'] == 'global']
    for i, key in enumerate(global_multipliers):
        metadata = MULTIPLIER_METADATA[key]
        y_pos = GLOBAL_START_Y + i * VERTICAL_SPACING
        input_box = InputBox(
            GLOBAL_COL_X, y_pos, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
            metadata['label'], metadata['description'],
            config.get_multiplier(key)
        )
        input_boxes[key] = input_box

    start_button = Button(800, 1050, 300, 60, "START GAME")

    preset_dropdown_x = bv.WIDTH // 2 - PRESET_DROPDOWN_WIDTH // 2
    preset_dropdown = Dropdown(
        preset_dropdown_x,
        PRESET_DROPDOWN_Y,
        PRESET_DROPDOWN_WIDTH,
        PRESET_DROPDOWN_HEIGHT,
        config.list_presets()
    )

    save_button_x = preset_dropdown_x - PRESET_BUTTON_WIDTH - 20
    load_button_x = preset_dropdown_x + PRESET_DROPDOWN_WIDTH + 20
    delete_button_x = load_button_x + PRESET_BUTTON_WIDTH + 10

    save_preset_button = Button(
        save_button_x,
        PRESET_DROPDOWN_Y,
        PRESET_BUTTON_WIDTH,
        PRESET_BUTTON_HEIGHT,
        "Save As")
    load_preset_button = Button(
        load_button_x,
        PRESET_DROPDOWN_Y,
        PRESET_BUTTON_WIDTH,
        PRESET_BUTTON_HEIGHT,
        "Load")
    delete_preset_button = Button(
        delete_button_x,
        PRESET_DROPDOWN_Y,
        PRESET_BUTTON_WIDTH,
        PRESET_BUTTON_HEIGHT,
        "Delete")

    input_dialog = None
    dialog_mode = None

    tooltip = Tooltip("", max_width=350)
    show_tooltip = False
    tooltip_pos = (0, 0)
    tooltip_text = ""

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_dialog:
                    action, text = input_dialog.handle_event(event)
                    if action == "ok":
                        if dialog_mode == "save":
                            for key, box in input_boxes.items():
                                value = box.get_value()
                                if value is not None:
                                    config.multipliers[key] = value

                            config.save_preset(text)
                            error_message = f"Preset '{text}' saved successfully"
                            preset_dropdown.set_options(config.list_presets())
                            new_index = preset_dropdown.options.index(text)
                            preset_dropdown.selected_index = new_index
                        elif dialog_mode == "confirm_delete":
                            selected_name = preset_dropdown.get_selected()
                            config.delete_preset(selected_name)
                            error_message = f"Preset '{selected_name}' deleted successfully"
                            preset_dropdown.set_options(config.list_presets())
                            preset_dropdown.selected_index = 0
                        input_dialog = None
                        dialog_mode = None
                    elif action == "cancel":
                        input_dialog = None
                        dialog_mode = None
                    continue

                active_box = None
                for key, box in input_boxes.items():
                    if box.rect.collidepoint(event.pos):
                        active_box = key
                        box.active = True
                    else:
                        box.active = False

                dropdown_changed, selected_preset = preset_dropdown.handle_event(event, mouse_pos)

                if save_preset_button.is_clicked(mouse_pos, event):
                    input_dialog = InputDialog("Save Preset", "Enter preset name:", bv.WIDTH, bv.HEIGHT)
                    dialog_mode = "save"

                if load_preset_button.is_clicked(mouse_pos, event):
                    selected_name = preset_dropdown.get_selected()
                    data = GameConfig.load_preset(selected_name)
                    config.from_dict(data)
                    for key, box in input_boxes.items():
                        box.text = str(config.get_multiplier(key))
                        box.valid = True
                    error_message = f"Loaded preset: {selected_name}"

                if delete_preset_button.is_clicked(mouse_pos, event):
                    selected_name = preset_dropdown.get_selected()
                    input_dialog = InputDialog(
                        "Confirm Delete",
                        f"Delete preset '{selected_name}'?",
                        bv.WIDTH,
                        bv.HEIGHT
                    )
                    dialog_mode = "confirm_delete"

                if start_button.is_clicked(mouse_pos, event):
                    all_valid = True
                    error_fields = []

                    for key, box in input_boxes.items():
                        metadata = MULTIPLIER_METADATA[key]
                        value = box.get_value()

                        if value is None:
                            all_valid = False
                            box.valid = False
                            error_fields.append(metadata['label'])
                        else:
                            box.valid = True

                    if all_valid:
                        for key, box in input_boxes.items():
                            config.multipliers[key] = box.get_value()
                        return config
                    else:
                        error_message = f"Invalid values in: {', '.join(error_fields[:3])}"
                        if len(error_fields) > 3:
                            error_message += f" (+{len(error_fields) - 3} more)"

            if event.type == pygame.KEYDOWN:
                if input_dialog:
                    action, text = input_dialog.handle_event(event)

                    if action == "ok":
                        if dialog_mode == "save":
                            for key, box in input_boxes.items():
                                value = box.get_value()
                                if value is not None:
                                    config.multipliers[key] = value

                            config.save_preset(text)
                            error_message = f"Preset '{text}' saved successfully"
                            preset_dropdown.set_options(config.list_presets())
                            new_index = preset_dropdown.options.index(text)
                            preset_dropdown.selected_index = new_index

                        elif dialog_mode == "confirm_delete":
                            selected_name = preset_dropdown.get_selected()
                            config.delete_preset(selected_name)
                            error_message = f"Preset '{selected_name}' deleted successfully"
                            preset_dropdown.set_options(config.list_presets())
                            preset_dropdown.selected_index = 0

                        input_dialog = None
                        dialog_mode = None

                    elif action == "cancel":
                        input_dialog = None
                        dialog_mode = None

                elif active_box and active_box in input_boxes:
                    input_boxes[active_box].handle_event(event)
                    error_message = ""

        preset_dropdown.update(mouse_pos)

        show_tooltip = False
        for key, box in input_boxes.items():
            box.update(mouse_pos)
            if box.hovered and not box.active:
                show_tooltip = True
                tooltip_text = box.description
                tooltip_pos = (box.rect.x, box.rect.y + box.rect.height + 5)

        screen.fill(LIGHT_GRAY)
        draw_text_centered(screen, "GAME SETTINGS", 950, 60, title_font, BLACK)
        info_text_1 = "Values are relative multipliers (1.0 is default, 2.0 is double)."
        info_text_2 = "Exception: Bludgers Per Side is the actual count."
        draw_text_centered(screen, info_text_1, 950, 130, info_font, DARK_GRAY)
        draw_text_centered(screen, info_text_2, 950, 180, info_font, DARK_GRAY)
        draw_text_centered(screen, "BLUE PLAYER", BLUE_COL_X + 75, 100, header_font, BLUE)
        draw_text_centered(screen, "RED PLAYER", RED_COL_X + 75, 100, header_font, RED)
        draw_text_centered(screen, "GLOBAL SETTINGS", GLOBAL_COL_X + 75, GLOBAL_START_Y - 50,
                          header_font, BLACK)

        for box in input_boxes.values():
            box.draw(screen, label_font, input_font)

        preset_dropdown.draw(screen, dropdown_font)
        save_preset_button.draw(screen, dropdown_font, mouse_pos)
        load_preset_button.draw(screen, dropdown_font, mouse_pos)
        delete_preset_button.draw(screen, dropdown_font, mouse_pos)

        if show_tooltip:
            tooltip.text = tooltip_text
            tooltip.draw(screen, tooltip_pos[0], tooltip_pos[1], label_font)

        start_button.draw(screen, header_font, mouse_pos)

        if error_message:
            error_surface = error_font.render(error_message, True, RED)
            error_rect = error_surface.get_rect(center=(950, 1000))
            screen.blit(error_surface, error_rect)

        if input_dialog:
            input_dialog.draw(screen, header_font, label_font, input_font, mouse_pos)

        pygame.display.flip()
        clock.tick(30)

    return None
