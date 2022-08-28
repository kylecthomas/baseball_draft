Every year for my fantasy baseball draft I would spend hours searching websites, copy/pasting data into spreadsheets, and manually calculating players projected values. No more! I created a program that does all the work for me, and even has a GUI interface to track the draft in real time, and suggest who I should draft next.  
  
Packages used:  
  
PySimpleGUI  
numpy  
matplotlib  
BeautifulSoup  
selenium  
pickle  
pandas  
Program Functions:  
  
Scrapes popular baseball websites for projected stats for every player in the league, and loads data into a pandas dataframe  
Calculates a value of each player based on scoring categories of the league: (R, HR, RBI, SB, OBP for hitters; K, QS, SV+HLD, WHIP, ERA for pitchers)  
Assigns a dollar amount to each player to be used in our salary cap auction draft  
Scrapes other popular websites such as pitcherlist, rosterresource to gather more information about rankings  
Displays all information in a GUI to be used during the draft. The GUI: **Type in or choose in a list the player who is currently up for auction **Display their projected stats, calculated salary, if they are watched or should be passed, where they rank in each category **Track players who have been drafted by other teams, or by your own **Track the amount spent so far and what you have left to spend **Track the stats of your team so far and suggest what stats and players you should target moving forward  
  

