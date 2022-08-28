# Fix for 2023:
# clear button to clear name from selection
# shift select name to highest person not drafted
# program crashes when you click on ranking above #1 in pos/ovr list
# program crashes when you sort selection list by pos
# backup to excel occasionally to reduce risk of crash

from bs4 import BeautifulSoup
import xlsxwriter
import requests
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import pickle
from difflib import *
from peewee import *
from player import Player
import pandas as pd
import cProfile
import sys
import numpy as np
import json
import urllib
import yfpy
from yfpy.logger import get_logger
from yfpy.models import Scoreboard, Settings, Standings, League
from yfpy.utils import prettify_data
from pybaseball import playerid_lookup
from pybaseball import batting_stats_range
from pybaseball import pitching_stats_range
from datetime import datetime, timedelta
from math import isnan
from unidecode import unidecode

import requests
from requests.packages.urllib3 import add_stderr_logger
import urllib
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen
import re, random

from requests.auth import HTTPBasicAuth
import requests

import time

http_proxy = "http://136.24.129.31:3128"
https_proxy = "http://136.24.129.31:3128"
ftp_proxy = "http://136.24.129.31:3128"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


def log(message):
    debug = False
    if debug:
        print(message)


def write_array(worksheet, array, header):
    myheader = ['']

    if type(header) == type([]): #  if header is already a list
        myheader = header
    if header == 'hitter':
        myheader = ['Name', 'Team', 'POS1', 'POS2', 'POS3', 'H', 'AB', 'R', 'HR',
                    'RBI', 'SB', 'AVG', 'OBP', 'SLG', 'OPS', 'BB', 'K']
    elif header == 'pitcher':
        myheader = ['Name', 'Team', 'POS1', 'POS2', 'G', 'GS', 'IP', 'K', 'QS',
                    'SV', 'HLD', 'SVHD', 'ERA', 'WHIP', 'W', 'BB', 'K/9']
    elif header == 'lineup':
        myheader = ['Name', 'Order']
    elif header == 'plist':
        myheader = ['Name', 'Rank']
    elif header == 'prices':
        myheader = ['Name', 'Price']

    for col, i in enumerate(myheader):
        worksheet.write(0, col, i)


    for row, i in enumerate(array):
        if header == 'plist':
            worksheet.write(row + 1, 0, i)
            worksheet.write(row + 1, 1, row+1)
        else:
            for col in range(len(i)):
                cell = i[col]
                # if cell != cell: #  checks for nan
                #     cell = 0
                try:
                    worksheet.write(row + 1, col, cell)
                except:
                    worksheet.write(row + 1, col, 0)


def changenames(targetlist, mylist):
    targetnames = []
    targetpos = []
    for i in range(len(targetlist)):
        tpos = ''
        if isinstance(targetlist[i][1], str):
            tpos = targetlist[i][1]
        targetnames.append(targetlist[i][0])
        targetpos.append(tpos)

    mynames = []
    for i in range(len(mylist)):
        mypos = ''
        if isinstance(mylist[i][1], str):
            mypos = mylist[i][1]
        mynames.append([mylist[i][0],mypos])

    renamed = []
    found = 0
    notfound = 0

    for rank, i in enumerate(mynames):
        if i[0] in targetnames:
            log('Exact Name Found - ' + i[0])
            pass
        else:
            matches = get_close_matches(i[0], targetnames, 3, .75)
            if matches:
                targindex = targetnames.index(matches[0])
                name = targetnames[targindex]
                if targetpos[targindex].lower() == i[1].lower() or i[1].lower() == '':
                    mylist[rank][0] = name
                    log('FOUND CLOSE MATCH: ' + i[0] + '  -  ' + targetnames[targindex] + '   ' + str(rank))
                    found = found+1
                    renamed.append([i[0], name])
                else:
                    log('NO MATCH FOUND ' + i[0])
                    notfound = notfound + 1
            else:
                log('NO MATCH FOUND ' + i[0])
                notfound = notfound+1

    return mylist

def getrank(name, mylist):
    # print(name)
    # print(list)
    try:
        rnk = mylist.index(name)+1
    except:
        #Return 999 if name was not found
        rnk = 999

    return rnk

def get_all_sources(source):

    if source == 'pickle':
        # Grabbing espn data from 2020.  this should be ignored
        # f = open('store2.pckl', 'rb')
        # [espnh, espnp, prices_h, prices_p, fpros_h, fpros_p, lineups, plist] = pickle.load(f)
        # f.close()

        season_stats_h = pd.DataFrame()
        last15_stats_h = pd.DataFrame()
        last7_stats_h = pd.DataFrame()
        season_stats_p = pd.DataFrame()
        last15_stats_p = pd.DataFrame()
        last7_stats_p = pd.DataFrame()

        # This is 2022 projected data from fantasypros
        f = open('store.pckl', 'rb')
        # f = open('store.pckl', 'rb')
        # [espnh, espnp, prices_h, prices_p, fpros_h, fpros_p, lineups, plist] = pickle.load(f)
        [prices_h, prices_p, fpros_h, fpros_p, lineups, plist, rplist, availdf, hranks, pranks] = pickle.load(f)
        f.close()
    else:
        # Grabbing espn data from 2020.  this should be ignored
        # f = open('store2.pckl', 'rb')
        # [espnh, espnp, prices_h, prices_p, fpros_h, fpros_p, lineups, plist] = pickle.load(f)
        # f.close()


        # Prices manually grabbed from yahoo
        prices_h = [["Trea Turner", 53], ["Vladimir Guerrero Jr.", 50], ["Juan Soto", 50], ["Fernando Tatis Jr.", 50], ["Jose Ramirez", 47], ["Bo Bichette", 47], ["Ronald Acuna Jr.", 44], ["Mookie Betts", 44], ["Bryce Harper", 43], ["Shohei Ohtani", 41], ["Mike Trout", 40], ["Freddie Freeman", 38], ["Kyle Tucker", 37], ["Rafael Devers", 35], ["Luis Robert", 34], ["Starling Marte", 33], ["Ozzie Albies", 32], ["Yordan Alvarez", 32], ["Manny Machado", 29], ["Xander Bogaerts", 28], ["Aaron Judge", 28], ["Tim Anderson", 28], ["Matt Olson", 27], ["Marcus Semien", 27], ["Whit Merrifield", 26], ["Salvador Perez", 25], ["Teoscar Hernandez", 25], ["Cedric Mullins", 25], ["Trevor Story", 24], ["Austin Riley", 24], ["Francisco Lindor", 23], ["Wander Franco", 23], ["Nick Castellanos", 22], ["Eloy Jimenez", 22], ["Randy Arozarena", 21], ["Nolan Arenado", 21], ["Paul Goldschmidt", 21], ["Byron Buxton", 20], ["J.D. Martinez", 20], ["Pete Alonso", 20], ["Jose Altuve", 20], ["Alex Bregman", 20], ["George Springer", 20], ["Jose Abreu", 20], ["Adalberto Mondesi", 20], ["Javier Baez", 19], ["Corey Seager", 18], ["Tyler O'Neill", 18], ["Giancarlo Stanton", 18], ["Christian Yelich", 17], ["Kris Bryant", 17], ["Brandon Lowe", 17], ["Carlos Correa", 17], ["J.T. Realmuto", 16], ["Anthony Rendon", 16], ["Jazz Chisholm Jr.", 15], ["Will Smith", 15], ["Jonathan India", 15], ["Cody Bellinger", 15], ["Ketel Marte", 14], ["Mitch Haniger", 13], ["Jesse Winker", 13], ["Jared Walsh", 13], ["Jorge Polanco", 13], ["DJ LeMahieu", 12], ["Bryan Reynolds", 12], ["Ryan Mountcastle", 11], ["Franmil Reyes", 11], ["Nelson Cruz", 11], ["Max Muncy", 10], ["Kyle Schwarber", 10], ["Tommy Edman", 10], ["Austin Meadows", 9], ["Trent Grisham", 9], ["Bobby Witt Jr.", 9], ["C.J. Cron", 9], ["Dansby Swanson", 8], ["Yoan Moncada", 8], ["Chris Taylor", 8], ["Jake Cronenworth", 8], ["Rhys Hoskins", 8], ["Josh Bell", 7], ["Matt Chapman", 7], ["Willson Contreras", 7], ["Yasmani Grandal", 7], ["Michael Conforto", 6], ["Lourdes Gurriel Jr.", 6], ["Anthony Rizzo", 6], ["Seiya Suzuki", 6], ["Joey Gallo", 5], ["Avisail Garcia", 5], ["Trey Mancini", 5], ["Justin Turner", 5], ["Joey Votto", 4], ["Daulton Varsho", 4], ["Jarred Kelenic", 4], ["Michael Brantley", 4], ["Willy Adames", 4], ["Gleyber Torres", 3], ["Dylan Carlson", 3], ["Jorge Soler", 3], ["Hunter Renfroe", 3], ["Marcell Ozuna", 3], ["Eugenio Suarez", 3], ["Julio Rodriguez", 3], ["Ty France", 3], ["Yuli Gurriel", 3], ["Alex Verdugo", 3], ["Adam Duvall", 3], ["Randal Grichuk", 3], ["Ryan McMahon", 3], ["Ke'Bryan Hayes", 3], ["Josh Donaldson", 3], ["Ian Happ", 3], ["Adolis Garcia", 3], ["Mark Canha", 2], ["Austin Hays", 2], ["Myles Straw", 2], ["Frank Schwindel", 2], ["Luke Voit", 2], ["Keibert Ruiz", 2], ["Adley Rutschman", 2], ["Ramon Laureano", 2], ["Eduardo Escobar", 2], ["Andrew Benintendi", 2], ["Abraham Toro", 2], ["Travis d'Arnaud", 2], ["Spencer Torkelson", 2], ["Tyler Stephenson", 2], ["Gary Sanchez", 2], ["Robbie Grossman", 2], ["Tommy Pham", 2], ["Andrew Vaughn", 2], ["Jean Segura", 2], ["Brendan Rodgers", 2], ["Jonathan Villar", 2], ["Alejandro Kirk", 2], ["Charlie Blackmon", 2], ["Oneil Cruz", 2], ["Eddie Rosario", 2], ["Patrick Wisdom", 2], ["Mike Moustakas", 2], ["Adam Frazier", 2], ["Mitch Garver", 2], ["AJ Pollock", 2], ["Raimel Tapia", 2], ["Jo Adell", 2], ["Alex Kirilloff", 1], ["Nathaniel Lowe", 1], ["Jonathan Schoop", 1], ["Bobby Dalbec", 1], ["Eric Hosmer", 1], ["Luis Urias", 1], ["Jeff McNeil", 1], ["Gio Urshela", 1], ["Christian Vazquez", 1], ["Eric Haase", 1], ["Wil Myers", 1], ["Andrew McCutchen", 1], ["Jarren Duran", 1], ["Brandon Crawford", 1], ["Amed Rosario", 1], ["Isiah Kiner-Falefa", 1], ["Nicky Lopez", 1], ["Paul DeJong", 1], ["J.P. Crawford", 1], ["Brandon Belt", 1], ["Miguel Sano", 1], ["Kolten Wong", 1], ["Josh Rojas", 1], ["Kike Hernandez", 1], ["Joey Wendle", 1], ["David Fletcher", 1], ["Vidal Brujan", 1], ["Alec Bohm", 1], ["Cavan Biggio", 1], ["James McCann", 1], ["Kyle Lewis", 1], ["Max Kepler", 1], ["Jesus Aguilar", 1], ["Connor Joe", 1], ["Carlos Santana", 1], ["Gavin Lux", 1], ["Garrett Hampson", 1], ["Josh Harrison", 1], ["Luis Arraez", 1], ["Mike Zunino", 1], ["Sean Murphy", 1], ["Omar Narvaez", 1], ["Harrison Bader", 1], ["Anthony Santander", 1], ["Mike Yastrzemski", 1], ["Akil Baddoo", 1], ["LaMonte Wade Jr.", 1], ["Wilmer Flores", 1], ["Andres Gimenez", 1], ["Jeimer Candelario", 1], ["Yadier Molina", 1], ["Brandon Nimmo", 1], ["Jesus Sanchez", 1], ["Lorenzo Cain", 1], ["Rowdy Tellez", 1], ["Christian Walker", 1], ["Bobby Bradley", 1], ["Yoshi Tsutsugo", 1], ["Dominic Smith", 1], ["Pavin Smith", 1], ["Yandy Diaz", 1], ["Jurickson Profar", 1], ["Cesar Hernandez", 1], ["Nick Solak", 1], ["Nick Madrigal", 1], ["Nick Senzel", 1], ["Nico Hoerner", 1], ["Evan Longoria", 1], ["Josh Jung", 1], ["Carson Kelly", 1], ["Elias Diaz", 1], ["Austin Nola", 1], ["Tucker Barnhart", 1], ["Yan Gomes", 1], ["Joc Pederson", 1], ["David Peralta", 1], ["Willie Calhoun", 1], ["Lane Thomas", 1], ["Victor Robles", 1], ["Manuel Margot", 1], ["Josh Lowe", 1], ["Rafael Ortega", 1], ["Harold Ramirez", 1], ["Tyler Naquin", 1], ["Didi Gregorius", 1], ["Miguel Rojas", 1], ["Seth Beer", 1]]
        prices_p = [["Gerrit Cole", 43], ["Corbin Burnes", 40], ["Walker Buehler", 34], ["Max Scherzer", 34], ["Jacob deGrom", 33], ["Brandon Woodruff", 31], ["Shane Bieber", 29], ["Zack Wheeler", 28], ["Julio Urias", 27], ["Josh Hader", 24], ["Lucas Giolito", 23], ["Liam Hendriks", 23], ["Aaron Nola", 22], ["Lance Lynn", 21], ["Shohei Ohtani", 21], ["Sandy Alcantara", 21], ["Robbie Ray", 21], ["Freddy Peralta", 20], ["Kevin Gausman", 19], ["Chris Sale", 19], ["Max Fried", 18], ["Jose Berrios", 18], ["Jack Flaherty", 18], ["Luis Castillo", 17], ["Raisel Iglesias", 15], ["Joe Musgrove", 15], ["Aroldis Chapman", 15], ["Charlie Morton", 14], ["Frankie Montas", 14], ["Carlos Rodon", 14], ["Yu Darvish", 14], ["Alek Manoah", 14], ["Logan Webb", 13], ["Emmanuel Clase", 13], ["Trevor Rogers", 12], ["Dylan Cease", 12], ["Blake Snell", 11], ["Shane McClanahan", 11], ["Ryan Pressly", 11], ["Edwin Diaz", 11], ["Clayton Kershaw", 10], ["Pablo Lopez", 9], ["Jordan Romano", 8], ["Zac Gallen", 8], ["Giovanny Gallegos", 8], ["Chris Bassitt", 8], ["Ian Anderson", 8], ["Kenley Jansen", 7], ["Tyler Mahle", 7], ["Justin Verlander", 7], ["Framber Valdez", 7], ["Will Smith", 6], ["Eduardo Rodriguez", 6], ["Blake Treinen", 6], ["Sonny Gray", 6], ["Lance McCullers Jr.", 6], ["Nathan Eovaldi", 5], ["Trevor Bauer", 5], ["Mark Melancon", 4], ["Sean Manaea", 4], ["Scott Barlow", 4], ["Joe Barlow", 4], ["Michael Kopech", 4], ["Luis Garcia", 4], ["Mike Clevinger", 4], ["Jake McGee", 3], ["Corey Knebel", 3], ["Shane Baz", 3], ["Luis Severino", 3], ["Adam Wainwright", 3], ["Ranger Suarez", 3], ["Lou Trivino", 3], ["David Bednar", 3], ["Hyun Jin Ryu", 2], ["Taylor Rogers", 2], ["Logan Gilbert", 2], ["Camilo Doval", 2], ["Noah Syndergaard", 2], ["Andrew Kittredge", 2], ["Craig Kimbrel", 2], ["Garrett Whitlock", 2], ["Jose Urquidy", 2], ["Marcus Stroman", 2], ["Aaron Civale", 2], ["Tarik Skubal", 2], ["John Means", 2], ["Dylan Floro", 2], ["Michael Fulmer", 2], ["Anthony DeSclafani", 2], ["Corey Kluber", 2], ["Chris Flexen", 2], ["Joe Ryan", 2], ["Paul Sewald", 2], ["Patrick Sandoval", 2], ["Devin Williams", 2], ["Alex Colome", 2], ["Cole Sulser", 2], ["Kyle Hendricks", 2], ["Triston McKenzie", 2], ["German Marquez", 2], ["Zach Plesac", 2], ["Stephen Strasburg", 2], ["Matt Barnes", 2], ["Marco Gonzales", 2], ["Lucas Sims", 2], ["Alex Wood", 1], ["Casey Mize", 1], ["Jordan Montgomery", 1], ["Steven Matz", 1], ["Gregory Soto", 1], ["Jon Gray", 1], ["Cristian Javier", 1], ["Alex Reyes", 1], ["Diego Castillo", 1], ["Luis Patino", 1], ["Anthony Bender", 1], ["Tanner Houck", 1], ["Yusei Kikuchi", 1], ["Chris Paddack", 1], ["Taijuan Walker", 1], ["Bailey Ober", 1], ["Nestor Cortes", 1], ["Nick Pivetta", 1], ["James Karinchak", 1], ["Rowan Wick", 1], ["Jonathan Loaisiga", 1], ["Nate Pearson", 1], ["Zack Greinke", 1], ["Huascar Ynoa", 1], ["Alex Cobb", 1], ["Carlos Carrasco", 1], ["Tony Gonsolin", 1], ["Cal Quantrill", 1], ["Aaron Ashby", 1], ["Chad Green", 1], ["James Kaprielian", 1], ["Drew Rasmussen", 1], ["Hector Neris", 1], ["Jameson Taillon", 1], ["Brady Singer", 1], ["Sixto Sanchez", 1], ["Dinelson Lamet", 1], ["Josiah Gray", 1], ["Kyle Gibson", 1], ["Eric Lauer", 1], ["Collin McHugh", 1], ["Jesus Luzardo", 1], ["Madison Bumgarner", 1], ["Zach Eflin", 1], ["Dane Dunning", 1], ["Pete Fairbanks", 1], ["Dustin May", 1], ["Adbert Alzolay", 1], ["Andrew Heaney", 1], ["Elieser Hernandez", 1], ["Brad Hand", 1], ["Roansy Contreras", 1], ["MacKenzie Gore", 1], ["Edward Cabrera", 1], ["Tylor Megill", 1], ["Domingo German", 1], ["Nick Lodolo", 1], ["JT Brubaker", 1], ["Michael Pineda", 1], ["Tanner Rainey", 1], ["Jake Odorizzi", 1]]

        fpros_h = []
        fpros_p = []
        lineups = []
        plist = []
        avail_list = []
        season_stats_h = []
        last15_stats_h = []
        last7_stats_h = []
        season_stats_p = []
        last15_stats_p = []
        last7_stats_p = []

        fpros_h = get_fpros_h_data()
        fpros_p = get_fpros_p_data()
        lineups = get_rosterresource()
        plist = get_pitcherlist_data()
        rplist = get_pitcherlist_rp()
        availdf = get_available_players()
        hranks, pranks = get_fpros_ranks()
        [season_stats_h, last7_stats_h, last15_stats_h, season_stats_p, last7_stats_p, last15_stats_p] = get_season_stats()

        f = open('store.pckl', 'wb')
        pickle.dump([prices_h, prices_p, fpros_h, fpros_p, lineups, plist, rplist, availdf, hranks, pranks], f)
        f.close()

    availdf['Rank'] = np.ones(availdf.shape[0]).astype(np.uint)*1000
    availdf['Pitcherlist SP'] = np.ones(availdf.shape[0]).astype(np.uint)*1000
    availdf['Pitcherlist RP'] = np.ones(availdf.shape[0]).astype(np.uint)*1000
    availdf.loc[availdf['Pos']=='H', 'Rank'] = availdf.loc[availdf['Pos']=='H'].apply(lambda row: getrank(row[0], hranks), axis=1)
    availdf.loc[availdf['Pos']=='P', 'Rank'] = availdf.loc[availdf['Pos']=='P'].apply(lambda row: getrank(row[0], pranks), axis=1)
    availdf.loc[availdf['Pos']=='P', 'Pitcherlist SP'] = availdf.loc[availdf['Pos']=='P'].apply(lambda row: getrank(row[0], plist), axis=1)
    availdf.loc[availdf['Pos']=='P', 'Pitcherlist RP'] = availdf.loc[availdf['Pos']=='P'].apply(lambda row: getrank(row[0], rplist), axis=1)
    # print(availdf.to_string())

    workbook = xlsxwriter.Workbook('importeddata.xlsx')

    espn_prices_h_ws = workbook.add_worksheet('ESPN_PRICES_H')
    espn_prices_h_ws.set_column(0, 0, 25)
    write_array(espn_prices_h_ws, prices_h, 'prices')

    espn_prices_p_ws = workbook.add_worksheet('ESPN_PRICES_P')
    espn_prices_p_ws.set_column(0, 0, 25)
    write_array(espn_prices_p_ws, prices_p, 'prices')

    # espn_p_ws = workbook.add_worksheet('ESPN_P')
    # espn_p_ws.set_column(0, 0, 25)
    # write_array(espn_p_ws, espnp, 'pitcher')

    # espn_h_ws = workbook.add_worksheet('ESPN_H')
    # espn_h_ws.set_column(0, 0, 25)
    # write_array(espn_h_ws, espnh, 'hitter')

    fpros_h_ws = workbook.add_worksheet('FPROS_H')
    fpros_h_ws.set_column(0, 0, 25)
    # fpros_h_newnames = changenames(espnh, fpros_h)
    # write_array(fpros_h_ws, fpros_h, 'hitter')
    write_array(fpros_h_ws, fpros_h, 'hitter')

    fpros_p_ws = workbook.add_worksheet('FPROS_P')
    fpros_p_ws.set_column(0, 0, 25)
    # fpros_p_newnames = changenames(espnp, fpros_p)
    # write_array(fpros_p_ws, fpros_p, 'pitcher')
    write_array(fpros_p_ws, fpros_p, 'pitcher')

    plist_ws = workbook.add_worksheet('PitcherList')
    plist_ws.set_column(0, 0, 25)
    #plist_newnames = changenames(fpros_p, plist)
    write_array(plist_ws, plist, 'plist')

    lineupspot_ws = workbook.add_worksheet('Lineups')
    lineupspot_ws.set_column(0, 0, 25)
    # lineups_newnames = changenames(espnh, lineups)
    write_array(lineupspot_ws, lineups, 'lineup')

    avail_ws = workbook.add_worksheet('Available')
    avail_ws.set_column(0, 0, 25)
    write_array(avail_ws, availdf.values.tolist(), availdf.columns.tolist())

    season_h_ws = workbook.add_worksheet('Season_H')
    season_h_ws.set_column(0, 0, 25)
    write_array(season_h_ws, season_stats_h.values.tolist(), season_stats_h.columns.tolist())

    last7_h_ws = workbook.add_worksheet('Last_7_H')
    last7_h_ws.set_column(0, 0, 25)
    write_array(last7_h_ws, last7_stats_h.values.tolist(), last7_stats_h.columns.tolist())

    last15_h_ws = workbook.add_worksheet('Last_15_H')
    last15_h_ws.set_column(0, 0, 25)
    write_array(last15_h_ws, last15_stats_h.values.tolist(), last15_stats_h.columns.tolist())

    season_p_ws = workbook.add_worksheet('Season_P')
    season_p_ws.set_column(0, 0, 25)
    write_array(season_p_ws, season_stats_p.values.tolist(), season_stats_p.columns.tolist())

    last7_p_ws = workbook.add_worksheet('Last_7_P')
    last7_p_ws.set_column(0, 0, 25)
    write_array(last7_p_ws, last7_stats_p.values.tolist(), last7_stats_p.columns.tolist())

    last15_p_ws = workbook.add_worksheet('Last_15_P')
    last15_p_ws.set_column(0, 0, 25)
    write_array(last15_p_ws, last15_stats_p.values.tolist(), last15_stats_p.columns.tolist())


    workbook.close()

    return [prices_h, prices_p, fpros_h, fpros_p, lineups, plist, rplist, availdf, hranks, pranks]


def get_season_stats():
    #run it once to get the lookup table
    # playerid_lookup('pujols', 'albert')

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    todaym7 = today - timedelta(days=7)
    todaym15 = today - timedelta(days=15)

    d_OD = "2022-04-07" #  beginning of season
    dtoday = today.strftime("%Y-%m-%d")
    dyest = yesterday.strftime("%Y-%m-%d")
    d7 = todaym7.strftime("%Y-%m-%d")
    d15 = todaym15.strftime("%Y-%m-%d")



    # EDIT BATTING_STATS_RANGE FUNCTION
    # in get_soup function
    # The page wasn't loading fully and was getting an incomplete list
    #s = requests.get(url, timeout=(10, 3)).content

    #Get stats through yesterday
    #might be an issue with the pybaseball code if games are running today?
    season_stats_h = batting_stats_range(d_OD, dtoday)
    last7_stats_h = batting_stats_range(max(d7, d_OD), dtoday)
    last15_stats_h = batting_stats_range(max(d15, d_OD), dtoday)

    season_stats_p = pitching_stats_range(d_OD, dtoday)
    last7_stats_p = pitching_stats_range(max(d7, d_OD), dtoday)
    last15_stats_p = pitching_stats_range(max(d15, d_OD), dtoday)

    return [season_stats_h, last7_stats_h, last15_stats_h, season_stats_p, last7_stats_p, last15_stats_p]

    pass


def get_fpros_ranks():
    print("Loading FantasyPros ROS rankings")

    page = requests.get("https://www.fantasypros.com/mlb/rankings/ros-hitters.php")
    soup = BeautifulSoup(page.content, 'html.parser')

    alldata = soup.find_all('a', {"class": 'player-name'})

    hnames = []
    for nm in alldata:
        hnames.append(unidecode(nm.text))

    page = requests.get("https://www.fantasypros.com/mlb/rankings/ros-pitchers.php")
    soup = BeautifulSoup(page.content, 'html.parser')

    alldata = soup.find_all('a', {"class": 'player-name'})

    pnames = []
    for nm in alldata:
        pnames.append(unidecode(nm.text))

    return hnames, pnames

def get_fpros_h_data():
    print("Loading FantasyPros hitters")
    #page = requests.get("https://www.fantasypros.com/mlb/projections/hitters.php", proxies=proxyDict)
    page = requests.get("https://www.fantasypros.com/mlb/projections/hitters.php")
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get list of list of all players
    alldata = soup.find_all('tr', {"class": lambda L: L and L.startswith('mpb-player')})

    print("Getting FantasyPros hitter stats")

    numplayers = len(alldata)
    allstats = [[]] * numplayers

    for i in range(numplayers):
        pd = [a.text for a in alldata[i].find_all('td')]

        result = pd[0][pd[0].find('(') + 1:pd[0].find(')')]
        positions = result.split(' - ')[-1].split(',')

        for x in range(len(positions)):
            if positions[x] == "LF":
                positions[x] = "OF"
            if positions[x] == "RF":
                positions[x] = "OF"
            if positions[x] == "CF":
                positions[x] = "OF"

        positions = list(dict.fromkeys(positions))

        pos1 = '-'
        pos2 = '-'
        pos3 = '-'
        if len(positions) > 0:
            pos1 = positions[0]
        if len(positions) > 1:
            pos2 = positions[1]
        if len(positions) > 2:
            pos3 = positions[2]

        nt = alldata[i].find_all('a')
        name = nt[0].get_text()
        team = nt[1].get_text()
        if team == '':
            team = 'FA'
        log([name, team])
        allstats[i] = [name, team, pos1, pos2, pos3, int(pd[8]), int(pd[1]), int(pd[2]), int(pd[3]), int(pd[4]), int(pd[5]),
                       float(pd[6]), float(pd[7]), float(pd[13]), float(pd[14]), int(pd[11]), int(pd[12])]

    return allstats


def get_fpros_p_data():
    print("Loading FantasyPros pitchers")


    #projhtml = 'C:\\Users\\ffxr3b\\Desktop\\temp\\fpSP.html'
    #soup = BeautifulSoup(open(projhtml), "html.parser")
    #sppage = requests.get("https://www.fantasypros.com/mlb/projections/sp.php", proxies=proxyDict)
    sppage = requests.get("https://www.fantasypros.com/mlb/projections/sp.php")
    soup = BeautifulSoup(sppage.content, 'html.parser')

    # Get list of list of all players
    alldata = soup.find_all('tr', {"class": lambda L: L and L.startswith('mpb-player')})

    print("Getting FantasyPros SP stats")

    ignore = ['Shohei Ohtani']
    numplayers = len(alldata)
    allstats = []
    spnames = []
    for i in range(numplayers):
        pd = [a.text for a in alldata[i].find_all('td')]

        nt = alldata[i].find_all('a')
        name = nt[0].get_text()
        team = nt[1].get_text()
        # print(pd)

        if name not in ignore:
            # print(name)
            allstats.append([name, team, 'SP', '-', int(pd[11]), int(pd[12]), float(pd[1]), int(pd[2]),
                             int(pd[13]), 0, 0, 0, float(pd[5]), float(pd[6]), int(pd[3]),
                             int(pd[9]), float(pd[2]) / float(pd[1]) * 9])
            spnames.append(name)





    #projhtml = 'C:\\Users\\ffxr3b\\Desktop\\temp\\fpRP.html'
    #soup = BeautifulSoup(open(projhtml), "html.parser")
    #rppage = requests.get("https://www.fantasypros.com/mlb/projections/rp.php", proxies=proxyDict)
    rppage = requests.get("https://www.fantasypros.com/mlb/projections/rp.php")
    soup = BeautifulSoup(rppage.content, 'html.parser')


    # Get list of list of all players
    alldata = soup.find_all('tr', {"class": lambda L: L and L.startswith('mpb-player')})

    print("Getting FantasyPros RP stats")

    numplayers = len(alldata)

    for i in range(numplayers):
        pd = [a.text for a in alldata[i].find_all('td')]

        nt = alldata[i].find_all('a')
        name = nt[0].get_text()
        team = nt[1].get_text()

        if name not in ignore + spnames:
            allstats.append([name, team, 'RP', '-', int(pd[12]), 0, float(pd[1]), int(pd[2]),
                             0, int(pd[3]), int(pd[5]), int(pd[3]) + int(pd[5]), float(pd[6]), float(pd[7]), int(pd[13]),
                             int(pd[10]), float(pd[2]) / float(pd[1]) * 9])

    return allstats

def get_pitcherlist_rp():

    print("Loading Pitcherlist Saves+Holds")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    rplist = []

    # url = "https://www.pitcherlist.com/top-100-relievers-for-savehold-leagues-" + dtrystring
    url = "https://www.pitcherlist.com/category/fantasy/svs-hlds/"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    holddiv = soup.find('div', attrs={'class':'hold-me'})
    latest_url = holddiv.find('a').get('href')
    print(latest_url)

    page = requests.get(latest_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    for nm in soup.find_all('td', attrs={'class': 'name'}):
        rplist.append(unidecode(nm.find('a').text))

    return rplist


def get_pitcherlist_data():
    print("Loading Pitcherlist")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    #page = requests.get("https://www.pitcherlist.com/category/articles/the-list/", proxies=proxyDict, headers=headers)
    #page = requests.get("https://www.pitcherlist.com/category/articles/the-list/", headers=headers)

    page = requests.get("https://www.pitcherlist.com/", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    latest_list = soup.find('div', class_='list-latest')
    latest_url = latest_list.find('a').get('href')
    print(latest_url)


    page = requests.get(latest_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    plist_table = soup.find('table', class_="list")
    # names = [[]]
    names = []
    for counter, name in enumerate(plist_table.find_all('td', class_="name")):
        # if counter % 2 != 0:
        # nm = name.find("a").get_text()
        nm = unidecode(name.find("a").text)

        # names.append([nm, counter+1])
        names.append(nm)

    return names


def get_available_players():
    print("Getting available players")
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir=C:\\Users\\Kyle\\AppData\\Local\\Google\\Chrome\\User Data\\Default")  # Path to your chrome profile
    # "user-data-dir=C:\\Users\\ffxr3b\\AppData\\Local\\Google\\Chrome\\User Data\\Default")  # Path to your chrome profile
    browser = webdriver.Chrome(chrome_options=options)

    # browser.get('https://login.yahoo.com')
    # wait = WebDriverWait(browser, 10)
    #
    # emailelem = wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
    # emailelem.send_keys('tuminator@yahoo.com')
    #
    # wait.until(EC.presence_of_element_located((By.ID, 'login-signin')))
    # emailelem.submit()
    #
    # wait.until(EC.element_to_be_clickable((By.ID, 'login-signin')))
    # passwordelem = wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
    # passwordelem.send_keys('yUC$Bengr12o')
    # passwordelem.send_keys(Keys.RETURN)
    #
    # sleep(2)
    availplayers = []

    preurls = [
        "https://baseball.fantasysports.yahoo.com/b1/19282/players?status=A&pos=B&cut_type=33&stat1=S_S_2022&myteam=0&sort=R_PO&sdir=1&count=",
        "https://baseball.fantasysports.yahoo.com/b1/19282/players?status=A&pos=P&cut_type=33&stat1=S_S_2022&myteam=0&sort=R_PO&sdir=1&count=",
    ]

    avail_pos = [
        'H',
        'P'
    ]

    for j in range(2):
        for i in range(7):

            # urlpre = "https://baseball.fantasysports.yahoo.com/b1/19282/players?status=A&pos=B&cut_type=33&stat1=S_S_2022&myteam=0&sort=R_PO&sdir=1&count="
            urlpost = str(i*25)
            url = preurls[j]+urlpost
            # print(url)
            browser.get(url)

            if j==0 and i==0:
                sleep(15)

            innerHTML = browser.execute_script("return document.body.innerHTML")  # returns the inner HTML as a string
            soup = BeautifulSoup(innerHTML, 'html.parser')

            tbl = soup.find('div', class_='players')
            alldata = tbl.find_all('div', {"class": lambda L: L and L.startswith('ysf-player-name')})
            for row in alldata:
                rname = unidecode(row.find('a').text)
                # print(rname)
                availplayers.append([rname, avail_pos[j]])

    availdf = pd.DataFrame(availplayers, columns=['Name', 'Pos'])
    # print(availdf)
    return availdf

def get_rosterresource():
    #page = requests.get("https://www.rosterresource.com/mlb-roster-grid/#projected-order", proxies=proxyDict)

    all_lineups = []
    for num in range(1, 31):
        # page = requests.get(rr_page)
        # soup = BeautifulSoup(page.content, 'html.parser')

        # urlreq = 'https://cdn.fangraphs.com/api/roster-resource/lineup-tracker/data?teamid=21'
        # get response
        rr_page = "https://cdn.fangraphs.com/api/depth-charts/roster?teamid=" + str(num)
        response = urllib.request.urlopen(rr_page, timeout=10)
        # load as json
        jresponse = json.load(response)
        # write to file as pretty print
        # with open('asdaresp.json', 'w') as outfile:
        #     json.dump(jresponse, outfile, sort_keys=True, indent=4)
        print("Getting rosters from team: " + str(num))
        for i in range(len(jresponse)):
            #print(jresponse[0]['depthChartsData'][i]['playerName'], i)
            rr_pname = jresponse[i]['player']

            try:
                rr_role = int(jresponse[i]['role'])
            except:
                rr_role = 10

            if rr_role <= 9:
                all_lineups.append([rr_pname, i+1])

    print(all_lineups)


        # print(soup)
        # table = soup.find("div", attrs={'class': "fg-data-grid rr-depth-chart-roster-table mlb-sl sort-disabled  "})
        # print(table)


        # id = lambda x: x and x.startswith('post-')

        # for player in soup.find_all('playerName'):
        #     print(player)
            # players = []
            # for counter, player in enumerate(team.find_all('strong')):
            #     temp = player.get_text(strip=True)
            #     temp2 = unicodedata.normalize('NFKD', temp).encode('ASCII', 'ignore').decode('ASCII')
            #     temp3 = temp2.replace('*', '')
            #     all_lineups.append([temp3, counter + 1])

    return (all_lineups)


def add_hitter_to_pd(name, player, pdata):
    # espnh = pdata[0]
    espnprices = pdata[0]
    fprosh = pdata[2]
    lineups = pdata[4]

    # espnh_ind = find_in_2d_array(espnh, name)
    espnprices_ind = find_in_2d_array(espnprices, name)
    fprosh_ind = find_in_2d_array(fprosh, name)
    lineups_ind = find_in_2d_array(lineups, name)



    if(player.empty):
        watch = False
        passon = False
        keeper = False
        keeperprice = 0
    else:
        watch = player.watch.values[0]
        passon = player.passon.values[0]
        keeper = player.keeper.values[0]
        keeperprice = player.keeper_price.values[0]

    if espnprices_ind == -1:
        eprice = 1
        log("Not found in ESPN Prices")
    else:
        eprice = espnprices[espnprices_ind][1]

    if lineups_ind == -1:
        log("Not found in lineup")
        lup = 0
    else:
        lup = lineups[lineups_ind][1]

    # if espnh_ind == -1:
    #     log("Not Found in ESPN stats")
    #     espnh = fprosh
    #     espnh_ind = fprosh_ind

    # if name == 'Shohei Ohtani':
    #     espnh[espnh_ind][2:5] = ['DH', '-', '-']

    # if espnh[espnh_ind][2] == '-':
    #     espnh[espnh_ind][2] = 'DH'

    pd_data = [
        name,  # name
        fprosh[fprosh_ind][1],  # team
        False,  # drafted
        fprosh[fprosh_ind][5],  # h_h_fpros
        fprosh[fprosh_ind][6],  # h_ab_fpros
        fprosh[fprosh_ind][7],  # h_runs_fpros
        fprosh[fprosh_ind][8],  # h_hr_fpros
        fprosh[fprosh_ind][9],  # h_rbi_fpros
        fprosh[fprosh_ind][10],  # h_sb_fpros
        fprosh[fprosh_ind][11],  # h_avg_fpros
        fprosh[fprosh_ind][12],  # h_obp_fpros
        fprosh[fprosh_ind][13],  # h_slg_fpros
        fprosh[fprosh_ind][14],  # h_ops_fpros
        fprosh[fprosh_ind][15],  # h_bb_fpros
        fprosh[fprosh_ind][16],  # h_so_fpros
        # espnh[espnh_ind][5],  # h_h_espn
        # espnh[espnh_ind][6],  # h_ab_espn
        # espnh[espnh_ind][7],  # h_runs_espn
        # espnh[espnh_ind][8],  # h_hr_espn
        # espnh[espnh_ind][9],  # h_rbi_espn
        # espnh[espnh_ind][10],  # h_sb_espn
        # espnh[espnh_ind][11],  # h_avg_espn
        # espnh[espnh_ind][12],  # h_obp_espn
        # espnh[espnh_ind][13],  # h_slg_espn
        # espnh[espnh_ind][14],  # h_ops_f
        # espnh[espnh_ind][15],  # h_bb_espn
        # espnh[espnh_ind][16],  # h_so_espn
        0,  # p_g_fpros
        0,  # p_gs_fpros
        0,  # p_ip_fpros
        0,  # p_k_fpros
        0,  # p_qs_fpros
        0,  # p_sv_fpros
        0,  # p_hd_fpros
        0,  # p_svhd_fpros
        0,  # p_era_fpros
        0,  # p_whip_fpros
        0,  # p_w_fpros
        0,  # p_bb_fpros
        0,  # p_kp9_fpros
        # 0,  # p_g_espn
        # 0,  # p_gs_espn
        # 0,  # p_ip_espn
        # 0,  # p_k_espn
        # 0,  # p_qs_espn
        # 0,  # p_sv_espn
        # 0,  # p_hd_espn
        # 0,  # p_svhd_espn
        # 0,  # p_era_espn
        # 0,  # p_whip_espn
        # 0,  # p_w_espn
        # 0,  # p_bb_espn
        # 0,  # p_kp9_espn
        True,  # hitter
        False,  # pitcher
        fprosh[fprosh_ind][2],  # pos1
        fprosh[fprosh_ind][3],  # pos2
        fprosh[fprosh_ind][4],  # pos3
        'C' in fprosh[fprosh_ind][2:5],  # posC
        '1B' in fprosh[fprosh_ind][2:5],  # pos1B
        '2B' in fprosh[fprosh_ind][2:5],  # pos2B
        '3B' in fprosh[fprosh_ind][2:5],  # pos3B
        'SS' in fprosh[fprosh_ind][2:5],  # posSS
        'OF' in fprosh[fprosh_ind][2:5],  # posOF
        False,  # posSP
        False,  # posRP
        0,  # orank
        0,  # prank
        fprosh_ind,  # hitrank
        0,  # pitchrank
        # prev_h[min(fprosh_ind, len(prev_h)-1)],  # tier
        0,  # tier
        float(0),  # par
        eprice,  # espn_price
        0,  # my_price
        watch,  # watch
        passon, #pass
        lup,  # lineup
        0,  # plistrank
        keeper,  # keeper
        keeperprice,  # keeper_price
        float(0),  # Rpoints
        float(0),  # HRpoints
        float(0),  # RBIpoints
        float(0),  # SBpoints
        float(0),  # OBPpoints
        float(0),  # Kpoints
        float(0),  # QSpoints
        float(0),  # SVHDpoints
        float(0),  # ERApoints
        float(0),  # WHIPpoints

    ]


    return pd_data


def add_pitcher_to_pd(name, player, pdata):
    # espnp = pdata[1]
    espnprices = pdata[1]
    fprosp = pdata[3]
    pitcherlist = pdata[5]

    # espnp_ind = find_in_2d_array(espnp, name)
    espnprices_ind = find_in_2d_array(espnprices, name)
    fprosp_ind = find_in_2d_array(fprosp, name)
    # pitcherlist_ind = find_in_2d_array(pitcherlist, name)
    try:
        # pitcherlist_ind = pitcherlist.index(name)
        # pl = pitcherlist[pitcherlist_ind][1] + 1
        pl = pitcherlist.index(name)
    except:
        pl = 101

    prev_sp = [41.00, 35.00, 29.50, 28.50, 27.00, 26.33, 25.33, 24.67, 23.50, 22.50, 21.17, 20.67, 19.83, 18.17, 17.17,
              16.33, 15.67, 15.50, 15.17, 14.67, 14.33, 13.67, 13.00, 12.17, 11.83, 11.50, 11.00, 10.50, 9.83, 9.50,
              9.33, 8.83, 8.67, 8.17, 7.83, 7.50, 7.33, 7.00, 6.67, 6.50, 6.33, 6.00, 6.00, 5.67, 5.17, 4.50, 4.33,
              4.33, 4.00, 3.50, 3.00, 3.00, 2.83, 2.67, 2.67, 2.50, 2.00, 1.83, 1.67, 1.50, 1.50, 1.50, 1.50, 1.50,
              1.17, 1.17, 1.17, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]

    if(player.empty):
        watch = False
        passon = False
        keeper = False
        keeperprice = 0
    else:
        watch = player.watch.values[0]
        passon = player.passon.values[0]
        keeper = player.keeper.values[0]
        keeperprice = player.keeper_price.values[0]


    if espnprices_ind == -1:
        eprice = 1
        log("Not Found in ESPN Prices")
    else:
        eprice = espnprices[espnprices_ind][1]

    # if espnp_ind == -1:
    #     log("Not Found in ESPN stats")
    #     espnp = fprosp
    #     espnp_ind = fprosp_ind

    pd_data = [
        name,  # name
        fprosp[fprosp_ind][1],  # team
        False,  # drafted
        0,  # h_h_fpros
        0,  # h_ab_fpros
        0,  # h_runs_fpros
        0,  # h_hr_fpros
        0,  # h_rbi_fpros
        0,  # h_sb_fpros
        0,  # h_avg_fpros
        0,  # h_obp_fpros
        0,  # h_slg_fpros
        0,  # h_ops_fpros
        0,  # h_bb_fpros
        0,  # h_so_fpros
        # 0,  # h_h_espn
        # 0,  # h_ab_espn
        # 0,  # h_runs_espn
        # 0,  # h_hr_espn
        # 0,  # h_rbi_espn
        # 0,  # h_sb_espn
        # 0,  # h_avg_espn
        # 0,  # h_obp_espn
        # 0,  # h_slg_espn
        # 0,  # h_ops_f
        # # 0,  # h_bb_espn
        # 0,  # h_so_espn
        fprosp[fprosp_ind][4],  # p_g_fpros
        fprosp[fprosp_ind][5],  # p_gs_fpros
        fprosp[fprosp_ind][6],  # p_ip_fpros
        fprosp[fprosp_ind][7],  # p_k_fpros
        fprosp[fprosp_ind][8],  # p_qs_fpros
        fprosp[fprosp_ind][9],  # p_sv_fpros
        fprosp[fprosp_ind][10],  # p_hd_fpros
        fprosp[fprosp_ind][11],  # p_svhd_fpros
        fprosp[fprosp_ind][12],  # p_era_fpros
        fprosp[fprosp_ind][13],  # p_whip_fpros
        fprosp[fprosp_ind][14],  # p_w_fpros
        fprosp[fprosp_ind][15],  # p_bb_fpros
        fprosp[fprosp_ind][16],  # p_kp9_fpros
        # espnp[espnp_ind][4],  # p_g_espn
        # espnp[espnp_ind][5],  # p_gs_espn
        # espnp[espnp_ind][6],  # p_ip_espn
        # espnp[espnp_ind][7],  # p_k_espn
        # espnp[espnp_ind][8],  # p_qs_espn
        # espnp[espnp_ind][9],  # p_sv_espn
        # espnp[espnp_ind][10],  # p_hd_espn
        # espnp[espnp_ind][11],  # p_svhd_espn
        # espnp[espnp_ind][12],  # p_era_espn
        # espnp[espnp_ind][13],  # p_whip_espn
        # espnp[espnp_ind][14],  # p_w_espn
        # espnp[espnp_ind][15],  # p_bb_espn
        # espnp[espnp_ind][16],  # p_kp9_espn
        False,  # hitter
        True,  # pitcher
        fprosp[fprosp_ind][2],  # pos1
        '-',  # pos2
        '-',  # pos3
        False,  # posC
        False,  # pos1B
        False,  # pos2B
        False,  # pos3B
        False,  # posSS
        False,  # posOF
        'SP' in fprosp[fprosp_ind][2],  # posSP
        'RP' in fprosp[fprosp_ind][2],  # posRP
        0,  # orank
        0,  # prank
        0,  # hitrank
        fprosp_ind,  # pitchrank
        0,  # tier
        float(0),  # par
        eprice,  # espn_price
        0,  # my_price
        watch,  # watch
        passon, #passon
        0,  # lineup
        pl,  # plistrank
        keeper,  # keeper
        keeperprice,  # keeper_price
        float(0),  # Rpoints
        float(0),  # HRpoints
        float(0),  # RBIpoints
        float(0),  # SBpoints
        float(0),  # OBPpoints
        float(0),  # Kpoints
        float(0),  # QSpoints
        float(0),  # SVHDpoints
        float(0),  # ERApoints
        float(0),  # WHIPpoints
    ]

    return pd_data


def avg_by_pos(hdf, pdf):
    pd_header = ['AB', 'R', 'HR', 'RBI', 'SB', 'OBP', 'IP', 'K', 'QS', 'SVHD', 'ERA', 'WHIP']
    pd_index = ['C', '1B', '2B', 'SS', '3B', 'OF', 'OF2', 'OF3', 'OF4', 'OF5',
                'MI', 'CI', 'DH', 'SP', 'SP2', 'SP3', 'SP4', 'SP5', 'RP', 'RP2', 'RP3', 'TARGET']
    avgstatsdf = pd.DataFrame(columns=pd_header, index=pd_index)


    tdf = [
        hdf.head(200).loc[hdf['posC'] == True],
        hdf.head(200).loc[hdf['pos1B'] == True],
        hdf.head(200).loc[hdf['pos2B'] == True],
        hdf.head(200).loc[hdf['posSS'] == True],
        hdf.head(200).loc[hdf['pos3B'] == True],
        hdf.head(200).loc[hdf['posOF'] == True],
        hdf.head(200).loc[hdf['posOF'] == True],
        hdf.head(200).loc[hdf['posOF'] == True],
        hdf.head(200).loc[hdf['posOF'] == True],
        hdf.head(200).loc[hdf['posOF'] == True],
        hdf.head(200).loc[(hdf['pos2B'] == True) | (hdf['posSS'] == True)],
        hdf.head(200).loc[(hdf['pos1B'] == True) | (hdf['pos3B'] == True)],
        hdf.head(200).loc[hdf['hitter'] == True],
        pdf.head(100).loc[pdf['pos1'] == 'SP'],
        pdf.head(100).loc[pdf['pos1'] == 'SP'],
        pdf.head(100).loc[pdf['pos1'] == 'SP'],
        pdf.head(100).loc[pdf['pos1'] == 'SP'],
        pdf.head(100).loc[pdf['pos1'] == 'SP'],
        # pdf.head(100).loc[pdf['pos1'] == 'SP'],
        pdf.loc[pdf['pos1'] == 'RP'].head(36),
        pdf.loc[pdf['pos1'] == 'RP'].head(36),
        pdf.loc[pdf['pos1'] == 'RP'].head(36),
    ]

    # nums = [12, 18, 18, 18, 18, 72, 72, 72, 72, 72, 36, 36, 156, 72, 72, 72, 72, 72, 72, 24, 24, 24]
    nums = [12, 18, 18, 18, 18, 72, 72, 72, 72, 72, 36, 36, 156, 48, 48, 48, 48, 48, 24, 24, 24]
    for cntr, i in enumerate(tdf):
        num = nums[cntr]
        log(i.shape)
        stats = [round(i.h_ab_fpros.nlargest(num).median(), 2),
                 round(i.h_runs_fpros.nlargest(num).median(), 2),
                 round(i.h_hr_fpros.nlargest(num).median(), 2),
                 round(i.h_rbi_fpros.nlargest(num).median(), 2),
                 round(i.h_sb_fpros.nlargest(int(num/2)).median(), 2),  #make steals less valuable
                 # round(i.h_sb_fpros.nlargest(int(num/2)).median(), 2),  #make steals less valuable
                 round(i.h_obp_fpros.nlargest(num).median(), 3),
                 round(i.p_ip_fpros.nlargest(num).median(), 2),
                 round(i.p_k_fpros.nlargest(num).median(), 2),
                 round(i.p_qs_fpros.nlargest(num).median(), 2),
                 round(i.p_svhd_fpros.nlargest(num).median(), 2),
                 round(i.p_era_fpros.nsmallest(num).median(), 2),
                 round(i.p_whip_fpros.nsmallest(num).median(), 2),

                 ]
        avgstatsdf.loc[pd_index[cntr]] = stats

    for i in pd_header:
        avgstatsdf.loc['TARGET'][i] = avgstatsdf.iloc[0:21][i].sum()
        avgstatsdf.loc['TARGET'][i] = avgstatsdf.iloc[0:21][i].sum()

    avgstatsdf.loc['TARGET']['OBP'] = round(np.average(avgstatsdf.iloc[0:13]['OBP'], weights=avgstatsdf.iloc[0:13]['AB']), 3)
    avgstatsdf.loc['TARGET']['ERA'] = round(np.average(avgstatsdf.iloc[13:21]['ERA'], weights=avgstatsdf.iloc[13:21]['IP']), 3)
    avgstatsdf.loc['TARGET']['WHIP'] = round(np.average(avgstatsdf.iloc[13:21]['WHIP'], weights=avgstatsdf.iloc[13:21]['IP']), 3)

    # spread/2 = plus/minus spread between worst and first in 2021
    spread = np.asarray([.20, .20, .20, .25, .60, .10, .30, .30, .30, .40, -.40, -.14])

    for i in range(10, 121, 1):
        avgstatsdf.loc[i/10] = (1 - (spread / 2) + spread * (i/10 - 1) / 11) * avgstatsdf.loc['TARGET'].tolist()

    avgstatsdf.loc[1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1.5]
    avgstatsdf.loc[12] = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 0, 0]

    return avgstatsdf


def df_from_sources(pdata):
    # pdata = [prices_h, prices_p, fpros_h, fpros_p, lineups, plist, rplist, availdf, hranks, pranks]
    pd_header = [
        'name', 'team', 'drafted', 'h_h_fpros', 'h_ab_fpros', 'h_runs_fpros',
        'h_hr_fpros', 'h_rbi_fpros', 'h_sb_fpros', 'h_avg_fpros', 'h_obp_fpros', 'h_slg_fpros',
        'h_ops_fpros', 'h_bb_fpros', 'h_so_fpros',
        # 'h_h_espn', 'h_ab_espn', 'h_runs_espn', 'h_hr_espn', 'h_rbi_espn', 'h_sb_espn', 'h_avg_espn', 'h_obp_espn',
        # 'h_slg_espn', 'h_ops_f', 'h_bb_espn', 'h_so_espn',
        'p_g_fpros', 'p_gs_fpros', 'p_ip_fpros', 'p_k_fpros', 'p_qs_fpros',
        'p_sv_fpros', 'p_hd_fpros', 'p_svhd_fpros', 'p_era_fpros', 'p_whip_fpros', 'p_w_fpros', 'p_bb_fpros',
        'p_kp9_fpros',
        # 'p_g_espn', 'p_gs_espn', 'p_ip_espn', 'p_k_espn',  'p_qs_espn', 'p_sv_espn', 'p_hd_espn',
        # 'p_svhd_espn', 'p_era_espn', 'p_whip_espn', 'p_w_espn', 'p_bb_espn', 'p_kp9_espn',
        'hitter',
        'pitcher', 'pos1', 'pos2', 'pos3', 'posC', 'pos1B',
        'pos2B', 'pos3B', 'posSS', 'posOF', 'posSP', 'posRP',
        'orank', 'prank', 'hitrank', 'pitchrank', 'tier', 'par',
        'espn_price', 'my_price', 'watch', 'passon', 'lineup', 'plistrank', 'keeper',
        'keeper_price', 'Rpoints', 'HRpoints', 'RBIpoints', 'SBpoints', 'OBPpoints',
        'Kpoints', 'QSpoints', 'SVHDpoints', 'ERApoints', 'WHIPpoints',
    ]

    #hittersdf = pd.DataFrame(columns=pd_header)
    #pitchersdf = pd.DataFrame(columns=pd_header)

    #hittersdf, pitchersdf = load_df_from_excel()

    try:
        df = load_df_from_excel()
    except:
        df = pd.DataFrame(columns=pd_header)

    print("Loading Players")
    allhitters = []
    allpitchers = []
    for i in pdata[2]:
        log('Getting stats for ' + i[0])
        player = df.loc[df['name'] == i[0]]
        allhitters.append(add_hitter_to_pd(i[0], player, pdata))

    for i in pdata[3]:
        log('Getting stats for ' + i[0])
        player = df.loc[df['name'] == i[0]]
        allpitchers.append(add_pitcher_to_pd(i[0], player, pdata))

    sortby = 'espn_price'

    hittersdf = pd.DataFrame(allhitters, columns=pd_header)
    #hittersdf = pd.DataFrame(allhitters, columns=pd_header).sort_values(by=[sortby], ascending=False)
    #hittersdf['hitrank'] = list(range(1, hittersdf.shape[0]+1))

    pitchersdf = pd.DataFrame(allpitchers, columns=pd_header)
    #pitchersdf = pd.DataFrame(allpitchers, columns=pd_header).sort_values(by=[sortby], ascending=False)
    #pitchersdf['pitchrank'] = list(range(1, pitchersdf.shape[0]+1))

    avgstatsdf = avg_by_pos(hittersdf, pitchersdf)
    teamdf = load_teamdf_from_excel()
    slotsdf = load_slots_from_excel()

    df = pd.concat([hittersdf, pitchersdf])
    #df = pd.concat([hittersdf, pitchersdf]).sort_values(by=[sortby, 'orank'], ascending=[False, False])
    df['orank'] = list(range(1, df.shape[0]+1))

    print("Calculating PAR")
    df = calc_par(df, avgstatsdf)
    numhits = df.loc[df['hitter']].shape[0]
    numpits = df.loc[df['pitcher']].shape[0]

    df.loc[df['hitter'], 'hitrank'] = np.linspace(1, numhits, numhits).astype(np.int)
    df.loc[df['pitcher'], 'pitchrank'] = np.linspace(1, numpits, numpits).astype(np.int)

    print("Saving Keepers")
    df = savekeepers(df)

    print("Calculating Prices")
    df = calcprices(df)

    print("Saving to Excel")
    save_to_excel(df, avgstatsdf, teamdf, slotsdf)

    print("Done")
    return df, avgstatsdf, teamdf, slotsdf

def calc_par(df, avgstatsdf):

    start = time.process_time()

    print(time.process_time() - start)
    pointsdf = avgstatsdf.iloc[-111:]
    #print(pointsdf)

    stats_header = avgstatsdf.columns.values.tolist()
    player_header = df.columns.values.tolist()
    par_header = ['Rpoints', 'HRpoints', 'RBIpoints', 'SBpoints', 'OBPpoints',
                  'Kpoints', 'QSpoints', 'SVHDpoints', 'ERApoints', 'WHIPpoints']

    par_column = []
    for j in par_header:
        par_column.append(df.columns.get_loc(j))

    #print(par_column)


    avgstats = np.asarray(avgstatsdf.loc['TARGET'].tolist())
    #print(avgstats)

    print(time.process_time() - start)
    # for i in range(df.shape[0]):
    for i in range(20):
        playerstats = np.asarray(df.iloc[i][['h_ab_fpros', 'h_runs_fpros', 'h_hr_fpros','h_rbi_fpros',
                                  'h_sb_fpros', 'h_obp_fpros', 'p_ip_fpros', 'p_k_fpros',
                                  'p_qs_fpros', 'p_svhd_fpros', 'p_era_fpros', 'p_whip_fpros']].tolist())

        if df.iloc[i]['hitter']:
            posstats = np.asarray(avgstatsdf.loc['DH'].tolist())
        else:
            posstats = np.asarray(avgstatsdf.loc[df.iloc[i]['pos1']].tolist())



        #subtract avg stats, add player stats
        newstats = avgstats - posstats + playerstats

        print(time.process_time() - start)
        #calc k's
        if playerstats[6] !=0:
            newstats[7] = avgstats[7] - (posstats[7] / posstats[6] * playerstats[6]) + playerstats[7]

        print(time.process_time() - start)
        #calc obp
        newstats[5] = (avgstats[0]*avgstats[5] - posstats[0]*posstats[5] + playerstats[0]*playerstats[5]) \
            / (avgstats[0] - posstats[0] + playerstats[0])

        print(time.process_time() - start)
        #calc era
        newstats[10] = ((avgstats[10] * (avgstats[6]-posstats[6]+playerstats[6]) / 9)
                        - (posstats[10] * playerstats[6] / 9)
                        + (playerstats[10] * playerstats[6] / 9)) * 9 \
            / (avgstats[6] - posstats[6] + playerstats[6])

        print(time.process_time() - start)
        #calc whip
        newstats[11] = ((avgstats[11] * (avgstats[6]-posstats[6]+playerstats[6]))
                        - (posstats[11] * playerstats[6])
                        + (playerstats[11] * playerstats[6])) \
            / (avgstats[6] - posstats[6] + playerstats[6])

        print(time.process_time() - start)
        #find Points Above Average
        playerPAR = [(pointsdf.loc[pointsdf['R'] >= newstats[1]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['HR'] >= newstats[2]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['RBI'] >= newstats[3]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['SB'] >= newstats[4]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['OBP'] >= newstats[5]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['K'] >= newstats[7]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['QS'] >= newstats[8]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['SVHD'] >= newstats[9]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['ERA'] <= newstats[10]]).index[0]-6.5,
                    (pointsdf.loc[pointsdf['WHIP'] <= newstats[11]]).index[0]-6.5]

        print(time.process_time() - start)
        for cntr, j in enumerate(par_column):
            df.iat[i,j] = playerPAR[cntr]

        print(time.process_time() - start)
        df.iat[i, df.columns.get_loc('par')] = sum(playerPAR)



    prev_h = np.asarray([53.00, 52.00, 41.00, 41.00, 41.00, 40.00, 39.00, 39.00, 39.00, 36.00, 36.00, 34.00, 33.00, 32.00, 31.00,
                         30.00, 30.00, 29.00, 29.00, 29.00, 28.00, 28.00, 28.00, 28.00, 27.00, 27.00, 26.00, 25.00, 25.00, 25.00,
                         24.00, 24.00, 24.00, 24.00, 24.00, 23.00, 23.00, 23.00, 23.00, 23.00, 23.00, 23.00, 22.00, 22.00, 22.00,
                         21.00, 21.00, 20.00, 19.00, 19.00, 19.00, 19.00, 18.00, 18.00, 18.00, 18.00, 18.00, 18.00, 17.00, 17.00,
                         17.00, 17.00, 17.00, 17.00, 17.00, 17.00, 17.00, 16.00, 16.00, 16.00, 16.00, 16.00, 16.00, 16.00, 16.00,
                         16.00, 16.00, 15.00, 15.00, 15.00, 15.00, 15.00, 15.00, 15.00, 15.00, 14.00, 14.00, 14.00, 14.00, 14.00,
                         14.00, 13.00, 13.00, 13.00, 13.00, 13.00, 13.00, 13.00, 12.00, 12.00, 12.00, 12.00, 12.00, 12.00, 12.00,
                         12.00, 11.00, 11.00, 11.00, 11.00, 11.00, 11.00, 11.00, 11.00, 11.00, 11.00, 10.00, 10.00, 10.00, 10.00,
                         10.00, 10.00, 10.00, 10.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00,
                         8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 7.00, 7.00, 7.00, 7.00, 7.00, 7.00, 7.00,
                         7.00, 7.00, 7.00, 7.00, 7.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00,
                         6.00, 6.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
                         5.00, 5.00, 5.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 3.00, 3.00, 3.00, 3.00, 3.00,
                         3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00,
                         2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                         1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                         1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                         1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                         1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]).astype(np.int)

    print(time.process_time() - start)
    prev_h = np.hstack([prev_h, np.zeros(df['tier'].shape[0] - prev_h.shape[0])])
    df['tier'] = df['tier'].to_numpy() + prev_h

    print(time.process_time() - start)

    df = df.sort_values(by='par', ascending=False)
    df['orank'] = np.linspace(1, df.shape[0], df.shape[0]).astype(np.int)

    print(time.process_time() - start)
    df['prank'] = df.groupby('pos1')['par'].rank(method='first', ascending=False)


    print(time.process_time() - start)
    print("next")

    return df


def toggle(df, name, stat):
    # Stats:
    # 'watch'
    # 'passon'
    # 'keeper'
    df.loc[df['name'] == name, stat] = not df.loc[df['name'] == name, stat].values[0]

def setcell(df, name, stat, value):
    # Stats:
    # 'watch'
    # 'passon'
    # 'keeper'
    df.loc[df['name'] == name, stat] = value

def get_pos_names(df, pos):
    return(df.loc[df[pos] == True].name.tolist())


def get_pos_stats(df, name):
    pos = df.loc[df['name'] == name, 'pos1'].values[0]
    allnames = df.name.tolist()
    posnames = df.loc[(df['pos1'] == pos) |
                             (df['pos2'] == pos) |
                             (df['pos3'] == pos), 'name'].tolist()

    posstats = []
    pind = posnames.index(name)
    for i in range(-10, 11):
        if (pind + i >= 0) & (pind + i < len(posnames)):
            pl = df.loc[df['name'] == posnames[pind + i]]
            if pl.pitcher.values[0]:
                posstats.append([pl.name.values[0],
                                 pl.pos1.values[0],
                                 # pl.orank.values[0],
                                 pl.plistrank.values[0],
                                 pind + i + 1,
                                 pl.my_price.values[0],
                                 pl.espn_price.values[0],
                                 round(pl.par.values[0], 1),
                                 pl.p_k_fpros.values[0],
                                 pl.p_qs_fpros.values[0],
                                 pl.p_svhd_fpros.values[0],
                                 pl.p_era_fpros.values[0],
                                 pl.p_whip_fpros.values[0],
                                 pl.drafted.values[0]])

            else:
                posstats.append([pl.name.values[0],
                                 pl.pos1.values[0],
                                 pl.orank.values[0],
                                 pind + i + 1,
                                 pl.my_price.values[0],
                                 pl.espn_price.values[0],
                                 round(pl.par.values[0], 1),
                                 pl.h_runs_fpros.values[0],
                                 pl.h_hr_fpros.values[0],
                                 pl.h_rbi_fpros.values[0],
                                 pl.h_sb_fpros.values[0],
                                 pl.h_obp_fpros.values[0],
                                 pl.drafted.values[0]])

        else:
            posstats.append(['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])

    ovrstats = []
    oind = allnames.index(name)
    for i in range(-10, 11):
        if (oind + i >= 0) & (oind + i < len(allnames)):
            pl = df.loc[df['name'] == allnames[oind + i]]
            if pl.pitcher.values[0]:
                ovrstats.append([pl.name.values[0],
                                 pl.pos1.values[0],
                                 pl.orank.values[0],
                                 pl['pitchrank'].values[0],
                                 pl.my_price.values[0],
                                 pl.espn_price.values[0],
                                 round(pl.par.values[0], 1),
                                 pl.h_runs_fpros.values[0],
                                 pl.h_hr_fpros.values[0],
                                 pl.h_rbi_fpros.values[0],
                                 pl.h_sb_fpros.values[0],
                                 pl.h_obp_fpros.values[0],
                                 pl.drafted.values[0]])
            else:
                ovrstats.append([pl.name.values[0],
                                 pl.pos1.values[0],
                                 pl.orank.values[0],
                                 pl['hitrank'].values[0],
                                 pl.my_price.values[0],
                                 pl.espn_price.values[0],
                                 round(pl.par.values[0], 1),
                                 pl.h_runs_fpros.values[0],
                                 pl.h_hr_fpros.values[0],
                                 pl.h_rbi_fpros.values[0],
                                 pl.h_sb_fpros.values[0],
                                 pl.h_obp_fpros.values[0],
                                 pl.drafted.values[0]])
        else:
            ovrstats.append(['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])

    return ovrstats, posstats

def savekeepers(df):
    keepers = {
        'Pete Alonso': 13, 'Jazz Chisholm Jr.': 8, 'Shane Bieber': 22,  # Kyle
        'Kris Bryant': 23, 'Giancarlo Stanton': 27, 'Jake Cronenworth': 9,  # Ben
        'Marcus Semien': 24, 'Lance Lynn': 11,  # Scott
        'Shohei Ohtani': 15, 'Jared Walsh': 6, 'Robbie Ray': 6,  # Cope
        'Matt Olson': 16, 'Austin Riley': 11, 'Tyler O\'Neill': 10,  # Jonny
        'Wander Franco': 7, 'Ketel Marte': 12, 'Kyle Schwarber': 11,  # Randy
        'Bo Bichette': 34, 'Salvador Perez': 10, 'Freddy Peralta': 7,  # Cian
        'Fernando Tatis Jr.': 13, 'Yuli Gurriel': 6, 'Sandy Alcantara': 10,  # Alex
        'Rafael Devers': 32, 'Jonathan India': 7, 'Brandon Woodruff': 13,  # Keith
        'Cedric Mullins': 6,  # Tyler
        'Yordan Alvarez': 18, 'Corbin Burnes': 23, 'Carlos Rodon': 9,  # YB
    }

    for p in keepers:
        df.loc[df['name'] == p, ['keeper', 'keeper_price', 'drafted']] = [True, keepers.get(p), True]

    return(df)

def calcprices(df):
    hbudget = .73 * 3120
    spbudget = .23 * 3120
    rpbudget = .04 * 3120

    hitters156df = df.loc[df['hitter']==True].head(156)
    sp60df = df.loc[df['posSP']==True].head(60)
    rp36df = df.loc[df['posRP']==True].head(36)

    # HITTERS
    #Subtract keeper prices from budget
    hitkeepers = hitters156df.loc[hitters156df['keeper']==True, 'keeper_price'].sum()
    hbudget = hbudget - hitkeepers

    #Calculate PAR of leftover players
    hparmin = abs(hitters156df['par'].min())
    hitters156df['par'] += hparmin
    hpar = hitters156df.loc[hitters156df['keeper']==False, 'par'].sum()

    #ParFactor = leftover budget div leftover par
    hfactor = hbudget/hpar

    #STARTING PITCHERS
    #Subtract keeper prices from budget
    spkeepers = sp60df.loc[sp60df['keeper']==True, 'keeper_price'].sum()
    spbudget = spbudget - spkeepers

    #Calculate PAR of leftover players
    spparmin = abs(sp60df['par'].min())
    sp60df['par'] += spparmin
    sppar = sp60df.loc[sp60df['keeper']==False, 'par'].sum()

    #ParFactor = leftover budget div leftover par
    spfactor = spbudget/sppar


    #RELIEF PITCHERS
    #Subtract keeper prices from budget
    rpkeepers = rp36df.loc[rp36df['keeper']==True, 'keeper_price'].sum()
    rpbudget = rpbudget - rpkeepers

    #Calculate PAR of leftover players
    rpparmin = abs(rp36df['par'].min())
    rp36df['par'] += rpparmin
    rppar = rp36df.loc[rp36df['keeper']==False, 'par'].sum()

    #ParFactor = leftover budget div leftover par
    rpfactor = rpbudget/rppar


    #### add min to par, then multiply by factor
    df.loc[df['hitter'] == True, 'par'].add(hparmin)
    df.loc[df['hitter'] == True, 'my_price'] = df.loc[df['hitter']==True, 'par'].add(hparmin).multiply(hfactor).round(1)

    df.loc[df['posSP'] == True, 'par'].add(spparmin)
    df.loc[df['posSP'] == True, 'my_price'] = df.loc[df['posSP']==True, 'par'].add(spparmin).multiply(spfactor).round(1)

    df.loc[df['posRP'] == True, 'par'].add(rpparmin)
    df.loc[df['posRP'] == True, 'my_price'] = df.loc[df['posRP']==True, 'par'].add(rpparmin).multiply(rpfactor).round(1)

    return df


def get_pinfo(df, name):
    pl = df.loc[df['name'] == name]

    pinfo = [pl.name.values[0],
             pl.team.values[0],
             [pl.pos1.values[0],pl.pos2.values[0], pl.pos3.values[0]],
             pl.h_runs_fpros.values[0],
             pl.h_hr_fpros.values[0],
             pl.h_rbi_fpros.values[0],
             pl.h_sb_fpros.values[0],
             pl.h_obp_fpros.values[0],
             pl.orank.values[0],
             pl.prank.values[0],
             pl.my_price.values[0],
             pl.p_k_fpros.values[0],
             pl.p_qs_fpros.values[0],
             pl.p_svhd_fpros.values[0],
             pl.p_era_fpros.values[0],
             pl.p_whip_fpros.values[0],
             pl.h_ab_fpros.values[0],
             pl.p_ip_fpros.values[0],
             bool(pl.watch.values[0]),
             bool(pl.passon.values[0]),
             pl.espn_price.values[0],
             pl.plistrank.values[0],
             pl.lineup.values[0]
             ]

    return pinfo




def save_to_excel(df, avgstatsdf, teamdf, slotsdf):
    with pd.ExcelWriter('player_stats.xlsx') as writer:  # doctest: +SKIP
        df.loc[df['hitter']==True].to_excel(writer, sheet_name='Hitters')
        df.loc[df['pitcher'] == True].to_excel(writer, sheet_name='Pitchers')
        avgstatsdf.to_excel(writer, sheet_name='PosStats')
        teamdf.to_excel(writer, sheet_name='Team')
        slotsdf.to_excel(writer, sheet_name='Slots')

        df.loc[df['posC']==True].to_excel(writer, sheet_name='C')
        df.loc[df['pos1B']==True].to_excel(writer, sheet_name='1B')
        df.loc[df['pos2B']==True].to_excel(writer, sheet_name='2B')
        df.loc[df['posSS']==True].to_excel(writer, sheet_name='SS')
        df.loc[df['pos3B']==True].to_excel(writer, sheet_name='3B')
        df.loc[df['posOF']==True].to_excel(writer, sheet_name='OF')


def load_df_from_excel():
    xls = pd.ExcelFile('player_stats.xlsx', engine='openpyxl')
    hittersdf = pd.read_excel(xls, 'Hitters', engine='openpyxl')
    pitchersdf = pd.read_excel(xls, 'Pitchers', engine='openpyxl')
    #avgstatsdf = pd.read_excel(xls, 'PosStats')

    df = pd.concat([hittersdf, pitchersdf])


    return df #avgstatsdf


def load_teamdf_from_excel():


    try:
        xls = pd.ExcelFile('player_stats.xlsx', engine='openpyxl')
        teamdf = pd.read_excel(xls, 'Team', index_col=0, engine='openpyxl')
    except:
        team_header = ['Pos', 'Name', 'R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'QS', 'SVHD', 'ERA', 'WHIP', 'HP', 'Price']
        pos = ['C', '1B', '2B', 'SS', '3B', 'MI', 'CI', 'OF1', 'OF2', 'OF3', 'OF4', 'OF5', 'UTIL',
               'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'RP1', 'RP2', 'RP3', 'B1', 'B2', 'B3', 'TOTAL']
        teamdf = pd.DataFrame(columns=team_header)
        for x in team_header:
            teamdf[x] = [0] * 26
        teamdf['Pos'] = pos
        teamdf['Name'] = ['-'] * 26
        teamdf['HP'] = ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                        'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'RP', 'RP', '-', '-', '-', '-']


    return teamdf


def load_slots_from_excel():

    try:
        xls = pd.ExcelFile('player_stats.xlsx', engine='openpyxl')
        slotsdf = pd.read_excel(xls, 'Slots', index_col=0, engine='openpyxl')
    except:
        slot_header = ['Slot', 'Target', 'Actual', 'Diff']
        myslots = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13',
                   'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7', 'RP1', 'RP2', 'B1', 'B2', 'B3',
                   'Hitters', 'SPs', 'RPs']
        targets = [40, 34, 27, 24, 18, 13, 12, 8, 6, 4, 2, 1, 1,
                   22, 15, 10, 8, 5, 1, 1,
                   3, 2,
                   1, 1, 1,
                   193, 62, 5]

        slotsdf = pd.DataFrame(columns=slot_header)
        slotsdf['Target'] = targets
        slotsdf['Slot'] = myslots
        slotsdf['Actual'] = [0]*28
        slotsdf['Diff'] = [0]*28


    return slotsdf


def find_in_2d_array(array, item):
    index = -1
    for cntr, i in enumerate(array):
        if i[0] == item:
            index = cntr
            break

    return index
