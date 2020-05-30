import pydealer as pd
from collections import Counter
class Player(pd.stack.Stack):
    def __init__(self, id):
        super().__init__()
        self.count = self.hash()
        self.id = id
        self.selected = []
    
    def hash(self):
        h = Counter()
        for card in self.cards:
            h[card.abbrev] += 1
        return h
    
    def select(self, game, index = None):
        can_select = self.can_select(game)
        if index is None:
            self.selected = []
            return
        if index not in can_select:
            return
        if index in self.selected:
            self.selected.remove(index)
        else:
            self.selected.append(index)
    def can_select(self, game):
        # 100% empty select case:
        # Not current player
        # already selected enough
        if game.state['id'] != self.id or len(self.selected) >= game.state['cards']:
            return []
        select_list = []
        # able to select double jokers for revolution
        if self.count["JKR"] == 2 and game.state['cards'] == 4:
            select_list += [len(self.cards)-1, len(self.cards)-2]
        # first select case:
        if len(self.selected) == 0:
            for i in range(len(self.cards)):
                # if last played is single joker, you can play 3 of spades
                if self.cards[i].abbrev == "3S" and game.state['cards'] == 1 and game.state['value'] == "Joker":
                    select_list.append(i)
                    return select_list
                # you can't select cards that you don't have enough to match the round
                if self.count[self.cards[i].abbrev] < game.state['cards']:
                    continue
                # you can't select cards that is less than or equal to the round
                if self.cards[i].le(game.cards[-1], ranks = game.rank) and game.state['value'] != "NEW":
                    continue
                # you can select position i
                select_list.append(i)
        # not first select case
        else:
            for i in range(len(self.cards)):
                # can select joker all the time except if last card is joker
                if self.cards[i].abbrev == "JKR" and game.state['value'] != "Joker":
                    select_list.append(i)
                    continue
                # can't select different value 
                if self.cards[i].value != self.cards[self.selected[0]].value:
                    continue
                select_list.append(i)
        select_list = list(set(select_list))
        return select_list.sort()
    
    def play(self, game):
        play_cards = self.cards.get_list(self.selected)
            
    

players = []
for i in range(4):
    players.append(Player(i))