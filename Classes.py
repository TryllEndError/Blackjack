import random
import sys
import pygame

class Card:
    """Class for cards"""
    
    # Intrinsic variables
    width = 30
    height = 42
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def sprite(self, deckspritesheet):
        """Takes spritesheet of deck, returns sprite of card"""
        xoffset = self.width * (self.value - 1)
        yoffset = self.height * self.suit
        cardrect = pygame.Rect(xoffset, yoffset, self.width, self.height)
        cardimage = deckspritesheet.sprite(cardrect)
        return cardimage
        
    def ranktext(self):
        txt = ""
        if self.value == 1:
            txt = "A"
        elif self.value == 2:
            txt = "2"
        elif self.value == 3:
            txt = "3"
        elif self.value == 4:
            txt = "4"
        elif self.value == 5:
            txt = "5"
        elif self.value == 6:
            txt = "6"
        elif self.value == 7:
            txt = "7"
        elif self.value == 8:
            txt = "8"
        elif self.value == 9:
            txt = "9"
        elif self.value == 10:
            txt = "10"
        elif self.value == 11:
            txt = "J"
        elif self.value == 12:
            txt = "Q"
        elif self.value == 13:
            txt = "K"
        
        if self.suit == 0:
            txt += "h"
        elif self.suit == 1:
            txt += "s"
        elif self.suit == 2:
            txt += "d"
        elif self.suit == 3:
            txt += "c"
            
        return txt
        
class Hand:
    """Class for a list or set of cards (shoe, dealer, player, etc.)"""
    def __init__(self):
        self.cards = []
        
    def hasace(self):
        ace = False
        for c in self.cards:
            if c.value == 1:
                ace = True
        return ace
        
    def sum(self):
        total = 0
        for c in self.cards:
            if c.value <= 9:
                total += c.value
            else:
                total += 10
        return total
        
    
class InputHandler:
    """Class for handling user input"""
    def __init__(self):
        self.hit = False
        self.hitdown = False
        self.stand = False
        self.standdown = False
        self.split = False
        self.splitdown = False
        self.double = False
        self.doubledown = False
        self.exit = False
        self.exitdown = False
        self.betinc = False
        self.betincdown = False
        self.betdec = False
        self.betdecdown = False
        
    def keydown(self, key):
        if key == pygame.K_h:
            self.hitdown = True
        elif key == pygame.K_s:
            self.standdown = True
        elif key == pygame.K_d:
            self.doubledown = True
        elif key == pygame.K_ESCAPE:
            self.exitdown = True
        elif key == pygame.K_UP:
            self.betincdown = True
        elif key == pygame.K_DOWN:
            self.betdecdown = True
            
    def keyup(self, key):
        if key == pygame.K_h and self.hitdown == True:
            self.hit = True
        elif key == pygame.K_s and self.standdown == True:
            self.stand = True
        elif key == pygame.K_d and self.doubledown == True:
            self.double = True
        elif key == pygame.K_ESCAPE and self.exitdown == True:
            self.exit = True
        elif key == pygame.K_UP and self.betincdown == True:
            self.betinc = True
        elif key == pygame.K_DOWN and self.betdecdown == True:
            self.betdec = True
            
    def keyreset(self):
        self.hit = False
        self.stand = False
        self.split = False
        self.double = False
        self.exit = False
        self.betinc = False
        self.betdec = False
        
    def update(self):
        # not used - live update of keypresses (not event based)
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_ESCAPE]:
            self.exit = True
        if self.keys[pygame.K_h]:
            self.hit = True
        if self.keys[pygame.K_s]:
            self.stand = True
        if self.keys[pygame.K_p]:
            self.split = True
        if self.keys[pygame.K_d]:
            self.double = True
    
        
class LogicHandler:
    """Class that will contain the functions and flags needed to run the game"""
    def __init__(self):
        self.state = 0      # current gamestate
        # 0 - new hand
        # 1 - (if dealer ace) insurance
        # 2 - dealer BJ check
        # 3 - player's hand
        # 4 - split hand(s)
        # 5 - dealer's hand
        # 6 - hand resolution
        
        self.pocket = 100   # amount of chips the player has
        self.bet = 1        # the current bet amount
        self.paid = False   # whether the current hand has been paid out
        self.result = ""    # result text
        
    def dealcards(self, numcards, fromhand, tohand):
        while numcards > 0:
            card = fromhand.cards.pop(0)
            tohand.cards.append(card)
            numcards -= 1
    
    def newdeck(self, num):
        """Returns [num] amount of 52-card decks in one hand"""
        suits = [0, 1, 2, 3]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        deck = []
        while num > 0:
            for s in suits:
                for v in values:
                    deck.append(Card(s, v))
            num -= 1
        shufnum = random.randint(7,13)
        while shufnum > 0:
            random.shuffle(deck)
            shufnum -= 1
        
        return deck
        
    def stateaction(self, input, shoe, player, dealer):
        if self.state == 0:
            # new hand
            # reset payout flag
            self.paid = False
            # take bet from player
            self.pocket -= self.bet
            player.cards = []
            dealer.cards = []
            self.dealcards(2, shoe, player)
            self.dealcards(2, shoe, dealer)
            # if the dealer shows an ace, check for insurance
            if dealer.cards[-1].value == 1:
                self.state = 1
            # otherwise, continue to dealer blackjack check
            else:
                self.state = 2
        elif self.state == 1:
            # dealer shows an ace
            # TO DO = ASK FOR INSURANCE
            self.state = 2
        elif self.state == 2:
            # dealer blackjack check
            if dealer.sum() == 11 and dealer.hasace():
                self.state = 6
            else:
                self.state = 3
        elif self.state == 3:
            # player's hand
            #blackjack check
            if len(player.cards) == 2 and player.hasace() and player.sum() == 11:
                self.state = 6
            if input.stand:
                # stand
                self.state = 5
            elif input.hit:
                # hit
                self.dealcards(1, shoe, player)
                # check for bust
                if player.sum() > 21:
                    # bust
                    self.state = 6
            elif input.double and len(player.cards) == 2:
                # double bet if first two cards
                if self.bet > self.pocket:
                    self.bet += self.pocket
                    self.pocket = 0
                else:
                    self.bet += self.bet
                    self.pocket -= self.bet
                # double down - 1 card only
                self.dealcards(1, shoe, player)
                # check for bust
                if player.sum () > 21:
                    # bust
                    self.state = 6
                else:
                    self.state = 5
            elif input.split:
                # split if starting pair
                if len(player.cards) == 2 and player.cards[0].value == player.cards[1].value:
                    self.state = 4
        elif self.state == 4:
            # split hand(s)
            # TO DO = IMPLEMENT SPLIT HANDS
            pass
        elif self.state == 5:
            # dealer's hand
            if dealer.sum() > 16:
                # stand (hard 17+)
                self.state = 6
            elif dealer.sum() > 7 and dealer.hasace():
                # stand (soft 18+)
                self.state = 6
            else:
                # hit
                self.dealcards(1, shoe, dealer)
                # check for dealer bust
                if dealer.sum() > 21:
                    self.state = 6
        elif self.state == 6:
            # hand resolution
            p = player.sum()
            d = dealer.sum()
            # ace handling
            if p <= 11 and player.hasace():
                p += 10
            if d <= 11 and dealer.hasace():
                d += 10
            if p > 21:
                # player bust
                self.result = "BUST"
            elif d > 21:
                # dealer bust
                self.result = "WIN!"
            elif p > d:
                # player beats dealer
                self.result = "WIN!"
            elif d > p:
                # dealer beats player
                self.result = "LOSE"
            elif p == d:
                # push
                self.result = "PUSH"
            
            # DEBUG - payouts
            if self.result == "PUSH" and not self.paid:
                # pay back bet
                self.pocket += self.bet
                self.paid = True
            elif self.result == "WIN!"and not self.paid:
                # pay winnings
                if len(player.cards) == 2 and p == 21:
                    # blackjack: pay back bet and 3/2 winnings
                    self.pocket += (5 * self.bet ) / 2
                else:
                    # win: pay back bet and winnings
                    self.pocket += 2 * self.bet
                self.paid = True
            # deal new hand when player is ready
            if input.hit:
                self.state = 0
            elif input.betinc:
                self.bet += 1
                if self.bet > self.pocket:
                    self.bet = self.pocket
            elif input.betdec:
                self.bet -= 1
                if self.bet < 0:
                    self.bet = 0
        
    def update(self, input, shoe, player, dealer):
        """Main logic call"""
        # exit check
        if input.exit:
            pygame.quit()
            sys.exit()
        
        # main logic (game state)    
        self.stateaction(input, shoe, player, dealer)
        
        
        # reset input
        input.keyreset()
    
    
        
class DrawHandler(object):
    """class to handle drawing to the screen"""
    # intrinsic values
    yellow = (244, 206, 30)
    darkred = (80, 0, 0)
    chiptextloc = (15, 173)
    bettextloc = (15, 100)
    cardx = 150
    dealery = 50
    playery = 112
    midtextloc = (175, 94)
    dealertotalloc = (125, 59)
    playertotalloc = (125, 121)
    actiontextloc = (15, 19)
    
    def __init__(self, bgimage, deckspritesheet, deckbackimage):
        self.bg = bgimage
        self.deck = deckspritesheet
        self.back = deckbackimage
    
    def update(self, screen, font, logic, player, dealer):
        # draw background
        screen.blit(self.bg, (0, 0))
        # draw text
        drawtext = "Chips: " + str(logic.pocket)
        screen.blit(font.render(drawtext, 1, self.yellow), self.chiptextloc)
        drawtext = "Bet: " + str(logic.bet)
        screen.blit(font.render(drawtext, 1, self.yellow), self.bettextloc)
        psum = player.sum()
        if player.hasace() and psum == 11:
            drawtext = "21"
        if player.hasace() and psum <= 10:
            psum += 10
            drawtext = str(player.sum()) + "/" + str(psum)
        else:
            drawtext = str(psum)
        screen.blit(font.render(drawtext, 1, self.darkred), self.playertotalloc)
        if logic.state == 3:
            # display possible actions
            drawtext = "[H]it  [S]tand"
            if len(player.cards) == 2:
                drawtext += "  [D]ouble"
            screen.blit(font.render(drawtext, 1, self.darkred), self.actiontextloc)
        if logic.state == 6:
            # display possible actions
            drawtext = "[H] to deal, [up] to increase bet, [down] to decrease."
            screen.blit(font.render(drawtext, 1, self.darkred), self.actiontextloc)
            # display dealer's total
            dsum = dealer.sum()
            if dealer.hasace() and dsum <=11:
                dsum += 10
            drawtext = str(dsum)
            screen.blit(font.render(drawtext, 1, self.darkred), self.dealertotalloc)
            # display result (text) 
            drawtext = logic.result
            screen.blit(font.render(drawtext, 1, self.darkred), self.midtextloc)
        # draw player's cards
        cardcount = 0
        for c in player.cards:
            cardimage = c.sprite(self.deck)
            drawx = cardcount * 30 + self.cardx
            screen.blit(cardimage, (drawx, self.playery))
            cardcount += 1
        # draw dealer's cards
        cardcount = 0
        for d in dealer.cards:
            drawx = cardcount * 30 + self.cardx
            # while playing, first card is face down
            if cardcount == 0 and logic.state != 6:
                cardimage = self.back
            else:
                cardimage = d.sprite(self.deck)
            screen.blit(cardimage, (drawx, self.dealery))
            cardcount += 1
                

    
    
        
class SpriteSheet(object):
    """class for handling spritesheets"""
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        
    def sprite(self, rectangle):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image