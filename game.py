"""
Week 6: Memory Game
Author: Vu Tran
Website: http://vu-tran.com/

Memory game. Match cards and win!
"""

# Import modules

import simplegui, random

# Configurations

FRAME_WIDTH = 800
FRAME_HEIGHT = 800
SCOREBOARD_HEIGHT = 50
CARD_GUTTER_WIDTH = 5
NUM_PAIRS = 8
CARDS_PER_ROW = 4

class MemoryGame:
    def __init__(self, frame_width, frame_height, scoreboard_height, num_pairs, card_gutter_width, cards_per_row):
        # sets the options
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scoreboard_height = scoreboard_height
        self.num_pairs = num_pairs
        self.card_gutter_width = card_gutter_width
        self.cards_per_row = cards_per_row
        self.card_width = self.calculate_card_width()
        self.card_height = self.calculate_card_height()
        # creates a new frame
        self.frame = simplegui.create_frame("Memory Game", self.frame_width, self.frame_height)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.click)
        # creates the cards
        self.exposed = []
        self.create_cards(self.num_pairs)
        # creates the scoreboard
        self.scoreboard = Scoreboard(self.frame, self.frame_width, self.scoreboard_height)
        # creates the game buttons
        self.create_buttons()
        # creates a notification
        self.notification = Notification(self.frame, self.frame_width, self.frame_height)
    def start(self):
        """
        Starts the game frame
        """
        self.frame.start()
    def create_buttons(self):
        # create the reset button
        self.frame.add_button('Reset', self.reset)
    def calculate_card_width(self):
        """
        Calculates and returns the width for each card
        """
        return (self.frame_width - (self.card_gutter_width * self.cards_per_row) - self.card_gutter_width) / self.cards_per_row
    def calculate_card_height(self):
        """
        Calculates and returns the height for each card
        """
        # calculate the number of rows
        num_rows = (self.num_pairs * 2) / self.cards_per_row
        return ((self.frame_height - self.scoreboard_height) - (self.card_gutter_width * num_rows) - self.card_gutter_width) / num_rows
    def reset(self):
        """
        Resets the game
        """
        # resets the scoreboard
        self.scoreboard.reset()
        # resets the exposed list
        self.exposed = []
        # resets the notification
        self.notification.set_text("")
        self.notification.display = False
        # rebuilds the deck
        self.create_cards(self.num_pairs)
    def create_cards(self, num_pairs):
        """
        Creates the card pairs
        """
        self.cards = []
        # create a list of numbers
        card_list = range(num_pairs * 2)
        random.shuffle(card_list)
        # create a deck of cards
        for i in range(len(card_list)):
            card_num = card_list[i] % self.num_pairs
            # calculate the current column for the card
            card_col = i % self.cards_per_row
            # calculate the current row for the card
            card_row = i / self.cards_per_row
            # set the x, y position for the card
            start_x = ((self.card_width * card_col) + (card_col * self.card_gutter_width)) + self.card_gutter_width
            start_y = ((self.card_height * card_row) + (card_row * self.card_gutter_width)) + (self.card_gutter_width + self.scoreboard_height)
            # create a card at the given starting x/y coordinates with given width/height
            card = Card(self.frame, card_num, start_x, start_y, self.card_width, self.card_height)
            # add to the list of cards
            self.cards.append(card)
    def draw(self, canvas):
        """
        Draw handler for the frame
        """
        # draw the cards
        for i in range(len(self.cards)):
            # retrieve the card
            card = self.cards[i]
            # draws the card on the given canvas
            card.draw(canvas)
        # draw the scoreboard
        self.scoreboard.draw(canvas)
        # draw the notification
        self.notification.draw(canvas)
    def click(self, position):
        """
        Click handler for the frame
        """
        valid_click = False
        click_matched = False
        # iterate through all cards
        for i in range(len(self.cards)):
            # retrieve the card
            card = self.cards[i]
            # if not yet exposed or matched
            if not card.is_exposed and not card.is_matched:
                # if clicked position is within the card's range
                if card.is_clicked(position):
                    # set the flag
                    valid_click = True
                    # expose the given card
                    card.is_exposed = True
                    # add to the exposed list
                    self.exposed.append(card)
                    # check the exposed cards
                    this_matched = self.check_exposed()
                    if this_matched and not click_matched:
                        click_matched = True
        # if it's the 2nd click or if it was a matching click
        if len(self.exposed) == 2 or click_matched:
            # if the user did a valid click
            if valid_click is True:
                # increment tries
                self.scoreboard.tries += 1

    def check_exposed(self):
        """
        Checks all exposed cards to see if it matches each other

        Returns a boolean if there was a match
        """
        matched = False
        total_exposed = len(self.exposed)
        # let's just match the first 2 cards
        if total_exposed == 2:
            # if the first and second card's numbers matches
            if self.exposed[0].number == self.exposed[1].number:
                # make the given cards as matched
                self.exposed[0].is_matched = True
                self.exposed[1].is_matched = True
                # increment score
                self.scoreboard.score += 1
                # creates a new list
                self.exposed = []
                matched = True
        # if clicked on the 3rd card, reset the list and check it
        elif total_exposed > 2:
            # otherwise, remove the previous 2 cards
            self.exposed[0].is_exposed = False
            self.exposed[1].is_exposed = False
            # creates a new list
            self.exposed.pop(0)
            self.exposed.pop(0)
        # checks if the user has matched all pairs
        if self.scoreboard.score == self.num_pairs:
            self.notification.set_text("You won!")
            self.notification.show()
        return matched

class Card:
    def __init__(self, frame, number, start_x, start_y, width, height):
        self.frame = frame
        self.number = number
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.is_exposed = False
        self.is_matched = False
    def calculate_position(self):
        """
        Calculates the position for a card
        """
        top_left = [self.start_x, self.start_y]
        top_right = [self.start_x + self.width, self.start_y]
        bottom_right = [self.start_x + self.width, self.start_y + self.height]
        bottom_left = [self.start_x, self.start_y + self.height]
        return [
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ]
    def is_clicked(self, clicked_position):
        """
        Given a position (tuple), checks if the current card is clicked
        """
        # a card is clicked if the given position is within
        # the top left, and bottom right areas
        # retrieve the card's positions
        pos = self.calculate_position()
        # clicked X is between the left and right
        if clicked_position[0] >= pos[0][0] and clicked_position[0] <= pos[1][0]:
            # clicked Y is between the top and bottom
            if clicked_position[1] >= pos[0][1] and clicked_position[1] <= pos[3][1]:
                # card is clicked
                return True
        return False
    def draw(self, canvas):
        """
        Draws the card
        """
        # sets the card positions
        point_list = self.calculate_position()
        if self.is_exposed:
            self.draw_front(canvas, point_list)
        else:
            self.draw_back(canvas, point_list)
    def draw_front(self, canvas, point_list):
        """
        Draws the front of the card
        """
        # set the card's color
        card_color = "white"
        if self.is_matched == True:
            card_color = "gray"
        # draw the card
        canvas.draw_polygon(point_list, 1, card_color, card_color)
        # draw the text
        text = str(self.number)
        font_size = self.height / 2
        # retrieve the text width
        font_width = self.frame.get_canvas_textwidth(text, font_size, "serif")
        # calculate the text alignment
        font_align_horizontal = self.start_x + ((self.width - font_width) / 2)
        font_align_vertical = self.start_y + ((self.height + font_size) / 2)
        canvas.draw_text(text, [font_align_horizontal, font_align_vertical], font_size, "red", "serif")
    def draw_back(self, canvas, point_list):
        """
        Draws the back of the card
        """
        canvas.draw_polygon(point_list, 1, "green", "green")

class Scoreboard:
    def __init__(self, frame, width, height):
        # set configurations
        self.frame = frame
        self.width = width
        self.height = height
        # set default values
        self.font_size = 30
        # reset board
        self.reset()
    def reset(self):
        self.score = 0
        self.tries = 0
    def calculate_position(self, text, font_size):
        """
        Calculates the x/y position of the score text based on the frame's dimensions
        """
        text_width = self.frame.get_canvas_textwidth(text, font_size)
        return [
            (self.width - text_width) / 2,
            self.font_size
        ]
    def get_score_text(self):
        """
        Returns a string of the score / tries
        """
        return str(self.score) + " / " + str(self.tries)
    def draw(self, canvas):
        """
        Draws the score on the canvas
        """
        text = self.get_score_text()
        canvas.draw_text(text, self.calculate_position(text, self.font_size), self.font_size, "white", "serif")

class Notification:
    def __init__(self, frame, frame_width, frame_height):
        self.frame = frame
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.text = ""
        self.display = False
        self.font_size = 80
        self.font_color = "yellow"
    def calculate_position(self, text, font_size):
        """
        Calculates the x/y position of the notification based on the frame's dimensions
        """
        text_width = self.frame.get_canvas_textwidth(text, font_size)
        return [
            (self.frame_width - text_width) / 2,
            (self.frame_height + self.font_size) / 2
        ]
    def draw(self, canvas):
        """
        Draws the text on the canvas
        """
        if self.display:
            canvas.draw_text(self.text, self.calculate_position(self.text, self.font_size), self.font_size, self.font_color, "serif")
    def set_text(self, text):
        """
        Sets the notification's text
        """
        self.text = text
    def show(self):
        self.display = True
    def hide(self):
        self.display = False

# create a new game
game = MemoryGame(FRAME_WIDTH, FRAME_HEIGHT, SCOREBOARD_HEIGHT, NUM_PAIRS, CARD_GUTTER_WIDTH, CARDS_PER_ROW)

# starts the game
game.start()
