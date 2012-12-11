# -*- coding: utf-8 -*-
'''
    stare game xmpp protocol module
    
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
import xmpp
import configure
import hall
import weakref

class StareXMPP:
    def __init__(self):
        self._game_hall = hall.GameHall(weakref.ref(self))
        
    def start(self):
        jid, password, server = configure.XMPP['jid'], configure.XMPP['password'], configure.XMPP['server']
        self._jid = xmpp.JID(jid)
        self._conn = xmpp.Client(self._jid.getDomain(), debug=[])        
        res = self._conn.connect(server)
        if not res:
            raise 'Error: cannot connect to server %s!' % str(server)
        if res <> 'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"
        res = self._conn.auth(self._jid.getNode(), password, self._jid.getResource())
        if not res:
            raise "Error: unable to authorize on %s - check login/password." % server
        if res <> 'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!" % server
        self._bot_jid = '%s@%s/%s' % (self._conn.User, self._conn.Server, self._conn.Resource)
        self._conn.RegisterHandler('message', self.__messageCB)
        self._conn.RegisterHandler('presence',self.__presenceCB)
        self._conn.sendInitPresence()
        print 'Bot started.'
        self.__main_loop()
        print 'Bot stopped.'
        
    def __main_loop(self):
        last_active = time.time()
        
        while True:
            try:
                self._conn.Process(0.1)
                now = time.time()
                if now - last_active > 0.1:
                    last_active = now
                    self._game_hall.active()
                    
            except KeyboardInterrupt:
                return
            
    def __messageCB(self, dispatcher, message):
        who = message.getFrom()
        player = self._game_hall.get_player(who.getStripped().lower())
        if not player:
            text = message.getBody()
            if not text:
                return
                
            if text.strip().lower() == '/login':
                self._game_hall.add_player(who.getStripped().encode('utf-8').lower(), who.getNode().encode('utf-8'))
                return
                            
            self.send(who.getStripped(), '您还没有登陆，需要登陆请输入：/login')
            return            
            
        try:
            loc = player._loc_ref()
            msg = message.getBody()
            if msg:
                loc.process_message(player, msg.encode('utf-8'))
                
        except:
            SHOW_TRACE()
            
    def __presenceCB(self, dispatcher, presence):
        who = presence.getFrom()
        type = presence.getType()
        print type, who
        if type == 'subscribe':
            self._conn.send(xmpp.Presence(to = who.getStripped(), typ = 'subscribed'))
            self._conn.send(xmpp.Presence(to = who.getStripped(), typ = 'subscribe'))            
            print 'send subscribed'         
        elif type == 'unavailable' or type == 'unsubscribed':
            self._game_hall.remove_player(who.getStripped().encode('utf-8'))
        elif type == 'available' or type == None:
            player = self._game_hall.get_player(who.getStripped().lower())
            if not player:
                self.send(who.getStripped(),
                '''
                
                
                
                
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

                     
                您好！我是《干瞪眼》机器人，欢迎您的到来！
                进入游戏请输入：/login
                更多信息请访问：http://code.google.com/p/stare-game/''')
            
           
            
    def send(self, jid, msg):
        m = xmpp.Message(jid, msg)
        m.setFrom(self._bot_jid)
        m.setType('chat')
        self._conn.send(m)
        
    def send_to_all(self, msg, player_list, exclude = []):
        r = self._conn.getRoster()
        for i in r.getItems():
            key = unicode(i).encode('utf-8')
            player = player_list.get(key, None)
            if player and key not in exclude:
                self.send(player._account, msg)