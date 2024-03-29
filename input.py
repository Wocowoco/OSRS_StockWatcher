import pygame
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (143, 241, 245)
# thx for skrx for an easy to understand solution
# https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame


class InputBox:
    def __init__(self, w, h, x, y, font, screen, text=""):
        self.active = False
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = black
        self.screen = screen
        self.amount = 0
        self.textarea = font.render(self.text, False, black)
        self.searches = []

    def draw(self):
        # draw a white rectangle to remove previous blitted value
        pygame.draw.rect(self.screen, white, self.rect)
        if len(self.text) > 0:
            # blit the new values to the screen
            self.screen.blit(self.textarea, (self.rect.x + 3, self.rect.y + 3))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

    def handle_event(self, ev):
        # check for mousepress in box
        if ev.type == pygame.MOUSEBUTTONDOWN:  # check for mousepress in searchbox
            if self.rect.collidepoint(ev.pos): # if true give an a visual indicator (box turns blue)
                self.active = True             # and set the state to active
                self.color = blue
            else:
                self.active = False            # else set to black and state to false
                self.color = black

        # check for keypress
        font1 = pygame.font.SysFont('arial', 15)
        if ev.type == pygame.KEYDOWN:
            if self.active is True:
                if ev.key == pygame.K_RETURN: # if key == enter: Save the value and clear searchbar
                    ret_val = self.text
                    self.text = ""
                    self.textarea = font1.render(self.text, False, black)
                    self.searches.append(Search(self.screen, ret_val, (50 + self.amount * (25 + 5)), self.rect.x))
                    self.amount += 1
                elif ev.key == pygame.K_BACKSPACE:
                    # remove the last value
                    self.text = self.text[:-1]
                    self.textarea = font1.render(self.text, False, black)
                else:
                    # add the pressed input to the input
                    self.text += ev.unicode
                    self.textarea = font1.render(self.text, False, black)

    def show_searches(self):
        for x in range(len(self.searches)):
            self.searches[x].draw()  # used to draw the searchresults

    def get_searches(self):
        if len(self.searches) > 0:
            ret_val = []
            for i in range(len(self.searches)):
                ret_val.append(self.searches[i].text)
            return ret_val


    def remove_searches(self, ev):
        x = 0
        while x < self.amount:
            if self.searches[x].events(ev) is True:
                self.searches.pop(x)  # remove the searchresult
                index = x
                while index < len(self.searches):  # move all searches after the removed search up to remove whitespaces
                    self.searches[index].rect.y = self.searches[index].rect.y - 30
                    self.searches[index].remove.y = self.searches[index].remove.y - 30
                    index += 1
                self.amount -= 1
            x += 1

    def check_search(self, i):
        # used to delete a value when its not valid
        self.searches.pop(i)
        self.amount -= 1


class Search:
    def __init__(self, screen, text, y, x):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(x, y, 150, 25)
        self.remove = pygame.Rect(x+150-25, y, 25, 25)

# draw the searches and the remove rectangle for each search
    def draw(self):
        font1 = pygame.font.SysFont('arial', 15)
        pygame.draw.rect(self.screen, black, self.rect, 1)
        textarea = font1.render(self.text, False, black)
        textwidth = textarea.get_width()
        if textwidth > self.rect.width:
            self.rect.width = textwidth + 6 + 25
            self.remove.x = 10 + self.rect.width-25
        self.screen.blit(textarea, (self.rect.x + 3, self.rect.y + 3))
        pygame.draw.rect(self.screen, black, self.remove, 2)
        pygame.draw.line(self.screen, red, (self.remove.x + 5, self.remove.y + 5), (self.remove.x + 18, self.remove.y + 18), 3)
        pygame.draw.line(self.screen, red, (self.remove.x + 5, (self.remove.y + 18)), ((self.remove.x + 18), self.remove.y + 5), 3)

    def events(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.remove.collidepoint(ev.pos): # if the remove rectangle is pressed go to remove search
                return True
