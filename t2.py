#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:41
# @Author  : Future Fu
# @FileName: t2.py

import os, sys

import os
import pandas as pd
import tushare as ts
import time
import datetime


if __name__ == '__main__':

 df = ts.get_today_all()
 file_name = str(datetime.date.today()) + '_Astock.csv'
 df.to_csv('./data/'+file_name)

 # ZhangTing_df = df[(df["changepercent"]>9.5) & (df["changepercent"]<10.5) ]
 ZhangTing_df = df[(df["changepercent"]>9.5)]
 print(ZhangTing_df.head(10))

#__行业词典__
 HangYe_df = pd.read_excel('./data/2020-02-07_ALL.xlsx')
 HangYe_df['code']= HangYe_df["股票代码"].map(lambda x:str(x)[:-3])

 ZhangTing_df['code'] = ZhangTing_df['code'].apply(str)
 HangYe_df['code'] = HangYe_df['code'].apply(str)
 temp = pd.merge(ZhangTing_df, HangYe_df, how="inner",
                on="code")
 print(temp.head())

 temp = temp[['股票代码', '股票简称', '所属同花顺行业',"amount"]]
 temp['成交量'] = temp[['amount']].apply(lambda x:x/100000000)


 temp = temp[['股票代码', '股票简称', '所属同花顺行业',"amount"]]
 temp['成交量'] = temp[['amount']].apply(lambda x:x/100000000)
 hangye_count_gb = temp.groupby(['所属同花顺行业'])
#print(hangye_count_gb['amount'].agg(['count', 'sum']))
 hangye_count_gb = (hangye_count_gb['amount'].agg(['count']).sort_values(by='count', ascending=False))
 hangye_count_gb.to_csv('./data/'+'s1.txt')
 print(hangye_count_gb)


 hangye_amt_gb = temp.groupby(['所属同花顺行业'])
 hangye_amt_gb = (hangye_amt_gb['成交量'].agg(['sum']).sort_values(by='sum', ascending=False))
#hangye_amt_gb = hangye_amt_gb.sort_values(ascending=False, inplace=True)
 hangye_amt_gb.to_csv('./data/'+'s2.txt')
 print(hangye_amt_gb)