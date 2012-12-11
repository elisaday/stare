# -*- coding: utf-8 -*-
'''
    stare game start state.
    
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

from game_state_base import *
from card import find_min_card
import string

class GS_Start(GameState):
    def active(self, game):
        room = game._room_ref()
        game._card_set.shuffle()
        assert(len(room._player_list) <= 5)
        cl = []
        for player in room._player_list.values():
            card_list = game._card_set.deal(5)
            player.got_card(card_list)
            room.send(player, '您现在的牌有：\r\n%s' % player.get_card_list_str())
            cl.append(find_min_card(card_list))
            
        card = find_min_card(cl)
        game._turn = card._player_ref()
        game._must_play_card = card
        
        room.send_to_all('现在该%s出牌' % game._turn._nick_name, [game._turn._account])
        room.send(game._turn, '现在该您出牌，必须包含：%s' % card)
        
        return GS_WAIT_PLAY
        