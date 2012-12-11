# 干瞪眼 #

## 游戏介绍 ##

《干瞪眼》游戏是一种扑克牌玩法。据说是继《斗地主》后又一新兴玩法。
目前游戏支持XMPP, Telnet两种协议。 使用任意的支持这两种协议的工具进行游戏。 
游戏方式类似与文字MUD。

## 详细规则 ##

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

## 安装及运行 ##

* 解压缩服务器包到某个目录
* 修改配置文件configure.py中的参数，如果采用XMPP协议，那么修改XMPP中的参数; 如果采用Telnet协议，那么修改TELNET中的参数
	* XMPP：
		* jid：服务器使用google talk的帐号
		* password：服务器使用的google talk的帐号的密码
	* TELNET：
		* port：服务器开放的端口
* 使用python解释器运行game_server下的stare.py，后面带参数表示采用什么协议
    　现在可用的是xmpp和telnet
* 游戏方式：
	* XMPP：
        	* 玩家的google talk添加服务器使用的google talk的帐号，只需一次，以后不用在添加
	        * 玩家的google talk上线，这时候，游戏机器人会主动想玩家发送提示信息
        	* 玩家可以输入/help查看帮助，按照帮助提示即可进行游戏
	* TELNET：
	        * 直接用Telnet客户端工具连接到游戏服务器的指定端口
