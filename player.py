class Player:
    #maybe we should distinguish between "intelligent" player and "unintelligent" bots?
    
    #does a player need to have the distinctino betweeen the cards on the table and the hole cards?
    #a Hand is the best hand, no distinction?
    

    def __init__(self, playerid, hand, playerpot, game):
        self.playerid = playerid #unique ID number, needed for opponent evaluation?
        self.hand = hand #the Hand the player has,
        self.playerpot = playerpot
        self.game = game
        
    def __str__(self):
        return "[Player: "+ self.playerid +" Pot: $"+ str(self.playerpot) +" Cards: "+ str(self.hand) +"]"
    
    def action_selection(self):
        #do stuff
        #raise / call / fold