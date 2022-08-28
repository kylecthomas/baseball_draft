import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests
from player import Player
import numpy as np
import xlsxwriter
from peewee import *
from layouts import *
from data_analysis import *
import time
from pprint import pprint
import tkinter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')



def trim_list(names, typename):
    # print(typename)
    newnames=[]
    for nm in names:
        if typename.lower() in nm.lower():
            newnames.append(nm)

    return newnames


def get_player_stats(index):
    p = Player.get(Player.orank == index)
    stats = [p.name, p.pos1, p.orank, p.prank, -1, -1, -1, p.drafted]
    return stats


pdata = get_all_sources('pickle')
df, avgstatsdf, teamdf, slotsdf = df_from_sources(pdata)



allnames = df['name'].tolist()
listnames = allnames
p = listnames[0]
ovrstats, posstats = get_pos_stats(df, p)
pinfo = get_pinfo(df, p)

layout = DraftLayout(df)
window = layout.window

layout.update_select(listnames)
layout.update_positional(posstats)
layout.update_overall(ovrstats)
layout.update_pinfo(pinfo)
layout.update_team(teamdf)
layout.update_slots(slotsdf)



typeChange=False
while True:  # Event Loop


    event, values = window.Read(timeout=500)


    if event != '__TIMEOUT__':
        pass
        #print(event, values)

    if event == '__TIMEOUT__':
        window.Element('_myprice_').Update(values['_myprice_'])
        if typeChange:
            layout.update_cats(p, 'select')
            typeChange = False

    if event is None or event == 'Exit':
        save_to_excel(df, avgstatsdf, teamdf, slotsdf)
        print("BYYYEEEEEEEEEEEEEEEEE")
        break
    if event == '_typename_':
        listnames = trim_list(allnames, values['_typename_'])
        window.Element('_selectname_').Update(listnames)
        typeChange = True

        # label each value with key
        # function in player.py returns list of values
        # set values using keys to elements in list

        if len(listnames) > 0:
            p = listnames[0]

        ovrstats, posstats = get_pos_stats(df, p)
        pinfo = get_pinfo(df, p)

        layout.update_positional(posstats)
        layout.update_overall(ovrstats)
        layout.update_pinfo(pinfo)

    if event == '_selectname_':
        if len(values['_selectname_']) > 0:
            p = values['_selectname_'][0]
            ovrstats, posstats = get_pos_stats(df, p)
            pinfo = get_pinfo(df, p)

            layout.update_positional(posstats)
            layout.update_overall(ovrstats)
            layout.update_pinfo(pinfo)
            layout.update_cats(p, 'select')

            window.Refresh()


    if event == '_pass_':
        setcell(df, p, 'passon', values['_pass_'])

    if event == '_watch_':
        setcell(df, p, 'watch', values['_watch_'])

    if event == '_fetch_':
        pdata = get_all_sources('site')
        df, avgstatsdf, teamdf, slotsdf = df_from_sources(pdata)

    if event == '_savetoxls_':
        save_to_excel(df, avgstatsdf, teamdf, slotsdf)
        print("Saved")

    if event == '_posfil_':
        val = values['_posfil_']

        if val == 'ALL':
            allnames = df['name'].tolist()
        if val == 'H':
            allnames = df.loc[df['hitter']==True,'name'].tolist()
        if val == 'C':
            allnames = df.loc[df['posC']==True,'name'].tolist()
        if val == '1B':
            allnames = df.loc[df['pos1B']==True,'name'].tolist()
        if val == '2B':
            allnames = df.loc[df['pos2B']==True,'name'].tolist()
        if val == 'SS':
            allnames = df.loc[df['posSS']==True,'name'].tolist()
        if val == '3B':
            allnames = df.loc[df['pos3B']==True,'name'].tolist()
        if val == 'OF':
            allnames = df.loc[df['posOF']==True,'name'].tolist()
        if val == 'SP':
            allnames = df.loc[df['posSP']==True,'name'].tolist()
        if val == 'RP':
            allnames = df.loc[df['posRP']==True,'name'].tolist()
        if val == 'MI':
            allnames = df.loc[(df['pos2B']==True) | (df['posSS']==True),'name'].tolist()
        if val == 'CI':
            allnames = df.loc[(df['pos1B']==True) | (df['pos3B']==True),'name'].tolist()

        listnames = trim_list(allnames, values['_typename_'])
        window.Element('_selectname_').Update(listnames)

    if event == '_leaguedraft_':
        setcell(df, p, 'drafted', True)

        ovrstats, posstats = get_pos_stats(df, p)
        layout.update_positional(posstats)
        layout.update_overall(ovrstats)

        layout.update_cats(p, 'draft')

        save_to_excel(df, avgstatsdf, teamdf, slotsdf)

    if event == '_medraft_':
        if values['_myprice_'] != '':
            setcell(df, p, 'drafted', True)
            ovrstats, posstats = get_pos_stats(df, p)
            layout.update_positional(posstats)
            layout.update_overall(ovrstats)

            layout.update_cats(p, 'draft')

        layout.draft_me(df, teamdf, slotsdf, p, values['_slot_'], values['_myprice_'], values['_mypos_'])

        save_to_excel(df, avgstatsdf, teamdf, slotsdf)


    if event == '_undraft_':
        setcell(df, p, 'drafted', False)

        ovrstats, posstats = get_pos_stats(df, p)
        layout.update_positional(posstats)
        layout.update_overall(ovrstats)

        layout.update_cats(p, 'undraft')

    if ('ovr' in event) or ('pos' in event):
        p = window[event].DisplayText

        ovrstats, posstats = get_pos_stats(df, p)
        pinfo = get_pinfo(df, p)

        layout.update_positional(posstats)
        layout.update_overall(ovrstats)
        layout.update_pinfo(pinfo)
        layout.update_cats(p, 'select')

        try:
            nindex = listnames.index(p)
        except:
            nindex = 0
        window['_selectname_'].update(set_to_index=nindex, scroll_to_index = nindex-3)

        window.Refresh()

    if 'cats' in event:
        # print(event, values)
        # pprint(vars(window[event]))

        p = window[event].Tooltip.split(' :: ')[0]

        ovrstats, posstats = get_pos_stats(df, p)
        pinfo = get_pinfo(df, p)

        layout.update_positional(posstats)
        layout.update_overall(ovrstats)
        layout.update_pinfo(pinfo)
        layout.update_cats(p, 'select')

        try:
            nindex = listnames.index(p)
        except:
            nindex = 0
        window['_selectname_'].update(set_to_index=nindex, scroll_to_index=nindex-3)

        window.Refresh()

window.Close()








