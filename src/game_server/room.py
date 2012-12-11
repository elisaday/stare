# -*- coding: utf-8 -*-
'''
    stare game room
    
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

from place import Place
import datetime
from game import Game
import weakref
import string

class GameRoom(Place):
    '''游戏房间'''
    def __init__(self, stare_ref, player, name, passwd, hall_ref):
        Place.__init__(self, stare_ref)
        
        self._owner = player
        self._name = name
        self._passwd = passwd
        self._hall_ref = hall_ref
        self._player_list[player._account] = player
        self._turn_list = [player]
        player._loc_ref = weakref.ref(self)
        self._game = Game(weakref.ref(self))
        
    def __str__(self):
        if self._passwd:
            return '游戏房间[%s] 加密 房主：%s' % (self._name, self._owner._nick_name)
        else:
            return '游戏房间[%s] 开放 房主：%s' % (self._name, self._owner._nick_name) 
        
    def finalize(self):
        Place.finalize(self)
        
        self._owner = None
        self._turn_list = []
        self._game.finalize()
        self._game = None
        
    def process_message(self, player, text):
        if text and text.startswith('/'):
            reply = self._game.process_message(player, text[1:])
            if reply == None:
                Place.process_message(self, player, text)
            elif reply:
                self.send(player, reply)
    
    def join(self, player):
        if self._game._state:
            return '这个房间已经开始游戏，无法加入'
            
        self._player_list[player._account] = player
        self._turn_list.append(player)
        player._loc_ref = weakref.ref(self)
        self.send_to_all('%s进入了这个房间\r\n现在有%d人在这个房间' % (str(player), len(self._player_list)), [player._account])
        return '加入房间成功'
        
    def quit(self, player):
        Place.quit(self, player)
            
        self._game.game_over(True)
        
        self._turn_list.remove(player)
        if self._owner == player and self._turn_list:
            self._owner = self._turn_list[0]
            
    def active(self):
        self._game.active()
        
    def get_room_info(self):
        title = '房间信息：\r\n------------------------'
        name = '名称：%s' % self._name
        owner = '房主：%s' % self._owner._nick_name
        if self._passwd:
            passwd = '密码：%s' % self._passwd
        else:
            passwd = '密码：无'
        player_list = string.join(map(str, self._turn_list), '\r\n')
        return '%s\r\n%s\r\n%s\r\n%s\r\n------------------------\r\n玩家列表：\r\n%s\r\n------------------------' % (title, name, owner, passwd, player_list)
        
    def do_START(self, player, msg):
        '''开始游戏：
        用法：/start'''
        if player == self._owner:
            if len(self._turn_list) < 2:
                return '游戏人数不够，至少要2人'
            return self._game.start()
        else:
            return '只有房间的主人才能开始游戏'
            
    def do_EXIT(self, player, msg):
        '''退出房间：
        用法：/exit'''
        if self._game._state:
            self.send_to_all('游戏强制结束')
        self.quit(player)
        self.send_to_all('%s已经退出了房间' % player._nick_name, [player._account])
        player._loc_ref = self._hall_ref
        return '您已经退出了房间'
        
    def do_ROOM_INFO(self, player, msg):
        '''查看房间信息：
        用法：/room_info'''
        try:
            return self.get_room_info()
        except:
            SHOW_TRACE()
            
    def do_GAME_OVER(self, player, msg):
        '''结束游戏：
        用法：/game_over'''
        if self._owner != player:
            return '只有房主才能强制结束游戏'
            
        if self._game._state == None:
            return '游戏还没开始，不能结束'
            
        self._game.game_over(True)
        self.send_to_all('游戏强制结束')
        return None
        
       