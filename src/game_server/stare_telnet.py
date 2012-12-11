# -*- coding: utf-8 -*-
'''
    stare game telnet protocol module
    
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

import time
import common
import asynchat
import asyncore
import socket
import configure
import hall
import weakref

class StareChannel(asynchat.async_chat):
    def __init__(self, conn, addr, stare):
        asynchat.async_chat.__init__(self, conn = conn)
        self._addr = addr
        self._stare = stare
        self._ibuffer = []
        self.set_terminator('\r\n')
        
        self.push('''
        
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
        
        您好！我是《干瞪眼》机器人，欢迎您的到来！')
        进入游戏请输入：/login')
        更多信息请访问：http://code.google.com/p/stare-game/''')
        
    def handle_close(self):
        self._stare._game_hall.remove_player(str(self._addr))
        self._stare.on_channel_close(self)
        self.close()
                        
    def push(self, data):
        asynchat.async_chat.push(self, data + '\n\r\n')
                
    def collect_incoming_data(self, data):
        self._ibuffer.append(data)
        
    def found_terminator(self):
        data = ''.join(self._ibuffer).strip()
        if not data:
            return
            
        ret = self.__process_data(data)
        self._ibuffer = []
        if ret:
            self.push(ret)
        
    def __process_data(self, data):
        if not data.startswith('/'):
            return None

        player = self._stare._game_hall.get_player(str(self._addr))
        if not player:
            try:
                data = data[1:] 
                if ' ' in data:
                    cmd, msg = data.split(' ', 1)
                else:
                    cmd, msg = data, ''
                
                method = getattr(self, 'do_%s' % cmd.upper())
                return method(msg)
                
            except:
                return '您还没有登陆，需要登陆请输入：/login <nick name>'
                
        try:
            loc = player._loc_ref()
            loc.process_message(player, data)
        except:
            SHOW_TRACE()
            
    def do_LOGIN(self, msg):
        try:
            if not msg:
                return '请指定呢称'
                
            nick_name = msg
            self._stare._game_hall.add_player(str(self._addr), nick_name)
            return '登陆成功'
        except:
            SHOW_TRACE()
            return '登陆失败'

class StareTelnet(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        
        self.port = configure.TELNET['port']
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", self.port))
        self.listen(5)
        
        self._conn_list = {}
        self._game_hall = hall.GameHall(weakref.ref(self))

    def handle_accept(self):
        channel, addr = self.accept()
        conn = StareChannel(channel, addr, self)
        self._conn_list[str(addr)] = weakref.ref(conn)
        
    def on_channel_close(self, channal):
        try:
            self._conn_list.pop(str(channal._addr))
        except:
            pass
        
    def send(self, addr, msg):
        try:
            conn = self._conn_list[addr]()
            conn.push(msg)
        except KeyError:
            pass
        except:
            SHOW_TRACE()
            
    def send_to_all(self, msg, player_list, exclude = []):
        for addr in self._conn_list:
            player = player_list.get(addr, None)
            if player and addr not in exclude:
                self.send(addr, msg)
        
    def __main_loop(self):
        last_active = time.time()
        
        while asyncore.socket_map:
            try:
                asyncore.poll(0.01, asyncore.socket_map)
                now = time.time()
                if now - last_active > 0.1:
                    last_active = now
                    self._game_hall.active()
                
            except KeyboardInterrupt:
                return
                        
    def start(self):
        print 'Bot started.'
        self.__main_loop()
        print 'Bot stopped.'        
