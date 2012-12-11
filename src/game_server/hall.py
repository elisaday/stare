# -*- coding: utf-8 -*-
'''
    stare game hall
    
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
import xmpp
from place import Place
from player import Player
from room import GameRoom
import string
import weakref
import version

class GameHall(Place):
    '''游戏大厅'''
    def __init__(self, stare_ref):
        Place.__init__(self, stare_ref)
        
        self._room_list = {}
        
    def __str__(self):
        return '游戏大厅'
        
    def add_player(self, account, nick_name):
        p = Player(account, nick_name, weakref.ref(self))
        if self._player_list.get(p._account, None) == None:
            self._player_list[p._account] = p
            self.sys_send(p, 
            '''欢迎来到《干瞪眼》游戏世界！
            需要帮助请输入：/help
            更多信息请访问：http://code.google.com/p/stare-game/
            您现在的位置是：%s''' % p._loc_ref())
            
    def remove_player(self, account):
        try:
            player = self._player_list[account]
            player.on_offline()
            self._player_list.pop(account)
        
        except KeyError:
            pass
            
        except:
            SHOW_TRACE()
            
    def active(self):
        for room in self._room_list.values():
            room.active()
            if not room._player_list:
                room.finalize()
                self._room_list.pop(room._name)
            
    def get_player(self, account):
        return self._player_list.get(account, None)

    def do_VERSION(self, player, msg):
        '''查看服务器版本：
        用法：/version'''
        return '服务器版本为：%s' % version.SERVER_VERSION
        
    def do_CREATE(self, player, msg):
        '''创建房间：
        用法：/create <房间名字> [密码]'''  
        try:
            if ' ' in msg:
                name, passwd = msg.split(' ', 1)
            else:
                name, passwd = msg.strip(), ''
                
            assert(name)
            if self._room_list.get(name, None):
                return '房间名字重复'

            assert(player)
            room = GameRoom(self._stare_ref, player, name, passwd, weakref.ref(self))
            self._room_list[name] = room
            return '创建房间成功'
            
        except:
            SHOW_TRACE()
            return self.do_CREATE.__doc__
                
    def do_JOIN(self, player, msg):
        '''加入房间：
        用法：/join <房间名字> [密码]'''
        try:
            if ' ' in msg:
                name, passwd = msg.split(' ', 1)
            else:
                name, passwd = msg.strip(), ''
                
            assert(name)
            room = self._room_list.get(name, None)
            if not room:
                return '房间[%s]不存在' % name
                
            return room.join(player)
            
        except:
            SHOW_TRACE()
            return self.do_JOIN.__doc__
            
    def do_ROOM_LIST(self, player, msg):
        '''获取房间列表：
        用法：/room_list'''
        if self._room_list:
            return '房间列表：\r\n%s' % string.join(map(str, self._room_list.values()), '\r\n')
        else:
            return '房间列表：空\r\n'
            
    def do_LOGOUT(self, player, msg):
        '''退出游戏：
        用法：/logout'''
        self.remove_player(player._account)
        return '您已经推出了游戏'