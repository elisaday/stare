# -*- coding: utf-8 -*-
'''
    stare game player
    
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

import weakref
import string
import card
from room import GameRoom

class Player:
    '''玩家'''
    def __init__(self, account, nick_name, hall_ref):
        self._account = account
        self._nick_name = nick_name
        self._loc_ref = hall_ref
        
        self._card_list = []
        
    def __str__(self):
        return '%s[%s]' % (self._nick_name, self._account)
        
    def do_ME(self, msg):
        '''查看自己的相关信息：
        用法：/me'''
        return '''帐号：%s
        呢称：%s
        位置：%s''' % (self._account, self._nick_name, self._loc_ref())
        
    def do_NICK(self, msg):
        '''修改呢称：
        用法：/nick <你的呢称>'''
        if msg:
            self._nick_name = msg
            return '您的呢称已经改为：%s' % msg
        else:
            return self.do_NICK.__doc__
            
    def do_SHOUT(self, msg):
        '''喊话：
        用法：/shout <文字>'''
        loc = self._loc_ref()
        if loc:
            loc.send_to_all('%s大声的喊到：%s' % (self._nick_name, msg), [self._account])
        return ''
        
    def do_SHOW_CARDS(self, msg):
        '''显示手中的牌：
        用法：/show_cards'''
        if not self._card_list:
            return '您没有牌'
        return '您的牌有：\r\n%s' % self.get_card_list_str()

    def __get_help_info(self):
        return '''
        -----------------------
        《干瞪眼》帮助信息
        -----------------------
        游戏通过输入命令的方式进行，命令的一般格式为：/<命令> [参数1] [参数2] ...
        命令和参数之间用空格分开，参数和参数之间也用空格分开
        
        查看游戏规则，请输入：/help rule
        查看详细命令说明，请输入：/help cmd
        '''

    def _get_help_CMD(self):
        info = ['''
        -----------------------
        《干瞪眼》帮助信息
        -----------------------
        游戏通过输入命令的方式进行，命令的一般格式为：/<命令> [参数1] [参数2] ...
        命令和参数之间用空格分开，参数和参数之间也用空格分开
        ''']
        import hall
        class_list = [Player, hall.GameHall, GameRoom]
        for c in class_list:
            info.append('%s命令：' % c.__doc__)
            info.append('-----------------------')
            for name in c.__dict__:
                if name.startswith('do_'):
                    cmd_name = name[4:]
                    info.append(c.__dict__[name].__doc__)
                    info.append('')
                    
            info.append('-----------------------')
                    
        return string.join(info, '\r\n')
        
    def _get_help_RULE(self):
        return '''
        = 《干瞪眼》游戏介绍 =
        
            《干瞪眼》游戏是一种扑克牌玩法。据说是继《斗地主》后又一新兴玩法。
        
        = 详细规则 =

              * 扑克牌上的点数以３最小，２最大
              
              * 大王和小王可以当作任意一张牌
              
              * 刚开始每人发５张牌，拥有最小的一张牌的玩家首先出牌，且出的牌必须包含这张牌。如果牌上的点数一样，那么就比较花色，从大到小依次为：黑桃，红心，梅花，方块
              
              * 出牌可以出单牌，一对，顺子（３张或以上），连对（３对或以上），三同，炸弹（４张点数相同），如果出王，那么王不能单独出，必须和其他的牌合到一起出。
              
              * 上一个玩家出了牌，那么下一个玩家出的牌，必须只比上家出的牌的点数大一，且张数必须一样。这里有个例外，如果是单牌，可以直接出２。
              
              * 如果没有对应的牌，那么只能选择过（pass）。有可以出的牌的时候，同样可以选择过。
              
              * 在任何情况下，都可以出炸弹。炸一次，牌局增加一翻。
              
              * 当一个玩家出了牌后，其他所有人都没有可以出的牌，那么称为一轮结束。这时候，每个人新发一张牌。
              
              * 当某个玩家所有牌出完后，游戏结束。
              
              * 游戏结束后，每个玩家手里有几张牌，那么输掉几点。如果手里有２，那么有几个２，就增加几翻。如果某个玩家一张牌都没有出，那么增加２翻。最后还要加上炸弹产生的翻。
        '''
                
    def do_HELP(self, msg):
        '''查看帮助：
        用法：/help [类别]'''
        try:
            method = getattr(self, '_get_help_%s' % msg.upper())
            return method()
            
        except:
            return self.__get_help_info()
                
    def process_message(self, msg):
        try:
            if ' ' in msg:
                cmd, msg = msg.split(' ', 1)
            else:
                cmd, msg = msg.strip(), ''
            method = getattr(self, 'do_%s' % cmd.upper())
            return method(msg)

        except AttributeError:
            pass
            
        except:
            SHOW_TRACE()
            
        return None
                
    def got_card(self, card_list):
        for card in card_list:
            card.attach_player(weakref.ref(self))
        self._card_list = self._card_list + card_list
        self._card_list.sort()
        
    def clear_all_card(self):
        self._card_list = []
        
    def calc_lose(self, double):
        for card in self._card_list:
            if card._no._no == 15:
                double += 1
        
        return len(self._card_list) * double
        
    def get_card_list_str(self, index_list = []):
        if not index_list:
            index_list = xrange(0, len(self._card_list))
            
        return string.join(map(lambda n : '(%d) %s' % (n, self._card_list[n]), index_list), '\r\n')
                
    def play(self, game, play_list, last_play_list, judge_ret):
        if game._must_play_card and not game._must_play_card in play_list:
            raise card.EXCEPTION_BAD_PLAY('没有包含必须出的牌：%s' % game._must_play_card)

        ret = card.judge_play(play_list, last_play_list, judge_ret)
        map(self._card_list.remove, play_list)
        return ret
            
    def on_offline(self):
        if not self._loc_ref:
            return
            
        place = self._loc_ref()
        if not place:
            return
            
        if isinstance(place, GameRoom):
            room = place
            if room._game._state:
                room.send_to_all('玩家%s下线，此盘游戏强制结束' % self.__str__())
            else:
                room.send_to_all('玩家%s下线' % self.__str__())
        
        place.quit(self)
        