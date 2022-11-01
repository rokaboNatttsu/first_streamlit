import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from copy import deepcopy
import numpy as np
from PIL import Image
from time import time

def choose_data(path, xy="x"):
    with st.form(key="input_info"+xy):
        nation_or_people = st.selectbox(
            "2変数の性質を選んでください",
            ("国単位の変数", "一人当たりの変数"),
        )
        st.form_submit_button("決定")
    if nation_or_people == "国単位の変数":
        path += "per_nation/"
    else:
        path += "per_person/"
            
    with st.form(key="input_info2"+xy):
        kind_of_variable = st.selectbox(
            "変数の種類を指定してください",
            ("成長率", "現地通貨建ての変数", "GDP比", "GDP比の増加幅", "人口"),
        )
        st.form_submit_button("決定")
    if kind_of_variable == "成長率":
        path += "growth_rate/"
    elif kind_of_variable == "現地通貨建ての変数":
        path += "national_currency_dbs/"
    elif kind_of_variable == "GDP比":
        path += "per_GDP/"
    elif kind_of_variable == "GDP比の増加幅":
        path += "diff_rate/"
    #else:   #   人口
    #    path +=

    files = os.listdir(path)
    value_name_lst = []
    for file_name in files:
        value_name, _ = file_name.split(".")
        value_name_lst.append(value_name)
        
    with st.form(key="input_info3"+xy):
        variable_name = st.selectbox(
            "変数を指定してください",
            tuple(value_name_lst),
        )
        st.form_submit_button("決定")
    path += variable_name + ".csv"
    db = pd.read_csv(path)
    st.dataframe(db)

    return db, variable_name


st.title("2変数に共通の設定")

nation_or_people, singleyear_of_midlespan = "",""
path = ""

with st.form(key="input_info1"):
    singleyear_of_midlespan = st.selectbox(
        "分析対象のデータの種類を選んでください",
        ("前年比データを使った分析", "2002と2020の比較による分析"),
    )
    st.form_submit_button("決定")
if singleyear_of_midlespan == "前年比データを使った分析":
    path = "data/calculated/SingleYear/"
else:
    path = "data/calculated/MidleRange/"


st.title("x軸の変数を指定")
db_x, x_db_name = choose_data(path)
st.text("\n\n\n")
st.title("y軸の変数を指定")
db_y, y_db_name = choose_data(path, xy="y")



st.text("\n\n\n")

class Plotter:
    def __init__(self, x_db, y_db, x_data_name, y_data_name):
        self.x_db = x_db
        self.y_db = y_db
        self.x_data_name = x_data_name
        self.y_data_name = y_data_name
        self.sovereign_currencies = [
            "Afghanistan","Albania","Australia","Belarus","Brazil","Canada","Chile",
            "Colombia","Czech Republic","Iceland","India","Israel","Japan","Kazakhstan",
            "Kenya","Korea","Malaysia","Mexico","Moldova","Morocco","New Zealand",
            "Pakistan","Paraguay","Peru","Philippines","Poland","Romania","Russia",
            "Singapore","South Africa","Sweden","Thailand","Turkey","United Kingdom",
            "United States",
        ]
        self.common_currencies = [
            "Austria","Belgium","Germany","Spain","France","Greece","Ireland","Italy",
            "Kosovo","Luxembourg","Montenegro","Netherlands","Portugal","Burkina Faso",
            "Senegal","Cameroon","Chad","Equatorial Guinea","Gabon","Republic of Congo",
            "Antigua and Barbuda","St Kitts and Nevis","St Lucia","St Vincent and the Grenadines",
        ]
        self.advanced_nation = [ 
            "Australia","Austria","Belgium","Canada","Czech Republic","Denmark","Finland",
            "France","Germany","Greece","Sweden","Ireland","Italy","Japan","Korea",
            "Luxembourg","Netherlands","New Zealand","Norway","Portugal","Spain",
            "Switzerland","United States","United Kingdom",
        ]

        self.drop_unfilled_countries()
    def drop_unfilled_countries(self):
        countries_lst = list(set(self.x_db["Country"]) & set(self.y_db["Country"]))
        M = min(len(list(self.x_db.columns)), len(list(self.y_db.columns)))
        col = ["Country"] + list(self.x_db.columns)[-M+1:]
        new_x_db = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=col)
        new_y_db = pd.DataFrame(np.zeros((len(countries_lst), M)), columns=col)
        new_x_db["Country"] = countries_lst
        new_y_db["Country"] = countries_lst
        for i, country in enumerate(countries_lst):
            t = list(self.x_db[self.x_db["Country"]==country].values[0])
            new_x_db.iloc[i,1:] = t[1:]
            t = list(self.y_db[self.y_db["Country"]==country].values[0])
            new_y_db.iloc[i,1:] = t[1:]

        self.x_db = new_x_db
        self.y_db = new_y_db
        
    def only_advanced_nations(self):
        t = deepcopy(self.advanced_nation)
        first_country = t.pop()
        new_x_db = self.x_db[self.x_db["Country"]==first_country].copy()
        new_y_db = self.y_db[self.y_db["Country"]==first_country].copy()
        while t:
            country = t.pop()
            new_x_db = pd.concat([new_x_db, self.x_db[self.x_db["Country"]==country].copy()])
            new_y_db = pd.concat([new_y_db, self.y_db[self.y_db["Country"]==country].copy()])
        new_x_db.sort_values("Country", inplace=True)
        new_y_db.sort_values("Country", inplace=True)
        new_x_db.reset_index(drop=True, inplace=True)
        new_y_db.reset_index(drop=True, inplace=True)
        return new_x_db, new_y_db
    
    def only_developing_country(self):
        t = deepcopy(self.advanced_nation)
        new_x_db = self.x_db.copy()
        new_y_db = self.y_db.copy()
        while t:
            country = t.pop()
            new_x_db = new_x_db[new_x_db["Country"]!=country].copy()
            new_y_db = new_y_db[new_y_db["Country"]!=country].copy()
        new_x_db.sort_values("Country", inplace=True)
        new_y_db.sort_values("Country", inplace=True)
        new_x_db.reset_index(drop=True, inplace=True)
        new_y_db.reset_index(drop=True, inplace=True)
        return new_x_db, new_y_db

    def only_sovereign_currencies(self):
        t = deepcopy(self.sovereign_currencies)
        first_country = t.pop()
        new_x_db = self.x_db[self.x_db["Country"]==first_country].copy()
        new_y_db = self.y_db[self.y_db["Country"]==first_country].copy()
        while t:
            country = t.pop()
            new_x_db = pd.concat([new_x_db, self.x_db[self.x_db["Country"]==country].copy()])
            new_y_db = pd.concat([new_y_db, self.y_db[self.y_db["Country"]==country].copy()])
        new_x_db.sort_values("Country", inplace=True)
        new_y_db.sort_values("Country", inplace=True)
        new_x_db.reset_index(drop=True, inplace=True)
        new_y_db.reset_index(drop=True, inplace=True)
        return new_x_db, new_y_db
    
    def only_common_currencies(self):
        t = deepcopy(self.common_currencies)
        first_country = t.pop()
        new_x_db = self.x_db[self.x_db["Country"]==first_country].copy()
        new_y_db = self.y_db[self.y_db["Country"]==first_country].copy()
        while t:
            country = t.pop()
            new_x_db = pd.concat([new_x_db, self.x_db[self.x_db["Country"]==country].copy()])
            new_y_db = pd.concat([new_y_db, self.y_db[self.y_db["Country"]==country].copy()])
        new_x_db.sort_values("Country", inplace=True)
        new_y_db.sort_values("Country", inplace=True)
        new_x_db.reset_index(drop=True, inplace=True)
        new_y_db.reset_index(drop=True, inplace=True)
        return new_x_db, new_y_db

    def range_scatter(self, xrange=[None, None], yrange=[None, None]):
        group = None
        with st.form(key="scatter"):
            group = st.selectbox(
                "分析対象の国の種類を選んでください",
                ("限定しない", "先進国限定", "発展途上国限定", "変動為替相場制と思われる国限定", "共通通貨使用国限定")
            )
            st.form_submit_button("確認")
        x_db, y_db, x_arr, y_arr = None, None, None, None
        if "限定しない" == group:
            x_db, y_db = self.x_db, self.y_db
            x_arr, y_arr = self.x_db.values, self.y_db.values
        elif "先進国限定" == group:
            x_db, y_db = self.only_advanced_nations()
            x_arr, y_arr = x_db.values, y_db.values
        elif "発展途上国限定" == group:
            x_db, y_db = self.only_developing_country()
            x_arr, y_arr = x_db.values, y_db.values
        elif "変動為替相場制と思われる国限定" == group:
            x_db, y_db = self.only_sovereign_currencies()
            x_arr, y_arr = x_db.values, y_db.values
        elif "共通通貨使用国限定" == group:
            x_db, y_db = self.only_common_currencies()
            x_arr, y_arr = x_db.values, y_db.values
        
        x_arr = np.array([x_arr[i][1:] for i in range(len(x_db))])
        y_arr = np.array([y_arr[i][1:] for i in range(len(y_db))])

        x_1d, y_1d = x_arr.reshape(len(x_arr)*len(x_arr[0,:])), y_arr.reshape(len(y_arr)*len(y_arr[0,:]))
        
        #   plt.subplotsでlen(groops)枚のグラフをプロット
        plt.scatter(x_1d, y_1d)
        plt.xlabel(self.x_data_name + " (%)", fontname="MS Gothic")
        plt.ylabel(self.y_data_name + " (%)", fontname="MS Gothic")
        plt.grid("both")
        plt.xlim(xrange)
        plt.ylim(yrange)
        t = str(time())
        fig_file_name = t+".png"
        plt.savefig("figs/"+t+".png")
        image = Image.open("figs/"+t+".png")
        st.image(image, width=750)

        country_lst = list(x_db["Country"])
        country_lst.sort()
        st.text("対象となった国の一覧")
        for country in country_lst:
            st.text(country)
        st.text("******************")

        return fig_file_name

    def range_hist2d(self, xrange=[None, None], yrange=[None, None], xybins=[100,100], logscale=True):
        group = None
        with st.form(key="heatmap"):
            group = st.selectbox(
                "分析対象の国の種類を選んでください",
                ("限定しない", "先進国限定", "発展途上国限定", "変動為替相場制と思われる国限定", "共通通貨使用国限定")
            )
            st.form_submit_button("確認")
        x_db, y_db, x_arr, y_arr = None, None, None, None
        if "限定しない" == group:
            x_db, y_db = self.x_db, self.y_db
            x_arr, y_arr = self.x_db.values, self.y_db.values
        elif "先進国限定" == group:
            x_db, y_db = self.only_advanced_nations()
            x_arr, y_arr = x_db.values, y_db.values
        elif "発展途上国限定" == group:
            x_db, y_db = self.only_developing_country()
            x_arr, y_arr = x_db.values, y_db.values
        elif "変動為替相場制と思われる国限定" == group:
            x_db, y_db = self.only_sovereign_currencies()
            x_arr, y_arr = x_db.values, y_db.values
        elif "共通通貨使用国限定" == group:
            x_db, y_db = self.only_common_currencies()
            x_arr, y_arr = x_db.values, y_db.values
        
        x_arr = np.array([x_arr[i][1:] for i in range(len(x_db))])
        y_arr = np.array([y_arr[i][1:] for i in range(len(y_db))])

        x_1d, y_1d = x_arr.reshape(len(x_arr[:,0])*len(x_arr[0,:])), y_arr.reshape(len(y_arr[:,0])*len(y_arr[0,:]))
        
        if logscale:
            plt.hist2d(x_1d, y_1d, bins=xybins, norm=LogNorm())
        else:
            plt.hist2d(x_1d, y_1d, bins=xybins)
        plt.xlabel(self.x_data_name + " (%)", fontname="MS Gothic")
        plt.ylabel(self.y_data_name + " (%)", fontname="MS Gothic")
        plt.grid("both")
        plt.colorbar()
        plt.xlim(xrange)
        plt.ylim(yrange)
        t = str(time())
        fig_file_name = t+".png"
        plt.savefig("figs/"+t+".png")
        image = Image.open("figs/"+t+".png")
        st.image(image, width=750)

        country_lst = list(x_db["Country"])
        country_lst.sort()
        st.text("対象となった国の一覧")
        for country in country_lst:
            st.text(country)
        st.text("******************")

        return fig_file_name


plotter = Plotter(db_x, db_y, x_db_name, y_db_name)

st.title("グラフの設定")
with st.form(key="plot"):
    graph_type = st.selectbox(
        "グラフの種類を選択",
        ("散布図", "ヒートマップ"),
    )
    st.form_submit_button("決定")
figfilename = None
if graph_type == "散布図":
    figfilename = plotter.range_scatter()
else:
    figfilename = plotter.range_hist2d()


for f in os.listdir("figs"):
    if f != figfilename:
        os.remove(os.path.join("figs", f))
