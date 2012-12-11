# -*- coding: utf-8 -*-
'''
    stare game pass state.
    
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

class GS_Pass(GameState):
    def active(self, game):
        room = game._room_ref()
        check_list = [p for p in room._turn_list if p in game._pass_list or p == game._last_play_player]
        if len(check_list) == len(room._turn_list):
            game._last_play_list = []
            game._judge_ret = None
            game._turn = game._last_play_player
            game._last_play_player = None
            return GS_ROUND_END
        else:
            game.next_turn()
            return GS_WAIT_PLAY