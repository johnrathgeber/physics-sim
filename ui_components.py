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

def draw_text_centered(screen, text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
