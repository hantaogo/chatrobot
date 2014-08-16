#!/usr/bin/python2
# -*- coding: utf8 -*-
# 
import aiml
import os
import config as cfg

import sys
from SocketServer import ThreadingTCPServer, BaseRequestHandler
import traceback
import socket

class TalkBot(aiml.Kernel):
    def __init__(self,properties=cfg.BOT_PROPERTIES):
        aiml.Kernel.__init__(self)
        self.verbose(cfg.DEBUG)
        if os.path.isfile("xdtuxbot.brn"):
            self.bootstrap(brainFile = "xdtuxbot.brn")
        else:
            self.init_bot()
            self.saveBrain("xdtuxbot.brn")
        for p in properties:
            self.setBotPredicate( p, properties[p] )
    
    def init_bot(self):
        for file in os.listdir(cfg.AIML_SET):
            if file[-4::]=="aiml":
                self.learn(os.path.join(cfg.AIML_SET,file) )

class ChatRobotRequestHandler(BaseRequestHandler):
    """
    聊天服务器处理器
    """
    bot = None

    def setup(self):
        self.bot = TalkBot()

    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if not data:
                    print "disconnect"
                    break

                if data == "88":
                    print "exit"
                    break

                params = str.split(data.strip(), ":")
                if len(params) != 2:
                    continue
                
                # print "request:", params[1]
                res = self.bot.respond(params[1])
                # print "response:", res
                self.request.sendall(params[0] + ":" + res)

            except:
                traceback.print_exc()

if __name__ == '__main__':
    paramCount = len(sys.argv)
    if paramCount == 2:
        port = int(sys.argv[1])
    else:
        port = 1874

    host = ""
    addr = (host, port)
    server = ThreadingTCPServer(addr, ChatRobotRequestHandler)

    print u"--------聊天机器人服务器启动--------"
    print u"  PORT:", port
    print u"------------------------------------"

    server.serve_forever()