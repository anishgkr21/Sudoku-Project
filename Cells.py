import pygame

cell_spacing = 60
group_size = 180
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
    def enable_selection(self):
        pygame.draw.rect(self.screen, (255, 0, 0), ((self.col * 60), (self.row * 60), cell_spacing+2, cell_spacing+2), 2)
        pygame.display.update()
    def disable_selection(self):
        pygame.draw.rect(self.screen, "blue", ((self.col * 60), (self.row * 60), cell_spacing + 2, cell_spacing + 2), 2)
        pygame.draw.line(self.screen, "blue", (0, group_size + 56 * 8), (Max_Width, group_size + 56 * 8), 6)
        pygame.display.update()
    def set_sketched_value(self, sketched_val):
        if self.val == "":
            pygame.draw.rect(self.screen, "blue",
                             pygame.Rect((self.col * 60) + 5, (self.row * 60) + 5, cell_spacing - 10,
                                         cell_spacing - 10))
            self.sketched_value = sketched_val
            value_font = pygame.font.Font(None, 60)
            value_surf = value_font.render(f'{self.sketched_value if ord("1") <= ord(self.sketched_value) <= ord("9") else "      "}', True, (30, 30, 30))
            self.value_rect = value_surf.get_rect(center=(cell_spacing // 2 + cell_spacing * self.col, cell_spacing // 2 + cell_spacing * self.row))
            self.screen.blit(value_surf, self.value_rect)
            pygame.display.update()

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), ((self.col * cell_spacing), (self.row * cell_spacing), cell_spacing, cell_spacing), 1)

        if self.val != "":
            value_font = pygame.font.Font(None, 60)
            value_surf = value_font.render(str(self.val), True, (255, 255, 255))
            value_rect = value_surf.get_rect(center=(cell_spacing // 2 + cell_spacing * self.col, cell_spacing // 2 + cell_spacing * self.row))
            self.screen.blit(value_surf, value_rect)
            self.value_rect = value_rect
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), ((self.col * cell_spacing), (self.row * cell_spacing), cell_spacing, cell_spacing))



    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return int(self.val)

    def __int__(self):
        return int(self.val)
