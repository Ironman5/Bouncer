"""
COMP.CS.100 Programming 1
Projekti: Graafinen käyttöliittymä
Tekijä: Mika Valtonen
Opiskelijanumero: 166364

Ulosheittäjä-noppapelin tavoitteena on kerätä pelimerkkejä ja välttyä
ulosheittämiseltä. Peli on 3-6 pelaajalle ja siinä tarvitaan arpakuution
lisäksi 12 pelimerkkiä jokaiselle pelaajalle.
Pelissä heitetään arpakuutiota ja verrataan silmälukua edellisen pelaajan
heittämään silmälukuun. Jos silmäluku on suurempi niin pelaaja saa edelliseltä
pelaajalta silmälukujen erotuksen määrän pelimerkkejä. Jos silmäluku on
pienempi niin pelaaja antaa edelliselle pelaajallle silmälukujen erotuksen
määrän pelimerkkejä. Jos silmäluvut ovat samat siirtyy vuoro suoraan
seuraavalle pelaajalle. Peli loppuu kun joku pelaajista joutuu luovuttamaan
enemmän pelimerkkejä kun hänellä on jäljellä. Pelaaja, jolla sillä hetkellä on
eniten pelimerkkejä, voittaa pelin.

"""
from tkinter import *
import random

IMAGE_FILES = ["1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif"]


class GUI:
    """
    This class models a graphical user interface (GUI).
    """

    def __init__(self):
        """
        Initializes the graphical user interface (GUI)
        """
        self.__mainwindow = Tk()
        self.__mainwindow.title("Ulosheittäjä")
        self.__mainwindow.columnconfigure((0, 1, 2, 3, 4, 5),
                                          weight=1,
                                          uniform="dices")
        self.__players = []
        self.__players_labels = []
        self.__dices_labels = []
        self.__points_labels = []
        self.__in_turn = 5

        # Create PhotoImage-objects of dices and store them in a list.
        self.__dice_images = []
        for image_file in IMAGE_FILES:
            self.__dice_images.append(PhotoImage(file=image_file))

        # Create players-labels
        self.__players_txt = Label(self.__mainwindow,
                                   text="Number of players: ")
        self.__players_txt.grid(row=0, column=0, columnspan=2,
                                padx=10, pady=10, sticky=E)

        # Create spinbox with default values 3 to 6
        self.__players_spinbox = Spinbox(self.__mainwindow)
        self.__players_spinbox['values'] = ('3', '4', '5', '6')
        self.__players_spinbox.grid(row=0, column=2, columnspan=2, sticky=W)

        # Create start game-button
        self.__start_button = Button(self.__mainwindow,
                                     text="Start game",
                                     command=self.start_game)
        self.__start_button.grid(row=0, column=4, sticky=W)

        # Create quit game-button
        Button(self.__mainwindow, text="Quit game",
               command=self.__mainwindow.destroy).grid(row=0, column=5,
                                                       padx=10, sticky=W)

        # Create instructions-label
        self.__instructions = Label(self.__mainwindow)

        # Create throw dice-button
        self.__throw_button = Button(self.__mainwindow,
                                     text="Throw dice",
                                     command=self.throw_dice)

        # Create winner-taxt
        self.__winner_txt = Label(self.__mainwindow)

        # initialize player- object and labels
        self.init_game()

        self.__mainwindow.mainloop()

    def init_game(self):
        """
        Initialize player-objects and create player name-, points- and
         dice-labels.
        """
        # Create player-objects
        for i in range(int(self.__players_spinbox.get())):
            dice = random.randint(1, 6)
            self.__players.append(Player("Player " + str(i + 1),
                                         self.__dice_images[dice - 1],
                                         dice))

        # Create player name-, points- and dice-labels
        for index, player in enumerate(self.__players):
            player_label = Label(self.__mainwindow, text=player.get_name())
            self.__players_labels.append(player_label)
            player_label.grid(row=2, column=index)
            points_label = Label(self.__mainwindow,
                                 text="Points: " +
                                      str(self.__players[index].get_points()))
            self.__points_labels.append(points_label)
            points_label.grid(row=3, column=index)
            dice_label = Label(self.__mainwindow,
                               image=self.__players[index].get_image())
            self.__dices_labels.append(dice_label)
            dice_label.grid(row=4, column=index, ipadx=10, ipady=10)

    def start_game(self):
        """
        Delete previous game and start new one.
        """
        # Disable the buttons that should not be clicked when the game is on.
        self.__players_spinbox.configure(state=DISABLED)
        self.__start_button.configure(state=DISABLED)

        # Clear text if exist
        self.__winner_txt.grid_forget()

        # Delete player- objects
        for player in self.__players:
            del player
        self.__players.clear()

        # Delete grids and create new lists
        for player in self.__players_labels:
            player.grid_forget()
        self.__players_labels = []

        for dice in self.__dices_labels:
            dice.grid_forget()
        self.__dices_labels = []

        for points in self.__points_labels:
            points.grid_forget()
        self.__points_labels = []

        # initialize player- object and labels
        self.init_game()

        # Saves players dices to the  list
        players_dice = []
        for player in self.__players:
            players_dice.append(player.get_dice())
        # The player with smallest dice starts the game
        self.__in_turn = players_dice.index(min(players_dice))

        # Show labels in GUI
        self.__instructions["text"] = "Player " + str(
            self.__in_turn + 1) + " starts the game."
        self.__instructions.grid(row=5, column=0, columnspan=2, sticky=E)
        self.__throw_button.grid(row=5, column=2)

    def throw_dice(self):
        """
        Throw players dice, update player-object and dice-label
        """
        dice = random.randint(1, 6)
        # Change the player's in turn picture and dice
        self.__players[self.__in_turn].set_image(self.__dice_images[dice - 1])
        self.__players[self.__in_turn].set_dice(dice)
        # Update dice-label
        self.__dices_labels[self.__in_turn].configure(
            image=self.__players[self.__in_turn].get_image())
        self.count_points()

    def count_points(self):
        """
        Calculates the points of a player and a previous player.
        Compare them and calculate new points.
        """
        player_dice = self.__players[self.__in_turn].get_dice()
        previous_player_dice = self.__players[self.__in_turn - 1].get_dice()

        # Compare players points and calculate new ones.
        if player_dice > previous_player_dice:
            self.__players[self.__in_turn].add_points(
                player_dice - previous_player_dice)
            self.__players[self.__in_turn - 1].subtract_points(
                player_dice - previous_player_dice)

        elif player_dice < previous_player_dice:
            self.__players[self.__in_turn - 1].add_points(
                previous_player_dice - player_dice)
            self.__players[self.__in_turn].subtract_points(
                previous_player_dice - player_dice)

        # Update points-labels
        self.__points_labels[self.__in_turn].configure(
            text="Points: " + str(self.__players[self.__in_turn].get_points()))
        self.__points_labels[self.__in_turn - 1].configure(
            text="Points: " + str(
                self.__players[self.__in_turn - 1].get_points()))

        self.check_game_results()

    def check_game_results(self):
        """
        Check game results and show winner.
        """
        player_points = self.__players[self.__in_turn].get_points()
        previous_player_points = self.__players[
            self.__in_turn - 1].get_points()

        # Game is over if player has less than zero points
        if player_points < 0 or previous_player_points < 0:
            # Create winner-labels
            points = []
            for player in self.__players:
                points.append(player.get_points())
            # Find out winner
            winner = points.index(max(points))
            # Create winner-label
            self.__winner_txt["text"] = "Player " + str(
                winner + 1) + " has won the game with " + str(
                max(points)) + " points."
            self.__winner_txt.grid(row=6, column=1, columnspan=3, sticky=W)

            # Disable and enable labels and buttoms.
            self.__throw_button.grid_forget()
            self.__instructions.grid_forget()
            self.__players_spinbox.configure(state=NORMAL)
            self.__start_button.configure(state=NORMAL)

        # Switch to the next player
        self.__in_turn = (self.__in_turn + 1) % len(self.__players)

        # Update instruction-label
        self.__instructions["text"] = "Player " + str(
            self.__in_turn + 1) + " in turn."


class Player:
    """
    This class models a players in bouncher-game.The attributes are:
    - player's name
    - image of the dice
    - number of dice (1 - 6)
    - player's points
    """

    def __init__(self, name, image, dice):
        self.__name = name
        self.__image = image
        self.__dice = dice
        self.__points = 12

    def get_name(self):
        """
        Return player's name
        :return: string, player's name
        """
        return self.__name

    def get_image(self):
        """
        Return image of dice
        :return: gif, image of dice
        """
        return self.__image

    def set_image(self, image):
        """
        Set new image
        :param image: gif, image of dice
        """
        self.__image = image

    def get_dice(self):
        """
        Return player's dice number
        :return: int, player's dice number
        """
        return self.__dice

    def set_dice(self, dice):
        """
        Set new dice number
        :param dice: int, new dice number
        """
        self.__dice = dice

    def get_points(self):
        """
        Return player's points.
        :return: int, player's points.
        """
        return self.__points

    def add_points(self, points):
        """
        Add points to player.
        :param points: int, added points.
        """
        self.__points += points

    def subtract_points(self, points):
        """
        Substract points from player.
        :param points: int, substracted points.
        """
        self.__points -= points


def main():
    GUI()


if __name__ == "__main__":
    main()
