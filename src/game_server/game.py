# -*- coding: utf-8 -*-
'''
    stare game main module.
    
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
import string
import card     
from fsm.game_state_base import *
from fsm.gs_start import GS_Start
from fsm.gs_wait_play import GS_WaitPlay
from fsm.gs_pass import GS_Pass
from fsm.gs_round_end import GS_RoundEnd

class Game:    
    def __init__(self, room_ref):
        self._room_ref = room_ref
        self._card_set = card.CardSet()                
        self._state = None        
        self._state_map = {
            GS_START : GS_Start(self),
            GS_WAIT_PLAY : GS_WaitPlay(self),
            GS_PASS : GS_Pass(self),
            GS_ROUND_END : GS_RoundEnd(self),
        }
        
        self._turn = None
        self._last_play_player = None
        self._pass_list = []
        self._must_play_card = None
        self._double = 1
        self._last_play_list = []
        self._judge_ret = None
        
    def finalize(self):
        self._turn = None
        self._state = None
        self._last_play_list = []
        self._pass_list = []
        
    def start(self):
        if self._state:
            return '游戏已经开始'
            
        room = self._room_ref()
        self._state = self._state_map[GS_START]
        room.sys_to_all('游戏开始...', room._player_list)
        return None
        
    def play(self, play_idx_list, player):
        play_list = [player._card_list[i] for i in play_idx_list]
        if not play_list:
            return '出牌非法[出牌列表为空]', False
            
        card_list_str = player.get_card_list_str(play_idx_list)
        try:
            self._judge_ret = player.play(self, play_list, self._last_play_list, self._judge_ret)
        except card.EXCEPTION_BAD_PLAY, e:
            return '出牌非法[%s]' % e._desc, False
            
        if self._judge_ret == card.JUDGE_RET_BOMB:
            self._double += 1
        room = self._room_ref()
        room.send_to_all('%s\r\n打出：%s' % (player._nick_name, card_list_str), [player._account])
        self._last_play_list = play_list
        self._pass_list = []
        self._last_play_player = player
        self._must_play_card = None        
        return '您打出：\r\n%s' % card_list_str, True
        
    def game_over(self, interrupt = False):
        room = self._room_ref()
        if not interrupt:
            result = ['游戏结束，结果如下：\r\n']
            for player in room._turn_list:
                lose = player.calc_lose(self._double)
                if lose == 0:
                    result.append('%s：胜利\r\n' % player._nick_name)
                else:
                    result.append('%s：输%d分\r\n' % (player._nick_name, lose))
                
            room.send_to_all(''.join(result))
            
        self._card_set.init()
        self._state = None  
        self._turn = None
        self._last_play_player = None
        self._pass_list = []
        self._must_play_card = None
        self._double = 1
        self._last_play_list = []
        self._judge_ret = None
                    
        for player in room._turn_list:
            player.clear_all_card()
            
        return None
        
    def next_turn(self):
        room = self._room_ref()
        idx = room._turn_list.index(self._turn) - 1
        self._turn = room._turn_list[idx]
        
        room.send_to_all('现在该%s出牌' % self._turn._nick_name, [self._turn._account])
        room.send(self._turn, '现在该您出牌')
        room.send(self._turn, self._turn.get_card_list_str())
            
    def round_end(self):
        room = self._room_ref()
        for player in room._turn_list:
            new_card = self._card_set.deal(1)
            player.got_card(new_card)
    
    def change_state(self, state):
        if not self._state:
            return
            
        self._state.exit(self)
        self._state = self._state_map[state]
        self._state.enter(self)
        
    def active(self):
        if not self._state:
            return
            
        state = self._state.active(self)
        if state:
            self.change_state(state)
            
    def process_message(self, player, messsage):
        if not self._state:
            return None
            
        return self._state.process_message(self, player, messsage)