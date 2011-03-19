# -*- coding: utf-8 -*-

'''
对CTP进行mock，目的有二：
    1. 为agent提供桩机，便于agent功能的开发和测试
    2. 结合实时行情，测试策略的实时信号
    3. 结合历史ticks行情，对策略进行确认测试

TODO:   为真实起见，在mock中采用Command模式 
桩机控制: (数据播放循环)
    数据播放
    触发Agent数据准备
    触发Agent策略执行
    触发API桩机-->Command
    控制器触发SPI 
    ...   
'''

import time
import hreader
import agent

class TraderMock(object):
    def __init__(self,myagent):
        '''记录agent以回调agent的成交回报接口'''
        self.myagent = myagent

    def ReqOrderInsert(self, order, request_id):
        '''报单录入请求, 需要调用成交函数'''
        oid = order.OrderRef
        trade = ustruct.Trade(
                    InstrumentID = order.InstrumentID,
                    Direction=order.Direction,
                    Price = order.LimitPrice,
                    Volume = order.Volume,
                    OrderRef = oid,
                    TradeID=oid,
                    OrderSysID=oid,
                    BrokerOrderSeq=oid,
                    OrderLocalID = oid,
                    TradeTime = time.strftime('%H%M%S'),#只有备案作用
                )
        self.myagent.rtn_trade(trade)

    def ReqOrderAction(self, corder, request_id):
        '''撤单请求'''
        oid = order.OrderRef
        rorder = ustruct.Order(
                    InstrumentID = corder.InstrumentID,
                    OrderRef = corder.OrderRef,
                )
        self.myagent.rtn_order(rorder)


class UserMock(object):
    pass

class MockManager(object):
    pass

class MockMd(object):
    '''简单起见，只模拟一个合约，用于功能测试
    '''
    def __init__(self,instrument):
        self.instrument = instrument
        self.agent = agent.Agent(None,None,[instrument],{},{})

    def play(self,tday=0):
        ticks = hreader.read_ticks(self.instrument,tday)
        for tick in ticks:
            self.agent.RtnTick(tick)
            #self.agent.RtnTick(tick)

import time
import logging

class NULLAgent(object):
    #只用于为行情提供桩
    logger = logging.getLogger('ctp.nullagent')

    def __init__(self,trader,cuser,instruments):
        '''
            trader为交易对象
        '''
        self.trader = trader
        self.cuser = cuser
        self.instruments = instruments
        self.request_id = 1
        ###
        self.lastupdate = 0
        self.front_id = None
        self.session_id = None
        self.order_ref = 1
        self.trading_day = 20110101
        self.scur_day = int(time.strftime('%Y%m%d'))

    def set_spi(self,spi):
        self.spi = spi

    def inc_request_id(self):
        self.request_id += 1
        return self.request_id

    def inc_order_ref(self):
        self.order_ref += 1
        return self.order_ref

    def set_trading_day(self,trading_day):
        self.trading_day = trading_day

    def get_trading_day(self):
        return self.trading_day

    def login_success(self,frontID,sessionID,max_order_ref):
        self.front_id = frontID
        self.session_id = sessionID
        self.order_ref = int(max_order_ref)

    def RtnTick(self,ctick):#行情处理主循环
        pass


from agent import MdApi,MdSpiDelegate,c,INSTS_SAVE

def user_save1():
    logging.basicConfig(filename="ctp_user.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    cuser0 = c.SQ_USER
    cuser1 = c.GD_USER
    cuser2 = c.GD_USER_3
    cuser_wt1= c.GD_USER_2  #网通
    cuser_wt2= c.GD_USER_4  #网通

    my_agent = NULLAgent(None,None,INSTS_SAVE)

    agent.make_user(my_agent,cuser0,'data')

    #while True:
    #    time.sleep(1)

    return my_agent


def user_save2():
    logging.basicConfig(filename="ctp_user.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    cuser0 = c.SQ_USER
    cuser1 = c.GD_USER
    cuser2 = c.GD_USER_3
    cuser_wt1= c.GD_USER_2  #网通
    cuser_wt2= c.GD_USER_4  #网通

    my_agent = NULLAgent(None,None,INSTS_SAVE)

    #agent.make_user(my_agent,cuser0,'data')
    agent.make_user(my_agent,cuser1,'data1')
    agent.make_user(my_agent,cuser2,'data2')
    agent.make_user(my_agent,cuser_wt2,'data3')

    #while True:
    #    time.sleep(1)

    return my_agent
   
