from constants import FIGSIZE, FONT, TDS, TDS1, GREY, DGREY
import folium
from math import pi
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

#######################
# COMMENTS ANALYSIS

def project_24h(value_counts_per_hour):
    """
        Value counts can miss an hour of the day if there is no
        occurence at this specific date.
        
        This method force to have 24 values, adding nan if no 
        occurence has been observed.
        
        NB: a column named 'hod' must contain the hour of the day [0;23]
    """

    hours = [i for i in range(24)]
    target = pd.DataFrame(hours, columns=["hod"])
    target = (
        target.merge(value_counts_per_hour.reset_index(), how="left", on="hod")
        .drop("hod", axis="columns")
        .fillna(0)
    )
    return target


def hours_polar_count(df):
    cycle = 24
    units = [i for i in range(cycle)]

    angles = [(n / float(cycle) * 2 * pi) for n in range(cycle)]
    angles += angles[:1]  # close loop

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    plt.xticks(angles[:-1], units, color=DGREY, size=10)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(40)

    plt.yticks(color=DGREY, size=12)

    values = list(project_24h(df).values)
    values += values[:1]
    ax.plot(angles, values, color=TDS)
    ax.fill(angles, values, TDS, alpha=0.1)

    ax.annotate(
        f"I commented {values[22][0]} times\n         at {units[22]}:00",
        (angles[22], values[22]),
        (angles[22], 225),
        size=14,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.2", color=TDS),
    )

    ax.set_frame_on(False)
    plt.grid(color=GREY)
    plt.title(
        "Number of comments per hour of the day", color=DGREY, fontdict=FONT, y=1.1
    )
    plt.show()

#######################
# GOOGLE TRENDS
    
def load_gtrends(file):
    df = pd.read_csv(file)
    df = df.assign(date=pd.to_datetime(df.Month))
    df = df.set_index('date').sort_index()
    df.drop('Month', axis='columns', inplace=True)
    return df
    
def google_trends(france, usa, world):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plt.plot(france.index, france.values, color=TDS, label='France')
    plt.plot(usa.index, usa.values, color=TDS, alpha=0.5, label='USA')
    plt.plot(world.index, world.values, color=TDS1, alpha=0.5, linestyle='--', label='World')

    plt.title("Facebook interest over time on Google", fontdict=FONT, y=1.2, color=DGREY)
    plt.ylabel("Interest (Google Trends metric)\n", fontdict=FONT, color=DGREY)
    plt.xticks(color=DGREY, size=12)
    plt.yticks(color=DGREY, size=12)

    ax.annotate(
        f"Like button created",
        (pd.to_datetime('2009-02'), 50),
        (pd.to_datetime('2006-02'), 70),
        size=14,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.2", color=DGREY),
    )

    ax.annotate(
        f"Facebook launched in Harvard",
        (pd.to_datetime('2004-02'), 0),
        (pd.to_datetime('2004-02'), 30),
        size=14,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY),
    )

    ax.annotate(
        f"1 billion users",
        (pd.to_datetime('2012-12'), 100),
        (pd.to_datetime('2013-10'), 110),
        size=14,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.2", color=TDS1),
    )

    ax.annotate(
        f"Basket Ball game created",
        (pd.to_datetime('2016-04'), 62),
        (pd.to_datetime('2014-10'), 85),
        size=14,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY),
    )

    ax.tick_params(color='#fff', direction="out", length=8)
    plt.grid(True)
    ax.set_frame_on(False)
    ax.set_axisbelow(True)
    ax.grid(axis="both", alpha=.5)
    plt.legend(prop={"size": FONT["size"]})
    plt.show()
    

def world_proportions():
    # values are in billions, found on google
    world_pop = 7.6
    internet_pop = 3.2 / world_pop
    facebook_pop = 1.7 / world_pop
    world_pop /= world_pop

    fig, ax = plt.subplots(figsize=FIGSIZE)
    height = .2
    init = .1
    space = .03

    for i, v in enumerate([world_pop, internet_pop, facebook_pop]):
        rectm = patches.Rectangle((init, 0.7 - 0.2*i), v*.8, 0.1, facecolor=TDS, alpha=1-i*0.3, fill=True)
        ax.add_patch(rectm)

    plt.tick_params(
    bottom=False, left=False, labelleft=False, labelbottom=False) #
    ax.set_frame_on(False)
    ax.set_axisbelow(True)
    plt.title("Humans vs People w/ Internet vs Facebook daily active users", fontdict=FONT, color=DGREY)
    plt.show()
    
    
def location_activities(gps, city_count):
    connection_map = folium.Map(location=[52, 2],
               tiles='cartodbpositron',
              zoom_start=5)

    for location in gps:
        count: int = int(city_count.loc[location['name']])
        folium.Circle(
            radius=count*10,
            location=location['coords'],
            popup=f"{location['name']}\n{count} actions",
            color=TDS,
            fill=False,
        ).add_to(connection_map)
    
    return connection_map