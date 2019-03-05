
# Cribbage Helper 
# By: Christopher Olsen
# Version: 0.01 (in (somewhat-active) development)
# Copyright Notice: Copyright 2012 Christopher Olsen
# License: GNU General Public License, v3 (see LICENSE.txt)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from itertools import chain, combinations
from copy import copy
import random
# import sys

#### A program to find which cards to discard in a game of Cribbage
####
#### In its current state it does not take into account position or
#### whose crib it is
####
#### To demonstrate: run and type demonstrate() into the python shell
#### To enter a hand use find_keepers() and then follow the prompts
####
#### The expected values seem to be correct in a general sense but haven't
#### been checked (they seem to be on the high side)

################################################################################
################################ cards and deck ################################
################################################################################

class card(object):
    """ This is a card object, it has a rank, a value, a suit, and a display
        Value is an integer
        rank, suit and display are strings.
        """
    def __init__(self, rank=None, suit=None):
        ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        suits = ['D','H','C','S']
        assert type(rank) == str and rank in ranks
        assert type(suit) == str and suit in suits
        
        self.rank = rank
        self.suit = suit
        if rank == 'A':
            self.value = 1
        elif rank == 'T' or rank == 'J' or rank == 'Q' or rank == 'K':
            self.value = 10
        else:
            self.value = int(rank)
            
        self.display = rank + suit

    def __eq__(self, other):
        """ This overrides the == operator to check for equality """
        return self.__dict__ == other.__dict__


def make_deck():
    """ Creates a deck of 52 cards
        Returns the deck as a list
        """
    
    ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
    suits = ['D','H','C','S']
    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append(card(rank, suit))

    return cards


################################################################################
################################ various logic #################################
################################################################################


def get_rest_of_deck(hand):
    """ Takes a hand (a list of cards) and
        Returns a list of cards *not* in that hand
        """
    deck = make_deck()

    for h_card in hand:
        for d_card in deck:
            if h_card == d_card: # why we overrode __eq__ in the card object
                deck.remove(d_card)
    return deck

def get_rest_of_hand(four_hand, six_hand):
    """ Given a list of four cards of a six card hand,
        Returns a list of the two cards NOT in the four card hand
        """
    six_hand = copy(six_hand)
    for f_card in four_hand:
        for s_card in six_hand:
            if f_card == s_card:
                six_hand.remove(s_card)
    return six_hand
        
def enumerate_hands(hand):
    """ Given a hand of 6 cards, this method enumerates the possible four 
        card hands that can be made.
        Useful for choosing which cards to throw to the crib.
        Returns a list of four card lists.
        """
    assert len(hand) == 6
    return list(combinations(hand, 4))

    
def power_hand(hand):
    """ Given a hand of 5 cards (or 4 or 6..) this method creates every 
        possible combination of the cards of that hand.
        Useful for counting 15's.
        ***modified from: docs.python.org/2/library/itertools.html***
        Returns a list of tuples of each possible card combination.
        """
    assert type(hand) == list
    ch = chain.from_iterable(combinations(hand, r) for r in range(len(hand)+1))
    return list(ch)
    
def sort_hand(hand):
    """ This method takes a hand and sorts it (ace low and king high)
        Useful for counting runs.
        Returns a list of the original cards in sorted order 
        """
    ####**** This could be changed to map all ranks to numbers and then 
    ####**** sort once, probably could use this:
    ####     rank_dict = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6':6, '7':7, \
    ####                  '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}
    
    ## we need to sort T,J,Q,K separately because they share the same value
    not_tens = [x for x in hand if x.value != 10]
    tens = [x for x in hand if x.value == 10]

    # map the face cards to these numbers for the sort
    tens_dict = {'T':1, 'J':2, 'Q':3, 'K':4, 't':1, 'j':2, 'q':3, 'k':4}
    tens.sort(key=lambda x: tens_dict[x.rank], reverse=False)
    
    not_tens.sort(key=lambda x: x.value, reverse=False)

    # recombine the lists and return the results
    return not_tens + tens


def can_append_run(left, right):
    """ Helper function for find_run.
        takes 2 lists and determines if the leftmost element of the right list
        can be appended to the right side of the left list while keeping the
        left list legal as a run.
        Returns: True/False
        """
    if len(left) == 0:
        return True
    elif len(right) == 0:
        return False
    elif left[-1] == right[0] or left[-1]+1 == right[0]:
        return True
    else:
        return False

def is_scoring_run(run):
    """ Helper function for find_run.
        Determines if a run is a scoring run or not.
        Returns True/False
        """
    if len(run) < 3:
        return False
    elif run[-1] - run[0] < 2:
        return False
    else:
        return True
    

def find_run(current_run, left_to_go):
    """ Recursive method of finding any scoring runs in the hand,
        depends on can_append_run() and is_scoring_run().
        (Steps through the left_to_go list from left to right, appending the
        leftmost element to the current run if legal, or starting a new
        curernt_run if not)
        Returns the scoring run, if any
        """
    if can_append_run(current_run, left_to_go):
        # if legal, move one card over
        return find_run(current_run + [left_to_go[0]], left_to_go[1:])
    else:
        if is_scoring_run(current_run):
            # there can only be one scoring run in a five card hand
            return current_run
        elif len(left_to_go) > 2:
            return find_run([], left_to_go)
        else:
            return []

def sum_cards(hand):
    """ This method takes a hand of any length and adds the values of each card.
        Useful for counting 15's.
        Returns an int of the sum of all the cards' values
        """
    hand_sum = 0
    for _card in hand:
        hand_sum += _card.value
    return hand_sum


################################################################################
################################ scoring #######################################
################################################################################


def score_fifteens(full_hand):
    """ Takes a hand of 5 cards, counts all ways those cards can add up
        to 15.
        Returns the number of points from 15's
        """
    score = 0
    all_combos = power_hand(full_hand)
    for combo in all_combos:
        if sum_cards(combo) == 15:
            score += 2
    return score
            
def score_pairs(full_hand):
    """ Takes a hand of 5 cards, counts all pairs (which inclues 3,4 of-a-kind)
        Returns the number of points from pairs
        """
    score = 0
    all_pairs = list(combinations(full_hand, 2)) # need to use a different word
    for pair in all_pairs:
        if pair[0].rank == pair[1].rank:
            score += 2
    return score

def score_runs(full_hand):
    """ Takes a hand of 5 cards, counts all ways those cards can make runs
        three or four long.
        Returns the number of points from runs.
        """
    score = 0
    rank_dict = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6':6, '7':7, \
                 '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}

    " here we make a list of int values to work with instead of rank which \
      is a string, or the regular card values where T,J,Q,K all equal 10 "
    values = [rank_dict[x.rank] for x in full_hand]

    " seed the recursive function with initial condition [] "
    longest_run = find_run([], values)

    " look for pairs or three-of-a-kind within the run "
    run_set = set(longest_run) # ranks in the run without regard to duplicates
    run_set_dict = {} # this will hold the count of each rank

    if len(run_set) > 0:
        if len(run_set) == len(longest_run):
            # single run
            score += len(longest_run)
        else:
            for number in run_set:
                # count the instances of each rank in the run
                run_set_dict[number] = longest_run.count(number)
            doubles = [x for x in run_set if run_set_dict[x] == 2]
            triples = [x for x in run_set if run_set_dict[x] == 3]
            if len(doubles) == 1:
                # double run
                score += len(longest_run) * 2
            elif len(triples) == 1:
                # triple run
                score += len(longest_run) * 3
            elif len(doubles) == 2:
                # double-double run
                score += len(run_set) * 4
    return score

def score_flushes(hand, cut):
    """ Takes a hand of 4 cards, and a cut card
        Checks if the 4 hand cards are of the same suit, if so checks if the
        cut card is of the same suit as well.
        Returns the number of points from flushes.
        """
    score = 0
    if hand[0].suit == hand[1].suit and hand[0].suit == hand[2].suit and\
      hand[0].suit == hand[3].suit:
        if hand[0].suit == cut.suit:
            score += 5
        else:
            score += 4
    return score

def score_nobs(hand, cut):
    """ Takes a hand of 4 cards and a cut card
        If the hand contains the Jack of the same suit as the cut card,
        the player is awarded 1 point
        Returns the number of points from 'nobs'
        """
    score = 0
    if cut.rank != 'J':
        for card in hand:
            if card.rank == 'J':
                if card.suit == cut.suit:
                    score += 1
                    break
    return score

def score_hand(hand,cut):
    """ Given a hand of four cards, and a cut card
        Return the Cribbage score for the hand
        """
    score = 0
    full_hand = hand + (cut,)
    
    ## Order the hand by value 
    full_hand = sort_hand(full_hand)
    
    score += score_fifteens(full_hand)
    score += score_pairs(full_hand)
    score += score_runs(full_hand) 
    score += score_flushes(hand, cut)
    score += score_nobs(hand, cut)
    
    return score


################################################################################
############################ maximizing scores #################################
################################################################################



def max_hand(hand):
    """ Takes a hand of 6 cards and returns the hand of 4 cards with the
        highest expected value.
        Returns a dictionary of the max and min hands and their scores
        """
    possible_hands = enumerate_hands(hand)
    possible_cuts = get_rest_of_deck(hand)
    hand_scores = {}

    for hand in possible_hands:
        main_hand_score = 0
        for cut in possible_cuts: 
            main_hand_score += score_hand(hand,cut)
        hand_scores[copy(hand)] = main_hand_score

    max_score = max([hand_scores[key] for key in hand_scores])
    # in case there is a tie, find all hands with max scores
    max_hands = [key for key in hand_scores if hand_scores[key] == max_score]

    min_score = min([hand_scores[key] for key in hand_scores])
    min_hands = [key for key in hand_scores if hand_scores[key] == min_score]

    return {'max_hand':max_hands[0], 'max_score':max_score/46.,
            'min_hand':min_hands[0], 'min_score':min_score/46.}
    

def max_hand_own_crib(six_hand):
    """ Stub, in progress
        TODO: each possible hand needs to be paired with the crib cards
              that will be tossed so all the possible cribs can be ran.
        """
    possible_hands = enumerate_hands(six_hand)
    possible_cuts = get_rest_of_deck(six_hand)
    hand_scores = {}

    for hand in possible_hands:
        main_hand_score = 0
        crib_cards = get_rest_of_hand(hand, six_hand)
        print 'hand, crib_cards', [x.display for x in hand], [x.display
                                                             for x
                                                             in crib_cards]
        for cut in possible_cuts: 
            main_hand_score += score_hand(hand,cut)

            #hand_w_cut = hand 
            possible_crib_cards = get_rest_of_deck(hand+(cut,))
            possible_crib_pairs = combinations(possible_crib_cards, 2)

            crib_score = 0
            count = 0
            for pair in possible_crib_pairs:
                crib_score += score_hand(crib_cards+[pair,],cut)
                count = count + 1
            print '********** count: ', count
                
            
        hand_scores[copy(hand)] = main_hand_score

    max_score = max([hand_scores[key] for key in hand_scores])
    # in case there is a tie, find all hands with max scores
    max_hands = [key for key in hand_scores if hand_scores[key] == max_score]

    min_score = min([hand_scores[key] for key in hand_scores])
    min_hands = [key for key in hand_scores if hand_scores[key] == min_score]

    return {'max_hand':max_hands[0], 'max_score':max_score/46.,
            'min_hand':min_hands[0], 'min_score':min_score/46.}


################################################################################
############################# user interactions ################################
################################################################################

def make_random_hand():
    """ This makes a random hand of six cards
        Returns a list of six card objects.
        """
    deck = make_deck()
    hand = random.sample(deck, 6)

    return hand

def display(hand):
    """ Returns the display of a hand.
        """
    ##*** stuff like this is why it may be worthwhile to make a hand object
    return [x.display for x in hand]

def test_hand():
    """ This creates a random hand and recommeds which four cards to keep
        Returns the six and four card hands as displayable lists
        and the expected score
        """
    hand = make_random_hand()
    
    m_hand, m_score, min_hand, min_score = max_hand(hand) # broken

    print 'random hand', [card.display for card in hand]
    print 'recommended', [card.display for card in m_hand]
    print 'expected score %.2f' % m_score
    print 'worst play', [card.display for card in min_hand]
    print 'worst score %.2f' % min_score
    
    return [card.display for card in hand], [card.display for card in m_hand]\
           , m_score


def get_input():
    """ Helper function for find_keepers. Prompts the user for a card and
        Returns a card object.
        """
    ## This could do some checking
    card_string = raw_input("Please enter a card in the form '4H' or 'JD': ")
    return card(card_string[0].upper(), card_string[1].upper())


def find_keepers():
    """ This is a function for a user to input a hand and be given back
        the four cards with the highest expecgted score.\
        Returns nothing, prints results to the screen.
        """
    hand = []

    while len(hand) < 6:
        try:
            hand.append(get_input())
        except:
            print "There was an error, please try again"
            print "Error: ", sys.exc_info()[0]
            q = raw_input('To quit enter Q: ')
            if q == 'Q' or q == 'q':
                return
                
        print '                         The current hand is', display(hand)
        
    maxmin_dict = max_hand(hand)
    

    print 'The best hand to keep is: ', [x.display
                                         for x
                                         in maxmin_dict['max_hand']]
    print 'With an expected score of: %.2f' % maxmin_dict['max_score']
    
    print 'The worst hand to keep is: ', [x.display
                                          for x
                                          in maxmin_dict['min_hand']]
    print 'With an expected score of: %.2f' % maxmin_dict['min_score']
    

def find_keepers_own_crib():
    """ This is a method for a user to input a hand and be given back
        the four card with the highest expected score TAKING INTO ACCOUNT
        IT IS THEIR CRIB
        Returns....
        """
    pass

def find_keepers_opponents_crib():
    """ This is a method for a user to input a hand and be given back
        the four card with the highest expected score TAKING INTO ACCOUNT
        IT IS THEIR OPPONENT'S CRIB
        Returns....
        """    
    pass

def demonstrate():
    """ This is a method that generates a random hand, prints it to screen
        and then determines which cards to keep and which to discard.
        Returns nothing
        """
    hand = make_random_hand()
    maxmin_dict = max_hand(hand)
    print 'A randomly generated hand is: ', display(sort_hand(hand))
    print
    print 'The best cards to keep from this hand,'
    print 'not taking into account whose crib it is, are: '
    print display(sort_hand(maxmin_dict['max_hand']))
    print 'Which have an expected score of: %.2f' % maxmin_dict['max_score']
    print ''
    print 'The worst cards to keep from the hand would be:'
    print display(sort_hand(maxmin_dict['min_hand']))
    print 'With an expected score of: %.2f' % maxmin_dict['min_score']
    
    
    

    
    
    

    
    
