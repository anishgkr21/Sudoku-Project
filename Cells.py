import pygame

Cell_Spacing = 60
Group_Size = 180
Max_Width = 540


class Cell:
    def __init__(self, val, row, col, screen):
        self.val = val
        self.sketch_value = val
        self.row = row
        self.col = col
        self.screen = screen
        self.value_rect = None

    def set_cell_value(self, val):
        self.val = val

    def set_sketched_value(self, sketched_val):
        if self.val == 0:
            pygame.draw.rect(self.screen, "Cyan",
                             pygame.Rect((self.col * 60) + 5, (self.row * 60) + 5, Cell_Spacing - 10,
                                         Cell_Spacing - 10))
            self.sketched_value = sketched_val
            value_font = pygame.font.Font(None, 60)
            value_surf = value_font.render(
                f'{self.sketched_value if ord("1") <= ord(self.sketched_value) <= ord("9") else "      "}', True,
                (30, 30, 30))
            self.value_rect = value_surf.get_rect(
                center=(Cell_Spacing // 2 + Cell_Spacing * self.col, Cell_Spacing // 2 + Cell_Spacing * self.row))
            self.screen.blit(value_surf, self.value_rect)
            pygame.display.update()

    def draw(self):
        value_font = pygame.font.Font(None, 60)
        value_surf = value_font.render(f'{self.val if ord("1") <= ord(self.val) <= ord("9") else "      "}', True,
                                       (255, 255, 255))
        self.value_rect = value_surf.get_rect(center=(Cell_Spacing // 2 + Cell_Spacing * self.col, Cell_Spacing // 2 + Cell_Spacing * self.row))
        pygame.draw.rect(self.screen, "Blue", ((self.col * 60), (self.row * 60), Cell_Spacing + 2, Cell_Spacing + 2),
                         2)
        pygame.draw.line(self.screen, (0, 125, 200), (0, Group_Size + 56 * 8), (Max_Width, Group_Size + 56 * 8), 6)

        self.screen.blit(value_surf, self.value_rect)

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return int(self.val)

    def __int__(self):
        return int(self.val)
