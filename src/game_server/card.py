# -*- coding: utf-8 -*-
'''
    stare game card module
    
    created: 2007-2-7
    author: zeb
    e-mail: zebbey@gmail.com
            
      ◢██████◣　　　　　　◢████◣ 
    ◢◤　　　　　　◥◣　　　　◢◤　　　　◥◣ 
    ◤　　　　　　　　◥◣　　◢◤　　　　　　█ 
    ▎　　　◢█◣　　　◥◣◢◤　　◢█　　　█ 
    ◣　　◢◤　　◥◣　　　　　　◢◣◥◣　◢◤ 
    ◥██◤    ◢◤ 　　　　　　     ◥██◤ 
    　　　　　　█　●　　　　　　　●　█ 
    　　　　　　█　〃　　　▄　　　〃　█ 
    　　　　　  ◥◣　　　╚╩╝　　　◢◤ 
    　　　　　　　◥█▅▃▃　▃▃▅█◤ 
    　　　　　　　　　◢◤　　　◥◣ 
    　　　　　　　　　█　　　　　█ 
    　　　　　　　　◢◤▕　　　▎◥◣ 
    　　　　　　　▕▃◣◢▅▅▅◣◢▃ 

    ------------------------------------------------------------------------------
    Copyright (C) 2007 Zeb.
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    ------------------------------------------------------------------------------
''' 


import random

class EXCEPTION_BAD_PLAY(Exception):
    def __init__(self, desc = ''):
        self._desc = desc

class TypeBase:
    def __init__(self, val):
        self._val = val
        
class Spade(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 4)
        
    def __str__(self):
        return '黑桃'

class Heart(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 3)
        
    def __str__(self):
        return '红心'

class Club(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 2)
        
    def __str__(self):
        return '梅花'

class Diamond(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 1)
        
    def __str__(self):
        return '方块'

class RedJoker(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 0)
        
    def __str__(self):
        return '大王'
        
class BlackJoker(TypeBase):
    def __init__(self):
        TypeBase.__init__(self, 0)
        
    def __str__(self):
        return '小王'
        
SPADE = Spade()
HEART = Heart()
CLUB = Club()
DIAMOND = Diamond()
RED_JOKER = RedJoker()
BLACK_JOKER = BlackJoker()

class CARD_NO:
    NO_MAP = { 11 : 'J', 12 : 'Q', 13 : 'K', 14 : 'A', 15 : '2' }
    def __init__(self, no):
        self._no = no
        if no <= 10:
            self._str = str(self._no)
        else:
            self._str = CARD_NO.NO_MAP.get(self._no, '')
        
    def __str__(self):
        return self._str        
        
class Card:
    def __init__(self, type, no):
        self._type = type
        self._no = CARD_NO(no)
        self._player_ref = None
        
    def __int__(self):
        return self._no._no
        
    def __str__(self):
        return '%s[%s]' % (self._type, self._no)
        
    def __lt__(self, card):
        if self._no._no < card._no._no:
            return True
        elif self._no._no == card._no._no:
            if self._type._val < card._type._val:
                return True
                
        return False
        
    def __eq__(self, card):
        if card == None:
            return False
            
        if self._no._no == card._no._no:
            return True
        else:
            return False
            
    def __ne__(self, card):
        return not self.__eq__(card)
        
    def attach_player(self, ref):
        self._player_ref = ref
        
    def deattach_player(self):
        self._player_ref = None
        
class CardSet:
    def __init__(self):
        self._cards = []
        self.init()
        
    def init(self):
        self._cards = []
        for i in xrange(3, 16):
            self._cards.append(Card(SPADE, i))
            self._cards.append(Card(HEART, i))
            self._cards.append(Card(CLUB, i))
            self._cards.append(Card(DIAMOND, i))
            
        self._cards.append(Card(RED_JOKER, 17))
        self._cards.append(Card(BLACK_JOKER, 16))

    def shuffle(self):
        for i in xrange(0, 53):
            r = random.randrange(i + 1, 54)
            self._cards[r], self._cards[i] = self._cards[i], self._cards[r]
            
    def deal(self, amount):
        if amount > len(self._cards):
            amount = len(self._cards)
            
        if not amount:
            return []

        ret, self._cards = self._cards[:amount], self._cards[amount:]
        return ret
        
def find_min_card(card_list):
    assert(card_list)
    card = card_list[0]
    for i in card_list:
        if i < card:
            card = i
            
    return card
    
        
JUDGE_RET_BOMB = 1
JUDGE_RET_SINGLE = 2
JUDGE_RET_DOUBLE = 3
JUDGE_RET_TREBLE = 4
JUDGE_RET_STRAIGHT = 5
JUDGE_RET_STRAIGHT_DOUBLE = 6
    
def __is_same(card_list, amount):
    if len(card_list) == amount:
        c = None
        for card in card_list:
            if card._type == RED_JOKER or card._type == BLACK_JOKER:
                continue
                
            if c == None:
                c = card
                continue
                
            if card != c:
                return None
                
        return c
    return None
    
def __is_straight(card_list):
    if len(card_list) < 3:
        return None
        
    card = None
    joker = 0
    if card_list[-1]._type == RED_JOKER or card_list[-1]._type == BLACK_JOKER:
        joker += 1
    if card_list[-2]._type == RED_JOKER or card_list[-2]._type == BLACK_JOKER:
        joker += 1        
    for c in card_list:
        if c._type == RED_JOKER or c._type == BLACK_JOKER:
            continue
                    
        if c._no._no == 15:
            return None
            
        if card == None:
            card = c
            continue
            
        if c._no._no == card._no._no + 1:
            card = c
            continue
            
        if c._no._no == card._no._no + 2 and joker > 0:
            joker -= 1
            card = c
            continue
            
        if c._no._no == card._no._no + 3 and joker > 1:
            joker -= 2
            card = c
            continue
            
        return None
        
    return card_list[0]

def __is_straight_double(card_list):
    if len(card_list) < 6 and len(card_list) / 2 * 2 == len(card_list):
        return None
        
    card = None
    joker = 0
    if card_list[-1]._type == RED_JOKER or card_list[-1]._type == BLACK_JOKER:
        joker += 1
    if card_list[-2]._type == RED_JOKER or card_list[-2]._type == BLACK_JOKER:
        joker += 1
        
    idx = 0
    while idx < len(card_list):
        c1 = card_list[idx]
        if c1._type == RED_JOKER or c1._type == BLACK_JOKER:
            idx += 1
            continue
            
        idx += 1
        c2 = card_list[idx]
            
        if c1 != c2 and joker > 0:
            joker -= 1
            card = c1
            continue
            
        if card == None:
            card = c1
            idx += 1
            continue
            
        if c1._no._no == card._no._no + 1:
            card = c1
            idx += 1
            continue
            
        if c1._no._no == card._no._no + 2 and joker > 1:
            joker -= 2
            card = c1
            idx += 3
            continue
            
        return None
        
    return card_list[0]
    
def __get_judge_ret(card_list):
    if len(card_list) == 1:
        return JUDGE_RET_SINGLE
    elif __is_same(card_list, 2):
        return JUDGE_RET_DOUBLE
    elif __is_same(card_list, 3):
        return JUDGE_RET_TREBLE
    elif __is_same(card_list, 4):
        return JUDGE_RET_BOMB
    elif __is_straight(card_list):
        return JUDGE_RET_STRAIGHT
    elif __is_straight_double(card_list):
        return JUDGE_RET_STRAIGHT_DOUBLE
    raise EXCEPTION_BAD_PLAY('未知的牌类型')
        
def judge_play(card_list, last_list, judge_ret):
    card_list.sort()
    last_list.sort()
    
    card_type = card_list[0]._type
    if card_type == RED_JOKER or card_type == BLACK_JOKER:
        raise EXCEPTION_BAD_PLAY('大小王不能单独出，必须和其他牌组合打出')
    
    if judge_ret == None or not last_list:
        return __get_judge_ret(card_list)
        
    type = __get_judge_ret(card_list)
    if type == JUDGE_RET_BOMB:
        if judge_ret == JUDGE_RET_BOMB and card_list[0] < last_list[0]:
            raise EXCEPTION_BAD_PLAY('您出的炸弹没有上一个玩家出的炸弹大')
        
        return JUDGE_RET_BOMB
    
    if type != judge_ret:
        raise EXCEPTION_BAD_PLAY('您出的牌的类型和上个玩家的不同')
        
    if (card_list[0]._no._no == last_list[0]._no._no + 1) or\
       (card_list[0]._no._no == 15 and card_list[0]._no._no > last_list[0]._no._no):
        return type

    raise EXCEPTION_BAD_PLAY('牌的点数非法')
