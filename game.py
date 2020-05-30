'''
Game operation of revolution
'''
import pydealer as pd
from select import input_with_timeout as select_card

class Game():
    def __init__(self, rounds = 3):
        self.rounds = rounds
        self.curr_round = 1
        self.roles = {
            'beggar' : -1,
            'poor' : -1,
            'rich' : -1,
            'tycoon' : -1   
        }

        self.rank = {
            "values" : {
                "Joker" : 14,
                "2" : 13,
                "Ace" : 12,
                "King" : 11,
                "Queen" : 10,
                "Jack" : 9,
                "10" : 8,
                "9" : 7,
                "8" : 6,
                "7" : 5,
                "6" : 4,
                "5" : 3,
                "4" : 2,
                "3" : 1
            }
        }
        self.state = {
            'id' : -1,
            'skip' : False,
            'value' : '',
            'cards' : 0,
            'end' : False
        }
    def start(self, players):
        notFirst = self.curr_round != 1
        deck = pd.deck.Deck(jokers = notFirst, num_jokers = 2, ranks = self.rank)
        deck.shuffle()
        for i in range(len(players)):
            players[i].empty()
            players[i] = deck.deal(num = 13)
            if notFirst:
                if i == self.beggar or i == self.poor:
                    players[i] = deck.deal()
            players[i].sort(ranks = self.rank)
        if notFirst:
            try:
                print(players[self.tycoon])
                card_name = select_card("Tycoon choose your first card to swap", 10)
                card = players[self.tycoon].get(card_name)
                if len(card) == 0:
                    print("invalid card")
                    swap1 = players[self.tycoon].deal(end = 'bottom')
                else:
                    swap1 = card
            except:
                swap1 = players[self.tycoon].deal(end='bottom')
            try:
                print(players[self.tycoon])
                card_name = select_card("Tycoon choose your second card to swap", 10)
                card = players[self.tycoon].get(card_name)
                if len(card) == 0:
                    print("invalid card")
                    swap2 = players[self.tycoon].deal(end = 'bottom')
                else:
                    swap2 = card
            except:
                swap2 = players[self.tycoon].deal(end='bottom')
            players[self.tycoon].insert(players[self.beggar].deal(num = 2, end = 'top')).sort(ranks = self.rank)
            players[self.beggar].insert_list(swap1 + swap2).sort(ranks = self.rank)

def create_players():
    players = []
    for i in range(4):
        players.append(pd.deck.Deck().empty())