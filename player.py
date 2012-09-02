class Player:
    #maybe we should distinguish between "intelligent" player and "unintelligent" bots?
    
    #does a player need to have the distinctino betweeen the cards on the table and the hole cards?
    #a Hand is the best hand, no distinction?
    def __str__(self):
        return "[Player: "+ self.playerid +" Pot: $"+ str(self.playerpot) +" Cards: "+ str(self.hand) +"]"
    
    

    def __init__(self, playerid, playerpot, game):
        self.playerid = playerid #unique ID number, needed for opponent evaluation?
        self.hand = []
        self.playerpot = playerpot
        self.game = game
       
    #receives the cards dealt to the player 
    def deal(self, hand):
        self.hand = hand
        
    def action_selection(self):
        #do stuff
        #raise / call / fold
        
        if self.hand.strength()[0] > 7:
            self.raise_bet(100)
            
    
        
    #bets an amount of money, i.e. puts it in the pot of the game
    def raise_bet(self, amount):
        self.game.pot += amount
        
        
    #calls the amount already betted
    def call_bet(self):
        
        
    def fold(self):
        print "! Player "+self.playerid+" folds !"
        self.game.fold_player(self)
        
    