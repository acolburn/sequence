import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

TIMER_INTERVAL = 1.0


GREEN = '#8fef8f'
BLUE = '#a8c2e1'

HEARTS = "\u2665"
DIAMONDS = "\u2666"
CLUBS = "\u2663"
SPADES = "\u2660"

locations={'A'+HEARTS:[(5,1),(6,4)],
                   'K'+HEARTS:[(6,1),(6,5)],
                   'Q'+HEARTS:[(7,1),(6,6)],
                   '10'+HEARTS:[(8,1),(5,6)],
                   '9'+HEARTS:[(4,6),(8,2)],
                   '8'+HEARTS:[(3,6),(8,3)],
                   '7'+HEARTS:[(3,5),(8,4)],
                   '6'+HEARTS:[(3,4),(8,5)],
                   '5'+HEARTS:[(4,4),(8,6)],
                   '4'+HEARTS:[(5,4),(8,7)],
                   '3'+HEARTS:[(5,5),(8,8)],
                   '2'+HEARTS:[(4,5),(7,8)],
                   '2'+SPADES:[(1,0),(6,8)],
                   '3'+SPADES:[(2,0),(5,8)],
                   '4'+SPADES:[(3,0),(4,8)],
                   '5'+SPADES:[(4,0),(3,8)],
                   '6'+SPADES:[(5,0),(2,8)],
                   '7'+SPADES:[(6,0),(1,8)],
                   '8'+SPADES:[(7,0),(1,7)],
                   '9'+SPADES:[(8,0),(1,6)],
                   '10'+SPADES:[(9,1),(1,5)],
                   'Q'+SPADES:[(9,2),(1,4)],
                   'K'+SPADES:[(9,3),(1,3)],
                   'A'+SPADES:[(9,4),(1,2)],
                   'A'+DIAMONDS:[(1,9),(6,7)],
                   'K'+DIAMONDS:[(2,9),(7,7)],
                    'Q'+DIAMONDS:[(3,9),(7,6)],
                    '10'+DIAMONDS:[(4,9),(7,5)],
                    '9'+DIAMONDS:[(5,9),(7,4)],
                    '8'+DIAMONDS:[(6,9),(7,3)],
                    '7'+DIAMONDS:[(7,9),(7,2)],
                    '6'+DIAMONDS:[(8,9),(6,2)],
                    '5'+DIAMONDS:[(9,8),(5,2)],
                    '4'+DIAMONDS:[(9,7),(4,2)],
                    '3'+DIAMONDS:[(9,6),(3,2)],
                    '2'+DIAMONDS:[(9,5),(2,2)],
                    'A'+CLUBS:[(0,8),(5,7)],
                    'K'+CLUBS:[(0,7),(4,7)],
                    'Q'+CLUBS:[(0,6),(3,7)],
                    '10'+CLUBS:[(0,5),(2,7)],
                    '9'+CLUBS:[(0,4),(2,6)],
                    '8'+CLUBS:[(0,3),(2,5)],
                    '7'+CLUBS:[(0,2),(2,4)],
                    '6'+CLUBS:[(0,1),(2,3)],
                    '5'+CLUBS:[(1,1),(3,3)],
                    '4'+CLUBS:[(2,1),(4,3)],
                    '3'+CLUBS:[(3,1),(5,3)],
                    '2'+CLUBS:[(4,1),(6,3)],
                    'J'+HEARTS:[],
                    'J'+DIAMONDS:[],
                    'J'+SPADES:[],
                    'J'+CLUBS:[]
                  }


    
