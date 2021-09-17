#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:34
# @Author  : Future Fu
# @FileName: t1.py

import os, sys

import os
import pandas as pd
import tushare as ts
import time
import datetime
import xlrd
from dateutil.relativedelta import relativedelta #计算前多长时间间隔的日期的库
from matplotlib import pyplot as plt
# import mpl_finance  as mpf #画k线图的金融库
from matplotlib.pylab import date2num

today = datetime.datetime.now().strftime('%Y%m%d')
t = datetime.datetime.strptime(today,'%Y%m%d').date()
year_before_today = (t-relativedelta(years=1)).strftime('%Y%m%d')

ts.set_token('752a393dbf58f03637ebc9c340c8e6ccb07322d3c5421ba680aae2eb')

# path = 'D://python_data_analysis//tushare_project'
path = 'data'
if not os.path.exists('{0}//each_stock_year_data//{1}'.format(path, today)):
    os.makedirs('{0}//each_stock_year_data//{1}'.format(path, today))
    print("当日每只股票行情数据文件夹创建完成")
else:
    print("当日每只股票行情数据文件目录存在")


def get_stock_data_to_excel(day):
    print("******开始获取股市每日行情数据******")
    pro = ts.pro_api()
    stock_daily_data = pro.daily(trade_date=day)
    df = pd.DataFrame(stock_daily_data)
    df.to_excel('{0}//daily_stock_data//data{1}.xlsx'.format(path,day))
    print("******每日行情数据获取成功******")



filedir = path + "//daily_stock_data//data20190118.xlsx"
def stock_filter_than_percent9(file):
    print("******开始分析今日所有涨停板股票******")
    data = xlrd.open_workbook(file)
    table = data.sheets()[0] #获取Excel表的第几张
    table_nrows = table.nrows
    pct_chg = []
    code = []
    for row in range(table_nrows):
        if row == 0:
            continue
        else:
            if table.row_values(row)[9] > 9:
                pct_chg.append(table.row_values(row)[9])
                code.append(table.row_values(row)[1])
    result_code_info = dict(zip(code,pct_chg))
    print("今日涨幅大于9%的股票共有{}只".format(len(result_code_info)))
    return result_code_info


def get_code_year_data():
    print("开始获取今日所有涨停板股票时间段为一年的行情数据")
    pro = ts.pro_api() #tushare数据接口
    count = 1
    for item in stock_code.keys():
        print("******开始获取第{0}只股票行情数据******".format(count))
        time.sleep(3) #每次请求前暂停
        data = pro.daily(ts_code=item,start_date=year_before_today,end_date=today)
        df = pd.DataFrame(data)
        df.to_excel('{0}//each_stock_year_data//{1}//{2}.xlsx'.format(path,today,item))
        count += 1
    print("今日所有的涨停板股票年行情数据获取完成")


def draw_k_line():
    print("开始画股票K线图")
    datafiledir = os.listdir(path+'//each_stock_year_data//{0}//'.format(today))
    for i in range(len(datafiledir)):
        each_stock_code = datafiledir[i].split('.')[0]   #截取相应股票代码
        quotes = []
        stock = pd.read_excel(path+'//each_stock_year_data//{0}//{1}'.format(today,datafiledir[i])) #利用pandas设置excel数据为DataFrame
        stock_row = stock.shape[0] #获取数据表的行数
        #获取每个交易日的开盘价，收盘价，最高价，最低价
        for row in range(stock_row):
            stock_trade_date = str(stock.loc[row,'trade_date'])
            stock_trade_date_change = stock_trade_date[0:4] + '-' + stock_trade_date[4:6] + '-' + stock_trade_date[6:]
            stock_trade_date_num = date2num(datetime.datetime.strptime(stock_trade_date_change,'%Y-%m-%d'))
            stock_trade_date_plot = stock_trade_date_num #这个是画K线图必须使用的日期格式
            stock_open_price = stock.loc[row,'open']
            stock_close_price = stock.loc[row,'close']
            stock_high_price = stock.loc[row,'high']
            stock_low_price = stock.loc[row,'low'          ]
            #按照 candlestick_ohlc 函数要求的数据结构构造数据
            datas = (stock_trade_date_plot,stock_open_price,stock_high_price,stock_low_price,stock_close_price)
            quotes.append(datas)
        #开始画K线图
        fig,ax =plt.subplots(facecolor=(0,0.5,0.5),figsize=(12,8))
        fig.subplots_adjust(bottom=0.1)
        ax.xaxis_date()
        plt.xticks(rotation=45)#日期显示的旋转角度
        plt.title(each_stock_code)
        plt.xlabel('time')
        plt.ylabel('price')
        # mpf.candlestick_ohlc(ax,quotes,width=1.0,colorup='r',colordown='green')#上涨为红色，下降为绿色
        plt.grid(True)
        plt.savefig(path+'//k_line_graph//{0}//{1}.png'.format(today,each_stock_code),dpi=100,facecolor=(0,0.5,0.5))
        plt.close(fig)
        #plt.show()
    print("所有股票K线图绘制完毕,请在图片路径进行查看")


if __name__ == '__main__':
    get_stock_data_to_excel(today)                     #调用函数获取当天行情数据
    stock_code = stock_filter_than_percent9(filedir)   #调用函数分析今日涨停板股票，返回股票代码
    get_code_year_data()                               #根据返回的股票代码，获取其一年的行情数据
    draw_k_line()                                      #根据全年行情数据画对应股票的K线