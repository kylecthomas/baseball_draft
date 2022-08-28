import PySimpleGUI as sg


class DraftLayout():
    def __init__(self, df):

        self.names = [[0 for i in range(100)] for j in range(12)]
        self.drafts = [[0 for i in range(100)] for j in range(12)]
        self.vals = [[0 for i in range(100)] for j in range(12)]
        self.price = [[0 for i in range(100)] for j in range(12)]


        self.pselect_layout = [
            [sg.Input(do_not_clear=True, key='_typename_', change_submits=True, size=(30, 1)),
             sg.InputCombo(['ALL', 'H', 'C', '1B', '2B', '3B', 'SS', 'MI', 'CI', 'OF', 'SP', 'RP'],
                           key='_posfil_', size=(6, 1), change_submits=True)],
            [sg.Listbox(values=([]), key='_selectname_', select_mode='single',
                        change_submits=True, bind_return_key=True, size=(30, 8))],
        ]

        size=9
        self.pinfo_layout = [
            [sg.Text('Name: '),
             sg.Text('a', key='_name_', size=(16, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Team: '),
             sg.Text('a', key='_team_', size=(12, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Positions: ', size=(18, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_poss_', size=(12, 1), font=('Helvetica', size), text_color='black')
             ],
            [sg.Text('R:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_runs_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('K:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_ks_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Rank', size=(8, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_ovrrank_', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Roster:', size=(8, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_roster_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             ],
            [sg.Text('HR:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_hr_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('QS:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_qs_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Pos Rank', size=(8, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_posrank_', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('PLIST:', size=(8, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_plist_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             ],
            [sg.Text('RBI:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_rbi_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('SVHD:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_svhd_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('Worth', size=(8, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_worth_', size=(4, 1), font=('Helvetica', size), text_color='black')
             ],
            [sg.Text('SB:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_sb_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('ERA:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_era_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('ESPN: ', size=(6, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_espnprice_', size=(10, 1), font=('Helvetica', size), text_color='black'),

             ],
            [sg.Text('OBP:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_obp_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('WHIP:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_whip_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Checkbox('Watch', key='_watch_', default=False, change_submits=True, size=(8, 1)),
             ],
            [sg.Text('AB:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_abs_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('IP:', size=(4, 1), font=('Helvetica', size), text_color='black'),
             sg.Text('a', key='_ips_', size=(10, 1), font=('Helvetica', size), text_color='black'),
             sg.Checkbox('Pass', key='_pass_', default=False, change_submits=True, size=(10, 1)),
            ],
        ]

        self.draft_layout = [
            [sg.Button('UNDraft Me', size=(12, 1), key='_undraft_')],
            [sg.Button('Draft Me', size=(12, 1), key='_medraft_')],
            [sg.Button('Draft League', size=(12, 1), key='_leaguedraft_')],
            [sg.Input('', size=(8, 1), key='_myprice_'), sg.Text('Price', key='_mypricetext_')],
            [sg.InputCombo(['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8',
                            'H9', 'H10', 'H11', 'H12', 'H13', 'SP1', 'SP2',
                            'SP3', 'SP4', 'SP5', 'SP6', 'RP1', 'RP2', 'RP3',
                            'B1', 'B2', 'B3'], key='_slot_', size=(8, 1)),
             sg.Text('Slot')],
            [sg.InputCombo(['C', '1B', '2B', '3B', 'SS', 'MI', 'CI', 'OF1', 'OF2', 'OF3', 'OF4', 'OF5', 'UTIL',
                            'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'RP1', 'RP2', 'RP3'], key='_mypos_', size=(8, 1)),
             sg.Text('Pos')],
        ]

        self.data_layout = [
            [sg.Button('Fetch Stats', size=(12, 1), key='_fetch_')],
            [sg.Button('Save to Excel', size=(12, 1), key='_savetoxls_')],
        ]

        self.cat_legend_layout = [
            [sg.Text('R   ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('HR ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('RBI ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('SB  ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('OBP ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('K   ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('QS  ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('SVH ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('ERA ', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('WHIP', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('PLIST', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
            [sg.Text('Watch', size=(7, 1), font = ('Helvetica', 8),pad=(0,0))],
        ]

        self.overall_layout = self.draw_rank_table('ovr')
        self.position_layout = self.draw_rank_table('pos')
        self.team_layout = self.draw_team_table()
        self.slot_layout = self.draw_slot_table()
        self.cat_layout = self.draw_cat_table(df)

        #sg.Frame('Stats', self.team_layout)

        self.layout_tab1 = [
            [sg.Frame('Players', self.pselect_layout),
             sg.Frame('Draft', self.draft_layout),
             sg.Frame('Stats', self.pinfo_layout),
            sg.Frame('Data', self.data_layout)],
            [sg.Frame('Overall', self.overall_layout),
             sg.Frame('Positional', self.position_layout)],
            [sg.Frame('', self.cat_legend_layout),
             sg.Frame('', self.cat_layout)],
        ]

        self.layout_tab2 = [
            [sg.Frame('Stats', self.team_layout), sg.Frame('Slots', self.slot_layout)],
        ]

        # self.mousegraph = [
        #     [sg.Graph((1600, 1000), (0, 0), (1600, 1000), key='-GRAPH-', change_submits=True, drag_submits=False)],
        # ]

        self.layout = [[sg.TabGroup([[sg.Tab('Draft', self.layout_tab1),sg.Tab('Team', self.layout_tab2)]])],]

        self.window = sg.Window('Draft 2022', size=(1600, 1000), location = (0, 0), auto_size_buttons=False,
                           default_element_size=(5, 1), resizable=True).Layout(self.layout).Finalize()

    def update_pinfo(self, new):
        hd = ['_name_', '_team_', '_poss_', '_runs_', '_hr_','_rbi_',
              '_sb_', '_obp_', '_ovrrank_', '_posrank_', '_worth_',
              '_ks_', '_qs_', '_svhd_', '_era_', '_whip_', '_abs_', '_ips_',
              '_watch_', '_pass_', '_espnprice_', '_plist_', '_roster_']

        for cntr, i in enumerate(hd):
            self.window.Element(i).Update(value=new[cntr])

    def update_select(self, new):
        self.window.Element('_selectname_').Update(new)

    def update_overall(self, new):
        for i in range(0,21,1):
            if i == 10:
                bg = '#b3f0ff'
                if new[i][0] in self.names[11]:
                    bg = '#00cc00'
            elif new[i][0] in self.names[11]:
                bg = '#e6ffe6'
            else:
                bg = 'white'
            for j in range(0,12,1):
                if new[i][12] == True:
                    bg = '#ffb3b3'
                self.window.Element('ovr_'+str(i)+"_"+str(j)).Update(value=new[i][j], background_color=bg)

    def update_positional(self, new):
        for i in range(0,21,1):
            if i == 10:
                bg = '#b3f0ff'
                if new[i][0] in self.names[11]:
                    bg = '#00cc00'
            elif new[i][0] in self.names[11]:
                bg = '#e6ffe6'
            else:
                bg = 'white'
            for j in range(0,12,1):
                if new[i][12] == True:
                    bg = '#ffb3b3'
                self.window.Element('pos_'+str(i)+"_"+str(j)).Update(value = new[i][j], background_color=bg)

    def update_team(self, teamdf):
        teamdat = teamdf.reset_index().values.tolist()

        teamcombotemp = teamdf.loc[0:24, 'Pos':'Name'].values.tolist()

        myteam = []
        for x in teamcombotemp:
            if x[1] == '-':
                myteam.append(x[0])
            else:
                myteam.append(x[0] + ': XXX')

        self.window.Element('_mypos_').Update(values=myteam)

        for i in range(0, 28, 1):
            for j in range(0, 14, 1):
                if i < 26:
                    val = teamdat[i][j+1]
                    if isinstance(val, float):
                        val = round(val,1)

                else:
                    val = '-'
                self.window.Element('team_'+str(i)+"_"+str(j)).Update(value=val)

    def update_slots(self, slotsdf):
        slotsdat = slotsdf.reset_index().values.tolist()

        slotscombotemp = slotsdf.loc[0:24, 'Slot':'Actual'].values.tolist()

        myslots = []
        for x in slotscombotemp:
            if x[2] == 0:
                myslots.append(x[0] + ': ' + str(x[1]))
            else:
                myslots.append(x[0] + ': XXX')

        self.window.Element('_slot_').Update(values = myslots)

        for i in range(0,28,1):
            for j in range(0,4,1):
                self.window.Element('slots_'+str(i)+"_"+str(j)).Update(value = slotsdat[i][j+1])

    def update_cats(self, name, mode):
        for i in range(len(self.names)):
            for j in range(len(self.names[0])):
                if (mode == 'draft') & (self.names[i][j] == name):
                    self.drafts[i][j] = True
                elif (mode == 'undraft') & (self.names[i][j] == name):
                    self.drafts[i][j] = False

                if not self.vals[i][j]:
                    bg = 'white'
                elif self.drafts[i][j]:
                    bg = 'red'
                elif self.names[i][j] == name:
                    bg = 'blue'
                else:
                    bg = 'green'

                self.window.Element('cats_' + str(i) + "_" + str(j)).Update(background_color=bg)


    def draw_rank_table(self, pre):
        size = 9
        layout = [[sg.T('Name', size=(16, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('Pos', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('PList', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('P Rank', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('Worth', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('ESPN', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('PAR', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('R', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('HR', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('RBI', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('SB', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   sg.T('OBP', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                        font=('Helvetica', size), text_color='black'),
                   ]]

        for i in range(0, 21, 1):
            bg = 'white'

            row = [sg.T('-', size=(16, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_0"), enable_events=True),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_1")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_2")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_3")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_4")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_5")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_6")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre+"_"+str(i)+"_7")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_8")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_9")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_10")),
                   sg.T('-', size=(5, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_11")),
                   ]
            layout.append(row)

        layout.append(
            [sg.T('Name', size=(16, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('Pos', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('PList', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('P Rank', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('Worth', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('ESPN', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('PAR', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('K', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('QS', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('SVHD', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('ERA', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             sg.T('WHIP', size=(5, 1), background_color='grey', justification='center', pad=(1, 1),
                  font=('Helvetica', size)),
             ]
        )

        return layout

    def draw_team_table(self):
        size = 10

        layout = [[sg.T('POS', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('Name', size=(16, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('R', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('HR', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('RBI', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('SB', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('OBP', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('K', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('QS', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('SVHD', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('ERA', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('WHIP', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('HP', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   sg.T('Price', size=(6, 1), background_color='grey', justification='center',
                        pad=(1, 1), text_color='black', font=('Helvetica', size)),
                   ]]

        for i in range(0, 28, 1):
            bg = 'white'
            pre = 'team'

            row = [sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_0")),
                   sg.T('-', size=(16, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_1")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_2")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_3")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_4")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_5")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_6")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_7")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_8")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_9")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_10")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_11")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_12")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black', font=('Helvetica', size),
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_13")),
                   ]
            layout.append(row)

        return layout

    def draw_slot_table(self):
        layout = [[sg.T('Slot', size=(6, 1), background_color='grey', text_color='black', justification='center', pad=(1, 1)),
                   sg.T('Target', size=(6, 1), background_color='grey', text_color='black', justification='center', pad=(1, 1)),
                   sg.T('Actual', size=(6, 1), background_color='grey', text_color='black', justification='center', pad=(1, 1)),
                   sg.T('Diff', size=(6, 1), background_color='grey', text_color='black', justification='center', pad=(1, 1)),
                   ]]

        for i in range(0, 28, 1):
            bg = 'white'
            pre = 'slots'

            row = [sg.T('-', size=(6, 1), background_color=bg, text_color='black',
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_0")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black',
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_1")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black',
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_2")),
                   sg.T('-', size=(6, 1), background_color=bg, text_color='black',
                        justification='center', pad=(1, 1), key=(pre + "_" + str(i) + "_3")),
                   ]
            layout.append(row)

        return layout

    def draw_cat_table(self, df):
        layout = []
        pre = 'cats'

        self.names, self.drafts, self.vals, self.price= self.tooltips(df)

        for i in range(len(self.names)):
            layout_row = []
            for j in range(100):
                if self.drafts[i][j]:
                    bg = 'red'
                else:
                    bg = 'green'

                tt = (self.names[i][j] + ' :: ' + str(self.vals[i][j])) + ' :: $' + str(self.price[i][j])

                if (i == 11) & (self.vals[i][j] == False):
                    tt = ''
                    bg = 'white'

                cell = sg.T('', size=(3, 3), background_color=bg, pad=(1, 1), key=(pre + "_" + str(i) + "_" + str(j)),
                            text_color='black', font=('Helvetica', 2), tooltip=tt, enable_events = True)
                layout_row.append(cell)
            layout.append(layout_row)

        return layout

    def tooltips(self, df):
        names = []
        drafts = []
        vals = []
        price = []

        # sortby = ['h_runs_fpros', 'h_hr_fpros', 'h_rbi_fpros', 'h_sb_fpros', 'h_obp_fpros',
        #          'p_k_fpros', 'p_qs_fpros', 'p_svhd_fpros', 'p_era_fpros', 'p_whip_fpros']

        sortby = [['hitter', 'h_runs_fpros'],
                  ['hitter', 'h_hr_fpros'],
                  ['hitter', 'h_rbi_fpros'],
                  ['hitter', 'h_sb_fpros'],
                  ['hitter', 'h_obp_fpros'],
                  ['pitcher', 'p_k_fpros'],
                  ['pitcher', 'p_qs_fpros'],
                  ['pitcher', 'p_svhd_fpros'],
                  ['posSP', 'p_era_fpros'],
                  ['posSP', 'p_whip_fpros'],
                  ['posSP', 'plistrank'],
                  ['watch', 'watch']]

        for i, x in enumerate(sortby):
            asc = [False, False]
            if (x[1] == 'p_era_fpros') | (x[1] == 'p_whip_fpros') | (x[1] == 'plistrank') | (x[1] == 'watch'):
                asc = [False, True]

            sortdf = df.sort_values(by=x, ascending=asc)
            names.append(sortdf['name'].head(100).tolist())
            drafts.append(sortdf['drafted'].head(100).tolist())
            vals.append(sortdf[x[1]].head(100).tolist())
            price.append(sortdf['my_price'].head(100).tolist())

        for j, x in enumerate(vals[11]):
            if not x:
                names[11][j] = '-'

        return names, drafts, vals, price

    def draft_me(self, df, teamdf, slotsdf, p, slot, myprice, mypos):
        if myprice == '':
            self.window.Element('_mypricetext_').Update(value='Price', background_color='red')
            pass
        else:
            #Update Slots
            myprice = int(myprice)
            if ':' in slot:
                slot = slot[0:slot.index(':')]
            if ':' in mypos:
                mypos = mypos[0:mypos.index(':')]


            self.window.Element('_mypricetext_').Update(value='Price', background_color='white')

            if myprice > 0:
                targ = slotsdf.loc[slotsdf['Slot'] == slot, 'Target'].values[0]
                slotsdf.loc[slotsdf['Slot'] == slot, 'Actual'] = myprice
                slotsdf.loc[slotsdf['Slot'] == slot, 'Diff'] = targ - myprice




                #Update Team
                hp = 'H'
                if df.loc[df['name'] == p, 'pos1'].values[0] == 'SP':
                    hp = 'SP'
                if df.loc[df['name'] == p, 'pos1'].values[0] == 'RP':
                    hp = 'RP'

                tempPar = [[p],
                        df.loc[df['name'] == p, 'Rpoints':'WHIPpoints'].values.tolist()[0],
                        [hp],
                        [myprice]]

                pPar = [i for j in tempPar for i in j]

                teamdf.loc[teamdf['Pos'] == mypos, 'Name':'Price'] = pPar

            else:
                slotsdf.loc[slotsdf['Slot'] == slot, 'Actual':'Diff'] = 0
                teamdf.loc[teamdf['Pos'] == mypos, 'Name':'WHIP'] = ['-', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                teamdf.loc[teamdf['Pos'] == mypos, 'Price'] = 0

            slotsdf.loc[25, 'Diff'] = slotsdf.loc[0:12, 'Diff'].sum()
            slotsdf.loc[26, 'Diff'] = slotsdf.loc[13:18, 'Diff'].sum()
            slotsdf.loc[27, 'Diff'] = slotsdf.loc[19:21, 'Diff'].sum()
            self.update_slots(slotsdf)

            cols = ['R', 'HR', 'RBI', 'SB', 'OBP', 'K', 'QS', 'SVHD', 'ERA', 'WHIP', 'Price']
            teamdf.loc[25] = teamdf.loc[0:24, cols].sum()
            teamdf.loc[25, 'Pos'] = 'Total'
            teamdf.loc[25, 'Name'] = '-'
            teamdf.loc[25, 'HP'] = '-'
            self.update_team(teamdf)


