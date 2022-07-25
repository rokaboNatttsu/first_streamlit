import numpy as np
import pandas as pd
from copy import deepcopy


def add(df1, df2):
    countries_lst = list(set(df1["Country"]) & set(df2["Country"]))
    M = len(list(df1.columns))
    df = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=list(df1.columns))
    df["Country"] = countries_lst
    for i, country in enumerate(countries_lst):
        t = np.array(df1[df1["Country"]==country].iloc[:,1:].values) + np.array(df2[df2["Country"]==country].iloc[:,1:].values)
        df.iloc[i,1:] = t[0]
    return df

def diff(df1, df2):
    countries_lst = list(set(df1["Country"]) & set(df2["Country"]))
    M = len(list(df1.columns))
    df = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=list(df1.columns))
    df["Country"] = countries_lst
    for i, country in enumerate(countries_lst):
        t = np.array(df1[df1["Country"]==country].iloc[:,1:].values) - np.array(df2[df2["Country"]==country].iloc[:,1:].values)
        df.iloc[i,1:] = t[0]
    return df

def times(df1, df2):
    countries_lst = list(set(df1["Country"]) & set(df2["Country"]))
    M = len(list(df1.columns))
    df = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=list(df1.columns))
    df["Country"] = countries_lst
    for i, country in enumerate(countries_lst):
        t = np.array(df1[df1["Country"]==country].iloc[:,1:].values) * np.array(df2[df2["Country"]==country].iloc[:,1:].values)
        df.iloc[i,1:] = t[0]
    return df

def dev(df1, df2):
    countries_lst = list(set(df1["Country"]) & set(df2["Country"]))
    M = len(list(df1.columns))
    df = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=list(df1.columns))
    df["Country"] = countries_lst
    for i, country in enumerate(countries_lst):
        t = np.array(df1[df1["Country"]==country].iloc[:,1:].values) / np.array(df2[df2["Country"]==country].iloc[:,1:].values)
        df.iloc[i,1:] = t[0]
    return df

def num_plus(df0, num):
    df = deepcopy(df0)
    df.iloc[:,1:] = df.iloc[:,1:] + num
    return df

def num_minus(df0, num):
    df = deepcopy(df0)
    df.iloc[:,1:] = df.iloc[:,1:] - num
    return df

def num_times(df0, num):
    df = deepcopy(df0)
    df.iloc[:,1:] = df.iloc[:,1:]*num
    return df

def num_div(df0, num):
    df = deepcopy(df0)
    df.iloc[:,1:] = df.iloc[:,1:]/num
    return df

def cal_growth_rate(df0):
    df = deepcopy(df0)
    del df[list(df0.columns)[1]]
    last_year_lst, current_year_lst = list(df0.columns)[1:-1], list(df0.columns)[2:]
    for last_year, current_year in zip(last_year_lst, current_year_lst):
        df[current_year] = 100*(df0[current_year] - df0[last_year])/df0[last_year]
    return df

def cal_diff_rate(df0):
    df = deepcopy(df0)
    del df[list(df0.columns)[1]]
    last_year_lst, current_year_lst = list(df0.columns)[1:-1], list(df0.columns)[2:]
    for last_year, current_year in zip(last_year_lst, current_year_lst):
        df[current_year] = df0[current_year] - df0[last_year]
    return df


def output_SingleYear_data(population_db=None):
    national_currency_valiable_dic, per_GDP_dic, growth_rate_dic, diff_rate_dic = {}, {}, {}, {}

    if population_db is None:
        national_currency_valiable_dic["名目GDP"] = pd.read_csv("data/originals/名目GDP.csv")
        national_currency_valiable_dic["実質GDP"] = pd.read_csv("data/originals/実質GDP.csv")
        national_currency_valiable_dic["名目政府収入"] = pd.read_csv("data/originals/名目政府収入.csv")
        national_currency_valiable_dic["名目政府支出"] = pd.read_csv("data/originals/名目政府支出.csv")
        national_currency_valiable_dic["CPI"] = pd.read_csv("data/originals/CPI.csv")
        per_GDP_dic["最終消費支出対GDP比"] = pd.read_csv("data/originals/最終消費支出対GDP比.csv")
        per_GDP_dic["政府最終消費支出対GDP比"] = pd.read_csv("data/originals/政府最終消費支出対GDP比.csv")
        per_GDP_dic["総投資対GDP比"] = pd.read_csv("data/originals/総投資対GDP比.csv")
        per_GDP_dic["経常収支対GDP比"] = pd.read_csv("data/originals/経常収支対GDP比.csv")
        per_GDP_dic["輸出対GDP比"] = pd.read_csv("data/originals/輸出対GDP比.csv")
        per_GDP_dic["輸入対GDP比"] = pd.read_csv("data/originals/輸入対GDP比.csv")
    else:
        national_currency_valiable_dic["名目GDP"] = dev(pd.read_csv("data/originals/名目GDP.csv"), population_db)
        national_currency_valiable_dic["実質GDP"] = dev(pd.read_csv("data/originals/実質GDP.csv"), population_db)
        national_currency_valiable_dic["名目政府収入"] = dev(pd.read_csv("data/originals/名目政府収入.csv"), population_db)
        national_currency_valiable_dic["名目政府支出"] = dev(pd.read_csv("data/originals/名目政府支出.csv"), population_db)
        national_currency_valiable_dic["CPI"] = pd.read_csv("data/originals/CPI.csv")
        per_GDP_dic["最終消費支出対GDP比"] = dev(pd.read_csv("data/originals/最終消費支出対GDP比.csv"), population_db)
        per_GDP_dic["政府最終消費支出対GDP比"] = dev(pd.read_csv("data/originals/政府最終消費支出対GDP比.csv"), population_db)
        per_GDP_dic["総投資対GDP比"] = dev(pd.read_csv("data/originals/総投資対GDP比.csv"), population_db)
        per_GDP_dic["経常収支対GDP比"] = dev(pd.read_csv("data/originals/経常収支対GDP比.csv"), population_db)
        per_GDP_dic["輸出対GDP比"] = dev(pd.read_csv("data/originals/輸出対GDP比.csv"), population_db)
        per_GDP_dic["輸入対GDP比"] = dev(pd.read_csv("data/originals/輸入対GDP比.csv"), population_db)

    #   ここから変数の追加
    national_currency_valiable_dic["GDPデフレータ"] = dev(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["実質GDP"])
    national_currency_valiable_dic["実質政府収入"] = dev(national_currency_valiable_dic["名目政府収入"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["実質政府支出"] = dev(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目輸出"] = num_div(times(per_GDP_dic["輸出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["名目輸入"] = num_div(times(per_GDP_dic["輸入対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質輸出"] = times(national_currency_valiable_dic["名目輸出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["実質輸入"] = times(national_currency_valiable_dic["名目輸入"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目貿易収支"] = diff(national_currency_valiable_dic["名目輸出"], national_currency_valiable_dic["実質輸入"])
    national_currency_valiable_dic["実質貿易収支"] = diff(national_currency_valiable_dic["実質輸出"], national_currency_valiable_dic["実質輸入"])
    per_GDP_dic["民間最終消費支出対GDP比"] = diff(per_GDP_dic["最終消費支出対GDP比"], per_GDP_dic["政府最終消費支出対GDP比"])
    national_currency_valiable_dic["名目民間最終消費支出"] = times(national_currency_valiable_dic["名目GDP"], num_div(per_GDP_dic["民間最終消費支出対GDP比"], 100))
    national_currency_valiable_dic["実質民間最終消費支出"] = dev(national_currency_valiable_dic["名目民間最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目最終消費支出"] = times(national_currency_valiable_dic["名目GDP"], num_div(per_GDP_dic["最終消費支出対GDP比"], 100))
    national_currency_valiable_dic["実質最終消費支出"] = dev(national_currency_valiable_dic["名目最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])
    tdf = diff(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["名目政府支出"])
    national_currency_valiable_dic["名目民間付加価値生産額"] = diff(tdf, national_currency_valiable_dic["名目貿易収支"])
    national_currency_valiable_dic["実質民間付加価値生産額"] = diff(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目民間投資支出"] = diff(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目民間最終消費支出"])
    national_currency_valiable_dic["実質民間投資支出"] = dev(national_currency_valiable_dic["名目民間投資支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目財政収支"] = diff(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目政府収入"])
    national_currency_valiable_dic["実質財政収支"] = diff(national_currency_valiable_dic["名目財政収支"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目経常収支"] = num_div(times(per_GDP_dic["経常収支対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質経常収支"] = num_div(times(per_GDP_dic["経常収支対GDP比"], national_currency_valiable_dic["実質GDP"]), 100)
    national_currency_valiable_dic["名目民間収支"] = diff(national_currency_valiable_dic["名目経常収支"], national_currency_valiable_dic["名目財政収支"])
    national_currency_valiable_dic["実質民間収支"] = diff(national_currency_valiable_dic["実質経常収支"], national_currency_valiable_dic["実質財政収支"])
    national_currency_valiable_dic["名目政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["実質GDP"]), 100)
    national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目政府最終消費支出"])
    national_currency_valiable_dic["実質政府の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["実質政府支出"], national_currency_valiable_dic["実質政府最終消費支出"])
    tdf = diff(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["名目最終消費支出"])
    national_currency_valiable_dic["名目国内総資本形成"] = diff(tdf, national_currency_valiable_dic["名目貿易収支"])
    national_currency_valiable_dic["実質国内総資本形成"] = dev(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目民間の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"])
    national_currency_valiable_dic["実質民間の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["実質国内総資本形成"], national_currency_valiable_dic["実質政府の発注がきっかけの総資本形成"])
    national_currency_valiable_dic["名目政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質政府最終消費支出"] = dev(national_currency_valiable_dic["名目政府最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])

    per_GDP_dic["政府支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間付加価値生産額対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["貿易収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目貿易収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間最終消費支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間最終消費支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間付加価値生産額対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間投資支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間投資支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["財政収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目財政収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["経常収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目経常収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["政府の発注がきっかけの総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["国内総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間の発注がきっかけの総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間の発注がきっかけの総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)


    #   成長率の計算
    for label_name in national_currency_valiable_dic:
        if "収支" in label_name:
            continue
        if label_name == "CPI":
            growth_rate_dic["インフレ率"] = cal_growth_rate(national_currency_valiable_dic[label_name])
        else:
            growth_rate_dic[label_name+"成長率"] = cal_growth_rate(national_currency_valiable_dic[label_name])

    #   増加幅の計算
    for label_name in per_GDP_dic:
        diff_rate_dic[label_name+"の増加幅"] = cal_diff_rate(per_GDP_dic[label_name])


    if population_db is None:
        for label_name in national_currency_valiable_dic:
            national_currency_valiable_dic[label_name].sort_values("Country", inplace=True)
            national_currency_valiable_dic[label_name].to_csv("data/calculated/SingleYear/per_nation/national_currency_variables/"+label_name+".csv", index=False)

        for label_name in per_GDP_dic:
            per_GDP_dic[label_name].sort_values("Country", inplace=True)
            per_GDP_dic[label_name].to_csv("data/calculated/SingleYear/per_nation/per_GDP/"+label_name+".csv", index=False)

        for label_name in growth_rate_dic:
            growth_rate_dic[label_name].sort_values("Country", inplace=True)
            growth_rate_dic[label_name].to_csv("data/calculated/SingleYear/per_nation/growth_rate/"+label_name+".csv", index=False)

        for label_name in diff_rate_dic:
            diff_rate_dic[label_name].sort_values("Country", inplace=True)
            diff_rate_dic[label_name].to_csv("data/calculated/SingleYear/per_nation/diff_rate/"+label_name+".csv", index=False)
    else:
        for label_name in national_currency_valiable_dic:
            national_currency_valiable_dic[label_name].sort_values("Country", inplace=True)
            national_currency_valiable_dic[label_name].to_csv("data/calculated/SingleYear/per_person/national_currency_variables/"+label_name+".csv", index=False)

        for label_name in per_GDP_dic:
            per_GDP_dic[label_name].sort_values("Country", inplace=True)
            per_GDP_dic[label_name].to_csv("data/calculated/SingleYear/per_person/per_GDP/"+label_name+".csv", index=False)

        for label_name in growth_rate_dic:
            growth_rate_dic[label_name].sort_values("Country", inplace=True)
            growth_rate_dic[label_name].to_csv("data/calculated/SingleYear/per_person/growth_rate/"+label_name+".csv", index=False)

        for label_name in diff_rate_dic:
            diff_rate_dic[label_name].sort_values("Country", inplace=True)
            diff_rate_dic[label_name].to_csv("data/calculated/SingleYear/per_person/diff_rate/"+label_name+".csv", index=False)

def read_data_and_cut_interval(data_name):
    df = pd.read_csv("data/originals/"+data_name+".csv")
    df = df.iloc[:,[0,1,-1]]
    return df

def output_MidleRsnge_data(population_db=None):
    national_currency_valiable_dic, per_GDP_dic, growth_rate_dic, diff_rate_dic = {}, {}, {}, {}

    if population_db is None:
        national_currency_valiable_dic["名目GDP"] = read_data_and_cut_interval("名目GDP")
        national_currency_valiable_dic["実質GDP"] = read_data_and_cut_interval("実質GDP")
        national_currency_valiable_dic["名目政府収入"] = read_data_and_cut_interval("名目政府収入")
        national_currency_valiable_dic["名目政府支出"] = read_data_and_cut_interval("名目政府支出")
        national_currency_valiable_dic["CPI"] = read_data_and_cut_interval("CPI")
        per_GDP_dic["最終消費支出対GDP比"] = read_data_and_cut_interval("最終消費支出対GDP比")
        per_GDP_dic["政府最終消費支出対GDP比"] = read_data_and_cut_interval("政府最終消費支出対GDP比")
        per_GDP_dic["総投資対GDP比"] = read_data_and_cut_interval("総投資対GDP比")
        per_GDP_dic["経常収支対GDP比"] = read_data_and_cut_interval("経常収支対GDP比")
        per_GDP_dic["輸出対GDP比"] = read_data_and_cut_interval("輸出対GDP比")
        per_GDP_dic["輸入対GDP比"] = read_data_and_cut_interval("輸入対GDP比")
    else:
        national_currency_valiable_dic["名目GDP"] = dev(read_data_and_cut_interval("名目GDP"), population_db)
        national_currency_valiable_dic["実質GDP"] = dev(read_data_and_cut_interval("実質GDP"), population_db)
        national_currency_valiable_dic["名目政府収入"] = dev(read_data_and_cut_interval("名目政府収入"), population_db)
        national_currency_valiable_dic["名目政府支出"] = dev(read_data_and_cut_interval("名目政府支出"), population_db)
        national_currency_valiable_dic["CPI"] = read_data_and_cut_interval("CPI")
        per_GDP_dic["最終消費支出対GDP比"] = dev(read_data_and_cut_interval("最終消費支出対GDP比"), population_db)
        per_GDP_dic["政府最終消費支出対GDP比"] = dev(read_data_and_cut_interval("政府最終消費支出対GDP比"), population_db)
        per_GDP_dic["総投資対GDP比"] = dev(read_data_and_cut_interval("総投資対GDP比"), population_db)
        per_GDP_dic["経常収支対GDP比"] = dev(read_data_and_cut_interval("経常収支対GDP比"), population_db)
        per_GDP_dic["輸出対GDP比"] = dev(read_data_and_cut_interval("輸出対GDP比"), population_db)
        per_GDP_dic["輸入対GDP比"] = dev(read_data_and_cut_interval("輸入対GDP比"), population_db)

    #   ここから変数の追加
    national_currency_valiable_dic["GDPデフレータ"] = dev(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["実質GDP"])
    national_currency_valiable_dic["実質政府収入"] = dev(national_currency_valiable_dic["名目政府収入"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["実質政府支出"] = dev(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目輸出"] = num_div(times(per_GDP_dic["輸出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["名目輸入"] = num_div(times(per_GDP_dic["輸入対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質輸出"] = times(national_currency_valiable_dic["名目輸出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["実質輸入"] = times(national_currency_valiable_dic["名目輸入"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目貿易収支"] = diff(national_currency_valiable_dic["名目輸出"], national_currency_valiable_dic["実質輸入"])
    national_currency_valiable_dic["実質貿易収支"] = diff(national_currency_valiable_dic["実質輸出"], national_currency_valiable_dic["実質輸入"])
    per_GDP_dic["民間最終消費支出対GDP比"] = diff(per_GDP_dic["最終消費支出対GDP比"], per_GDP_dic["政府最終消費支出対GDP比"])
    national_currency_valiable_dic["名目民間最終消費支出"] = times(national_currency_valiable_dic["名目GDP"], num_div(per_GDP_dic["民間最終消費支出対GDP比"], 100))
    national_currency_valiable_dic["実質民間最終消費支出"] = dev(national_currency_valiable_dic["名目民間最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目最終消費支出"] = times(national_currency_valiable_dic["名目GDP"], num_div(per_GDP_dic["最終消費支出対GDP比"], 100))
    national_currency_valiable_dic["実質最終消費支出"] = dev(national_currency_valiable_dic["名目最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])
    tdf = diff(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["名目政府支出"])
    national_currency_valiable_dic["名目民間付加価値生産額"] = diff(tdf, national_currency_valiable_dic["名目貿易収支"])
    national_currency_valiable_dic["実質民間付加価値生産額"] = diff(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目民間投資支出"] = diff(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目民間最終消費支出"])
    national_currency_valiable_dic["実質民間投資支出"] = dev(national_currency_valiable_dic["名目民間投資支出"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目財政収支"] = diff(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目政府収入"])
    national_currency_valiable_dic["実質財政収支"] = diff(national_currency_valiable_dic["名目財政収支"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目経常収支"] = num_div(times(per_GDP_dic["経常収支対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質経常収支"] = num_div(times(per_GDP_dic["経常収支対GDP比"], national_currency_valiable_dic["実質GDP"]), 100)
    national_currency_valiable_dic["名目民間収支"] = diff(national_currency_valiable_dic["名目経常収支"], national_currency_valiable_dic["名目財政収支"])
    national_currency_valiable_dic["実質民間収支"] = diff(national_currency_valiable_dic["実質経常収支"], national_currency_valiable_dic["実質財政収支"])
    national_currency_valiable_dic["名目政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["実質GDP"]), 100)
    national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目政府最終消費支出"])
    national_currency_valiable_dic["実質政府の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["実質政府支出"], national_currency_valiable_dic["実質政府最終消費支出"])
    tdf = diff(national_currency_valiable_dic["名目GDP"], national_currency_valiable_dic["名目最終消費支出"])
    national_currency_valiable_dic["名目国内総資本形成"] = diff(tdf, national_currency_valiable_dic["名目貿易収支"])
    national_currency_valiable_dic["実質国内総資本形成"] = dev(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["GDPデフレータ"])
    national_currency_valiable_dic["名目民間の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"])
    national_currency_valiable_dic["実質民間の発注がきっかけの総資本形成"] = diff(national_currency_valiable_dic["実質国内総資本形成"], national_currency_valiable_dic["実質政府の発注がきっかけの総資本形成"])
    national_currency_valiable_dic["名目政府最終消費支出"] = num_div(times(per_GDP_dic["政府最終消費支出対GDP比"], national_currency_valiable_dic["名目GDP"]), 100)
    national_currency_valiable_dic["実質政府最終消費支出"] = dev(national_currency_valiable_dic["名目政府最終消費支出"], national_currency_valiable_dic["GDPデフレータ"])

    per_GDP_dic["政府支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目政府支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間付加価値生産額対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["貿易収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目貿易収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間最終消費支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間最終消費支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間付加価値生産額対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間付加価値生産額"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間投資支出対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間投資支出"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["財政収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目財政収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["経常収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目経常収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間収支対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間収支"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["政府の発注がきっかけの総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目政府の発注がきっかけの総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["国内総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目国内総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)
    per_GDP_dic["民間の発注がきっかけの総資本形成対GDP比"] = num_times(dev(national_currency_valiable_dic["名目民間の発注がきっかけの総資本形成"], national_currency_valiable_dic["名目GDP"]), 100)


    #   成長率の計算
    for label_name in national_currency_valiable_dic:
        if "収支" in label_name:
            continue
        growth_rate_dic[label_name+"成長率"] = cal_growth_rate(national_currency_valiable_dic[label_name])

    #   増加幅の計算
    for label_name in per_GDP_dic:
        diff_rate_dic[label_name+"の増加幅"] = cal_diff_rate(per_GDP_dic[label_name])


    if population_db is None:
        for label_name in national_currency_valiable_dic:
            national_currency_valiable_dic[label_name].sort_values("Country", inplace=True)
            national_currency_valiable_dic[label_name].to_csv("data/calculated/MidleRange/per_nation/national_currency_variables/"+label_name+".csv", index=False)

        for label_name in per_GDP_dic:
            per_GDP_dic[label_name].sort_values("Country", inplace=True)
            per_GDP_dic[label_name].to_csv("data/calculated/MidleRange/per_nation/per_GDP/"+label_name+".csv", index=False)

        for label_name in growth_rate_dic:
            growth_rate_dic[label_name].sort_values("Country", inplace=True)
            growth_rate_dic[label_name].to_csv("data/calculated/MidleRange/per_nation/growth_rate/"+label_name+".csv", index=False)

        for label_name in diff_rate_dic:
            diff_rate_dic[label_name].sort_values("Country", inplace=True)
            diff_rate_dic[label_name].to_csv("data/calculated/MidleRange/per_nation/diff_rate/"+label_name+".csv", index=False)
    else:
        for label_name in national_currency_valiable_dic:
            national_currency_valiable_dic[label_name].sort_values("Country", inplace=True)
            national_currency_valiable_dic[label_name].to_csv("data/calculated/MidleRange/per_person/national_currency_variables/"+label_name+".csv", index=False)

        for label_name in per_GDP_dic:
            per_GDP_dic[label_name].sort_values("Country", inplace=True)
            per_GDP_dic[label_name].to_csv("data/calculated/MidleRange/per_person/per_GDP/"+label_name+".csv", index=False)

        for label_name in growth_rate_dic:
            growth_rate_dic[label_name].sort_values("Country", inplace=True)
            growth_rate_dic[label_name].to_csv("data/calculated/MidleRange/per_person/growth_rate/"+label_name+".csv", index=False)

        for label_name in diff_rate_dic:
            diff_rate_dic[label_name].sort_values("Country", inplace=True)
            diff_rate_dic[label_name].to_csv("data/calculated/MidleRange/per_person/diff_rate/"+label_name+".csv", index=False)




population_db = pd.read_csv("data/originals/人口.csv")
output_SingleYear_data()
output_SingleYear_data(population_db=population_db)

population_db = read_data_and_cut_interval("人口")
output_MidleRsnge_data()
output_MidleRsnge_data(population_db=population_db)

