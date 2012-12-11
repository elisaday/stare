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

import xmpp
import string

class Place:        
    def __init__(self, stare_ref):
        self._stare_ref = stare_ref
        self._player_list = {}
        
    def __str__(self):
        return '未定义位置'
        
    def finalize(self):
        self._player_list = {}
        
    def quit(self, player):
        try:
            self._player_list.pop(player._account)
        except:
            pass
                    
    def process_message(self, player, text):
        text = text.strip()
        if not text:
            return

        if text.startswith('/'):
            text = text[1:]
            reply = player.process_message(text)
            if reply == None:
                try:
                    if ' ' in text:
                        cmd, msg = text.split(' ', 1)
                    else:
                        cmd, msg = text, ''
                    method = getattr(self, 'do_%s' % cmd.upper())
                    reply = method(player, msg)
                    
                except:
                    self.sys_send(player, '错误的命令')
                    return
                   
            if reply:
                self.send(player, reply)        
                
    def send(self, player, msg):
        stare = self._stare_ref()
        stare.send(player._account, msg)
                
    def send_to_all(self, msg, exclude = []):
        stare = self._stare_ref()
        stare.send_to_all(msg, self._player_list, exclude)
                
    def sys_send(self, player, msg):
        self.send(player, '[系统] %s' % msg)

    def sys_to_all(self, msg, exclude = []):
        self.send_to_all('[系统] %s' % msg, exclude)
        
    def do_PLAYER_LIST(self, player, msg):
        '''查看所在位置的玩家列表：
        用法：/player_list'''
        if self._player_list:
            return '玩家列表：\r\n%s' % string.join(map(str, self._player_list.values()), '\r\n')
        else:
            return '玩家列表：空\r\n'           