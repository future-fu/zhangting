#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:52
# @Author  : Future Fu
# @FileName: t3.py

import pandas as pd
import tushare as ts


import datetime

import csv
import os

from itertools import islice


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    print(x)
    pd.reset_option('display.max_rows')


def max_util(array_list):
    max_value = array_list[0]
    for i in range(1, len(array_list)):
        if max_value < array_list[i]:
            max_value = array_list[i]
    # print("最大值是：{}".format(max_value))
    max_value


def range_handle(x):
    str1 = list(map(float, x.replace('%', '').split('~')))
    return max(str1)


def csv_handle(file_name):
    file_res = 'C://work/pythoncoding/zhangting/data/res.csv'
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        print(type(reader))
        data = open(file_res, 'w+',encoding='utf-8')
        print("report_date ,code ,name, range, type ,pre_eps",file=data)
        for row in islice(reader, 1, None):
            if (float(range_handle(str(row[6]))) > 400):
                print(row[4], 'A' + row[1], row[2], range_handle(str(row[6])), row[3], row[5],file=data)


def forecast_q(q):
    df = ts.forecast_data(2021, q)
    file_name = str(datetime.date.today()) + '_Astock.csv'
    file_name2 = str(datetime.date.today()) + '_yeji.csv'
    df.to_csv('./data/' + file_name)

    # ZhangTing_df = df[(df["changepercent"]>9.5) & (df["changepercent"]<10.5) ]
    ZhangTing_df = df[(df["range"] > '1000')]
    # ZhangTing_df = df[(float(range_handle(str(df["range"]))) > 500)]
    print_full(ZhangTing_df)
    ZhangTing_df.to_csv('./data/' + file_name2)
    csv_handle('./data/' + file_name2)

def creat_file(file):
    if os.path.exists(file):
        with open(file, mode='r', encoding='utf-8') as ff:
            print(ff.readlines())
    else:
        with open(file, mode='w', encoding='utf-8') as ff:
            print("文件创建成功！")

def fund_holdings_g(q,re,pause):
    df = ts.fund_holdings(2021, q,re,pause)
    file_name = str(datetime.date.today()) + '_AstockjiJin.csv'
    file_name2 = str(datetime.date.today()) + '_yejijiJin.csv'
    df.to_csv('./data/' + file_name)

    # ZhangTing_df = df[(df["changepercent"]>9.5) & (df["changepercent"]<10.5) ]
    ZhangTing_df = df[(df["nums"] > '10')]
    ZhangTing_df.to_csv('./data/' + file_name2)
    csv_handle('./data/' + file_name2)

def file_to_str():
    str1=''
    with open('C://work/pythoncoding/zhangting/data/res.csv', mode='r', encoding='utf-8') as ff:
        str1+=ff.readlines()
    return str1
if __name__ == '__main__':
    print(range_handle('10%~100%'))
    #forecast_q(3)
    fund_holdings_g(3,3,1)
   #  profit_q(3)
