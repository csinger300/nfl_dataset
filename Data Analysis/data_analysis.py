########## This file will contain all the main functions and helper functions you utilized for each analysis ##########
import pymysql
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

def create_cursor(host_name, user_name, pw, db_name):
    try:
        connection = pymysql.connect(host = host_name, user = user_name, password = pw, db = db_name, charset = "utf8mb4", cursorclass = pymysql.cursors.Cursor)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(e)
        print(f"Couldn't log in to MySQL server using this password: {pw}.\n")

'''This analysis question gives us the name of the top 10 players with the most sack yards of all time. A defense that is able to not only block
the oncoming team, but can also subtract yards from them is crucial for a team's success. Knowing information such as this can tell you
which defensive players have shown the most success, and if they are still active players, they are ones to pay attention to. Team owners with
defenses that are greatly suffering could look into negotiating a trade for one of these higher ranking players.'''
def analysis_1(cursor):
    query = 'SELECT nameFull AS Full_Name, sum(sackYards)*-1 AS Total_Yards, count(sackTable.playerId) as NumberOf_Sacks FROM sackTable JOIN playerTable ON sackTable.playerId = playerTable.playerId GROUP BY sackTable.playerId ORDER BY Total_Yards DESC LIMIT 10;'

    cursor.execute(query)
    result = cursor.fetchall()
    return result

'''This next analysis question gives us the names of the top 5 players with the greatest and least fumble turnover rates, respectively. Having a quarterback
with good ball control is the backbone of a strong football team. Players that crack under pressure, panic, and lose their grip are not players
that you can rely on. That is why this information is interesting to look at. One interesting thing that became evident, however, is that the QBs
who have been active the longest and played in the most games tend to have significantly more fumbles. The total number of fumbles, then, becomes less meaningful,
and we need to focus more on the rate of fumbles (that result in a turnover) per number of games that the QB played in. This gives a more accurate representation of which players
are giving up the ball more on average.'''
def analysis_2(cursor):
    query1 = 'SELECT nameFull as Full_Name, (count(CASE WHEN fumTurnover = "True" then 1 end)/count(fumTurnover)) as Fum_Turnover_Rate, draftTeam FROM fumbleTable JOIN draftTable ON fumbleTable.playerId = draftTable.playerId GROUP BY fumbleTable.playerId HAVING Fum_Turnover_Rate < 1 AND Fum_Turnover_Rate > 0 ORDER BY Fum_Turnover_Rate DESC LIMIT 10;'
    query2 = 'SELECT nameFull as Full_Name, (count(CASE WHEN fumTurnover = "True" then 1 end)/count(fumTurnover)) as Fum_Turnover_Rate, draftTeam FROM fumbleTable JOIN draftTable ON fumbleTable.playerId = draftTable.playerId GROUP BY fumbleTable.playerId HAVING Fum_Turnover_Rate < 1 AND Fum_Turnover_Rate > 0 ORDER BY Fum_Turnover_Rate ASC LIMIT 10;'

    cursor.execute(query1)
    result1 = cursor.fetchall()
    cursor.execute(query2)
    result2 = cursor.fetchall()
    return (result1, result2)

'''This next analysis looked at the top 10 players with the most reception yards. A strong connection between a quarterback and a receiver is
something that will take a football team from good to great. Looking at this question we can see which receivers over the years have accumulated
the most receiving yards, and by looking at the list you can see most of their legacies speak for themselves. Receivers with the most yards greatly
correlates to some of the best players in the league without question. These are consistent players that are extremely desirable to any team in the league.'''
def analysis_3(cursor):
    query = 'SELECT nameFull as Full_Name, sum(recYards) as Total_Yards FROM receiverTable JOIN draftTable ON receiverTable.playerId = draftTable.playerId GROUP BY receiverTable.playerId ORDER BY Total_Yards DESC LIMIT 10;'

    cursor.execute(query)
    result = cursor.fetchall()
    return result

'''This analysis looks more into the draft data and looks at what colleges are known for producing the most nfl drafted players. This information
could be extremely relevant if a highschool player was deciding where to commit for college. How you perform in college greatly indicates when and
where you will go in the draft should you try for the nfl. The first query shows, in general, the top 5 schools that produce nfl drafted players and how many.
The second query gets a bit more specific, narrowing the list to the top 5 schools that produce round 1 draft picks.'''
def analysis_4(cursor):
    query1 = 'SELECT college, count(college) FROM draftTable GROUP BY college ORDER BY count(college) DESC LIMIT 5;'
    query2 = 'SELECT college, count(college) FROM draftTable WHERE round = 1 GROUP BY college ORDER BY count(college) DESC LIMIT 5;'

    cursor.execute(query1)
    result1 = cursor.fetchall()
    cursor.execute(query2)
    result2 = cursor.fetchall()
    return (result1, result2)

'''This lasy analysis question looks into what teams on average have the best draft picks. A better draft pick is a number closer to 1,
but it is also well-known that an underperforming team in the previous season will have a higher draft pick in an effort to try and
improve their lineup. I was interested to see how this information correlated with the teams that are notorious for winning and losing.
It was not surprising to see teams like the packers and the patriots having lower draft picks on average, as their teams are known for
performing well in the league.'''
def analysis_5(cursor):
    query = 'SELECT draftTeam, avg(pick) AS Average_DraftPick FROM draftTable WHERE round = 1 GROUP BY teamId ORDER BY avg(pick) ASC;'

    cursor.execute(query)
    result = cursor.fetchall()
    return result


'''This first insightful visual gives us a look at which teams have the greatest number of total interceptions. When analyzing nfl teams,
an immediate red flag is a team with a large amount of turnovers. This information will allow us to see which teams are outperforming others
in this category, and it will give more insight into the best overall teams in the league. No matter how strong a team may seem, if they are
turning over the ball they will not win games.'''
def visual_1(cursor):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    teams = 'SELECT count(interceptionId), draftTeam FROM draftTable JOIN interceptionTable ON draftTable.teamId = interceptionTable.teamId WHERE draft = 2019 GROUP BY draftTable.draftTeam;'
    cursor.execute(teams)
    results = cursor.fetchall()
    intList = []
    teamList = []
    for result in results:
        intList.append(result[0])
        teamList.append(result[1])

    plt.rcdefaults()
    fig, ax = plt.subplots()

    plt.bar(teamList, intList, width = 0.2, color=sns.color_palette("deep"))

    ax.set_ylabel('Total Interceptions')
    ax.set_xlabel('Team')
    ax.set_title('Total Number of Interceptions Per NFL Team')

    plt.show()

'''My second visual shows the top player positions that make sacks. Sacking a quarterback is a huge plus for the defensive team, and teams want to
maximize their ability to do that at all times. By looking at this visual, people are able to see which position is creating the most sacks for their team.
Team owners could then make strategic decisions such as drafting more players in those positions or putting their stronger defensive linemen in those positions
to see if they have a better chance of a sack that way.'''
def visual_2(cursor):
    query = 'SELECT sackPosition, count(playerId) as NumberOf_Sacks FROM sackTable GROUP BY sackPosition ORDER BY NumberOf_Sacks DESC;'

    cursor.execute(query)
    results = cursor.fetchall()

    sackPos = []
    sackCount = []
    for result in results:
        sackPos.append(result[0])
        sackCount.append(result[1])

    fig, ax = plt.subplots()

    sns.set_context('paper')
    plt.bar(sackPos, sackCount, width = 0.5, color=sns.color_palette("deep") )
    ax.set_ylabel('Total Sacks')
    ax.set_xlabel('Position')
    ax.set_title('Positions with the most sacks')

    fig.autofmt_xdate()

    plt.show()

'''My last visual is meant to show the trend of the Falcon's and Patriot's first draft pick spot over the years. There is often, as we saw in one of my analysis questions,
a correlation between teams performing well/poorly and having a low/high draft pick for the next season. The Falcons are the team I've grown up supporting my
entire life, and I am curious to see how their draft picks have changed over the years, and if it has some sort of correlation with how I know they performed
in the previous season. One of the best teams in the league hands down is the patriots, and I am curious to see how the two's draft picks compare to each other.
It is extremely interesting to see how the draft picks for both teams often move in sync with one another, indicating that both teams often do well when one does well.'''
def visual_3(cursor):
    query = 'SELECT draftTeam, pick, draft FROM draftTable WHERE round = 1 AND (draftTeam = "ATL" OR draftTeam = "NE") ORDER BY draftTeam ASC, draft ASC;'

    cursor.execute(query)
    results = cursor.fetchall()

    teamList = ['Falcons', 'Patriots']
    yearList1 = []
    pickList1 = []
    yearList2 = []
    pickList2 = []
    for result in results:
        if result[0] == "ATL":
            if result[2] not in yearList1:
                yearList1.append(result[2])
                pickList1.append(result[1])
        else:
            if result[2] not in yearList2:
                yearList2.append(result[2])
                pickList2.append(result[1])

    fig, ax = plt.subplots()

    plt.plot(yearList1, pickList1, color='red')
    plt.plot(yearList2, pickList2, color='blue')

    falcons = mpatches.Patch(color='red', label='Falcons')
    patriots = mpatches.Patch(color='blue', label='Patriots')
    plt.legend(handles=[falcons, patriots])

    ax.set_ylabel('Draft Pick')
    ax.set_xlabel('Year')
    ax.set_title('Falcons vs. Patriots Round 1 Draft Picks')

    plt.show()

def summary_file1(cursor):
    f = open('summary_1.csv', 'w')
    query = 'SELECT draftTeam, teamId, count(playerId), avg(pick) AS Average_DraftPick, min(draft), max(draft) FROM draftTable GROUP BY teamId ORDER BY draftTeam ASC;'

    cursor.execute(query)
    results = cursor.fetchall()

    datalist = []
    for result in results:
        alist = []
        for data in result:
            alist.append(data)
        datalist.append(alist)
    for data in datalist:
        data[1] = str(data[1])
        data[2] = str(data[2])
        data[3] = str(float(data[3]))
        data[4] = str(data[4])
        data[5] = str(data[5])
    col_names = ['Team Name', 'TeamID', 'Total Players Drafted', 'Average Round 1 Draft Pick', 'First Draft Year', 'Most Recent Draft Year']
    header = ",".join(col_names) + '\n'
    f.write(header)
    for data in datalist:
        row_value = ",".join(data) + "\n"
        f.write(row_value)
    f.close()

def summary_file2(cursor):
    f = open('summary_2.csv', 'w')
    query = 'SELECT playerTable.nameFull, draftTable.playerId, draftTable.draft, draftTable.position, draftTable.heightInches, draftTable.weight, draftTeam, draftTable.college FROM draftTable JOIN playerTable ON draftTable.playerId = playerTable.playerId WHERE playerTable.position = "QB" AND draftTable.round = 1 GROUP BY draftTable.playerId ORDER BY nameFull ASC;'

    cursor.execute(query)
    results = cursor.fetchall()

    datalist = []
    for result in results:
        alist = []
        for data in result:
            alist.append(data)
        datalist.append(alist)
    for data in datalist:
        data[1] = str(data[1])
        data[2] = str(data[2])
        data[4] = str(data[4])
        data[5] = str(data[5])
    col_names = ['Name', 'PlayerID', 'Draft Year', 'Position', 'Height', 'Weight', 'Draft Team', 'College']
    header = ",".join(col_names) + '\n'
    f.write(header)
    for data in datalist:
        row_value = ",".join(data) + "\n"
        f.write(row_value)
    f.close()



def main():
    # create a cursor object. Fill in the pw parameter if you have a password to MySQL server
    cursor = create_cursor('localhost', 'root', '', 'nfldata')

    # print(">>> analysis_1(cursor)")
    # pprint(analysis_1(cursor))

    # print(">>> analysis_2(cursor)")
    # pprint(analysis_2(cursor))

    # print(">>> analysis_3(cursor)")
    # pprint(analysis_3(cursor))

    # print(">>> analysis_4(cursor)")
    # pprint(analysis_4(cursor))

    # print(">>> analysis_5(cursor)")
    # pprint(analysis_5(cursor))

    # pprint(visual_1(cursor))

    # pprint(visual_2(cursor))

    # pprint(visual_3(cursor))

    # pprint(summary_file1(cursor))

    # pprint(summary_file2(cursor))

if __name__ == '__main__':
    main()
