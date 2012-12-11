# -*- coding: utf-8 -*-
'''
    stare game wait state.
    
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

class GS_WaitPlay(GameState):
    def enter(self, game):
        self._change_state = None
        
    def active(self, game):
        if not game._turn._card_list:
            return game.game_over()
            
        if self._change_state == GS_WAIT_PLAY:
            game.next_turn()
            return GS_WAIT_PLAY
            
        return self._change_state
        
    def process_message(self, game, player, messsage):
        try:
            if ' ' in messsage:
                cmd, msg = messsage.split(' ', 1)
            else:
                cmd, msg = messsage.strip(), ''
                
            method = getattr(self, 'do_%s' % cmd.upper())
            return method(game, player, msg)

        except AttributeError:
            pass
            
        except:
            SHOW_TRACE()
            
        return None
        
    def do_PLAY(self, game, player, msg):
        '''出牌：
        用法：/play <牌的索引> ...'''
        if game._turn != player:
            return '现在不该您出牌'
            
        try:
            play_idx_list = map(int, msg.split(' '))
            ret, ok = game.play(play_idx_list, player)
            if ok:
                self._change_state = GS_WAIT_PLAY
            return ret
            
        except:
            return self.do_PLAY.__doc__
            
    def do_PASS(self, game, player, msg):
        '''放弃出牌：
        用法：/pass'''
        if game._turn != player:
            return '现在不该您出牌'
            
        try:
            if game._must_play_card or game._last_play_player == None:
                return '您必须出牌，不能放弃'
                
            self._change_state = GS_PASS
            room = game._room_ref()
            room.send_to_all('%s放弃出牌' % player._nick_name, [player._account])
            game._pass_list.append(player)
            return '您放弃出牌'
            
        except:
            return self.do_PASS.__doc__