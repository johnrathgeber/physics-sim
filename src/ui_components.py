import pygame

class InputBox:
    def __init__(self, x, y, width, height, label, description, initial_value=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.description = description
        self.text = str(initial_value)
        self.active = False
        self.hovered = False
        self.valid = True

        self.bg_color = pygame.Color('white')
        self.border_inactive = pygame.Color('black')
        self.border_active = pygame.Color('black')
        self.border_invalid = pygame.Color('red')
        self.text_color = pygame.Color('black')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                char = event.unicode
                if self._is_valid_char(char):
                    self.text += char

    def _is_valid_char(self, char):
        if char.isdigit():
            return True
        if char == '.' and '.' not in self.text:
            return True
        if char == '-' and len(self.text) == 0:
            return True
        return False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen, label_font, input_font):
        label_surface = label_font.render(self.label, True, self.text_color)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))

        if not self.valid:
            border_color = self.border_invalid
            border_width = 2
        elif self.active:
            border_color = self.border_active
            border_width = 2
        else:
            border_color = self.border_inactive
            border_width = 1

        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, border_width)
        text_surface = input_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(left=self.rect.x + 5, centery=self.rect.centery)
        screen.blit(text_surface, text_rect)

    def get_value(self):
        try:
            return float(self.text) if self.text else None
        except ValueError:
            return None

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.enabled = True
        self.color_normal = pygame.Color(50, 150, 50)
        self.color_hover = pygame.Color(70, 180, 70)
        self.color_disabled = pygame.Color(100, 100, 100)
        self.text_color = pygame.Color('white')

    def is_clicked(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.enabled and self.rect.collidepoint(mouse_pos)
        return False

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font, mouse_pos):
        if not self.enabled:
            color = self.color_disabled
        elif self.is_hovered(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_normal

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.rect, 2)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Tooltip:
    def __init__(self, text, max_width=300):
        self.text = text
        self.max_width = max_width
        self.bg_color = pygame.Color(240, 240, 240, 230)
        self.border_color = pygame.Color('black')
        self.text_color = pygame.Color('black')
        self.padding = 10

    def draw(self, screen, x, y, font):
        words = self.text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + ' ', True, self.text_color)
            word_width = word_surface.get_width()

            if current_width + word_width <= self.max_width - 2 * self.padding:
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))

        line_height = font.get_height()
        tooltip_height = len(lines) * line_height + 2 * self.padding
        tooltip_width = self.max_width

        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height))
        tooltip_surface.fill(self.bg_color)

        pygame.draw.rect(tooltip_surface, self.border_color,
                        tooltip_surface.get_rect(), 1)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, self.text_color)
            tooltip_surface.blit(text_surface,
                                (self.padding, self.padding + i * line_height))

        screen.blit(tooltip_surface, (x, y))

class Dropdown:
    def __init__(self, x, y, width, height, options, selected_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options if options else ["default"]
        self.selected_index = min(selected_index, len(self.options) - 1)
        self.is_open = False
        self.hovered_option = -1

        self.bg_color = pygame.Color('white')
        self.border_color = pygame.Color('black')
        self.hover_color = pygame.Color(220, 220, 220)
        self.selected_color = pygame.Color(240, 240, 240)
        self.text_color = pygame.Color('black')
        self.arrow_size = 10

    def get_selected(self):
        return self.options[self.selected_index]

    def set_options(self, options, selected_index=0):
        self.options = options if options else ["default"]
        self.selected_index = min(selected_index, len(self.options) - 1)
        self.is_open = False

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return False, None

            if self.is_open:
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height * (i + 1),
                        self.rect.width,
                        self.rect.height
                    )
                    if option_rect.collidepoint(event.pos):
                        old_selected = self.selected_index
                        self.selected_index = i
                        self.is_open = False

                        if old_selected != i:
                            return True, self.options[i]
                        return False, None

                self.is_open = False
        return False, None

    def update(self, mouse_pos):
        self.hovered_option = -1
        if self.is_open:
            for i in range(len(self.options)):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height * (i + 1),
                    self.rect.width,
                    self.rect.height
                )
                if option_rect.collidepoint(mouse_pos):
                    self.hovered_option = i
                    break

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        selected_text = self.options[self.selected_index]
        text_surface = font.render(selected_text, True, self.text_color)
        text_rect = text_surface.get_rect(
            left=self.rect.x + 10,
            centery=self.rect.centery
        )
        screen.blit(text_surface, text_rect)

        arrow_x = self.rect.right - 25
        arrow_y = self.rect.centery
        if self.is_open:
            points = [
                (arrow_x, arrow_y + 3),
                (arrow_x - self.arrow_size // 2, arrow_y - 3),
                (arrow_x + self.arrow_size // 2, arrow_y - 3)
            ]
        else:
            points = [
                (arrow_x, arrow_y + 3),
                (arrow_x - self.arrow_size // 2, arrow_y - 3),
                (arrow_x + self.arrow_size // 2, arrow_y - 3)
            ]
            points = [(p[0], self.rect.centery + (self.rect.centery - p[1])) for p in points]

        pygame.draw.polygon(screen, self.text_color, points)

        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height * (i + 1),
                    self.rect.width,
                    self.rect.height
                )

                if i == self.hovered_option:
                    bg = self.hover_color
                elif i == self.selected_index:
                    bg = self.selected_color
                else:
                    bg = self.bg_color

                pygame.draw.rect(screen, bg, option_rect)
                pygame.draw.rect(screen, self.border_color, option_rect, 1)

                option_text = font.render(option, True, self.text_color)
                option_text_rect = option_text.get_rect(
                    left=option_rect.x + 10,
                    centery=option_rect.centery
                )
                screen.blit(option_text, option_text_rect)


class InputDialog:
    def __init__(self, title, prompt, screen_width, screen_height, width=400, height=200):
        self.width = width
        self.height = height
        self.title = title
        self.prompt = prompt
        self.input_text = ""
        self.input_box_height = 40
        self.max_length = 30

        self.bg_color = pygame.Color(240, 240, 240)
        self.border_color = pygame.Color('black')
        self.text_color = pygame.Color('black')
        self.input_bg = pygame.Color('white')
        self.active = True

        dialog_x = (screen_width - self.width) // 2
        dialog_y = (screen_height - self.height) // 2
        self.rect = pygame.Rect(dialog_x, dialog_y, self.width, self.height)

        button_width = 100
        button_height = 35
        button_y = dialog_y + self.height - button_height - 20

        ok_x = dialog_x + self.width // 2 - button_width - 10
        self.ok_button = Button(ok_x, button_y, button_width, button_height, "OK")

        cancel_x = dialog_x + self.width // 2 + 10
        self.cancel_button = Button(cancel_x, button_y, button_width, button_height, "Cancel")
        self.cancel_button.color_normal = pygame.Color(150, 50, 50)
        self.cancel_button.color_hover = pygame.Color(180, 70, 70)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    return "ok", self.input_text.strip()
            elif event.key == pygame.K_ESCAPE:
                return "cancel", ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < self.max_length:
                    char = event.unicode
                    if char.isprintable():
                        self.input_text += char

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.ok_button.is_clicked(mouse_pos, event):
                if self.input_text.strip():
                    return "ok", self.input_text.strip()

            if self.cancel_button.is_clicked(mouse_pos, event):
                return "cancel", ""

        return "none", ""

    def draw(self, screen, title_font, text_font, input_font, mouse_pos):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 3)

        title_surface = title_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 20)
        screen.blit(title_surface, title_rect)

        prompt_surface = text_font.render(self.prompt, True, self.text_color)
        prompt_rect = prompt_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 60)
        screen.blit(prompt_surface, prompt_rect)

        input_rect = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 100,
            self.rect.width - 60,
            self.input_box_height
        )
        pygame.draw.rect(screen, self.input_bg, input_rect)
        pygame.draw.rect(screen, self.border_color, input_rect, 2)

        input_surface = input_font.render(self.input_text, True, self.text_color)
        input_text_rect = input_surface.get_rect(left=input_rect.x + 10, centery=input_rect.centery)
        screen.blit(input_surface, input_text_rect)

        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_text_rect.right + 2
            pygame.draw.line(screen, self.text_color,
                           (cursor_x, input_rect.y + 8),
                           (cursor_x, input_rect.bottom - 8), 2)

        self.ok_button.draw(screen, text_font, mouse_pos)
        self.cancel_button.draw(screen, text_font, mouse_pos)

def draw_text_centered(screen, text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
