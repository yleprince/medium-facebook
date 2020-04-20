from constants import FIGSIZE, FONT, TDS, TDS1, GREY, DGREY
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd


week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def week_processing(tmp):
    tmp = tmp.resample("D").sum()
    tmp = tmp.assign(dow=tmp.index.dayofweek.values).sort_values("dow")
    return tmp.assign(dow_str=tmp.dow.apply(lambda d: week[d]))

def gender_ratio(men, women, others=0):
    total = men + women + others
    width = .8
    
    m_w = men * width / total
    f_w = women * width / total
    o_w = 8 * width / total
    
    height = .2
    init = .1
    space = .03

    fig, ax = plt.subplots(figsize=FIGSIZE)
    rectm = patches.Rectangle((init - space,.3), m_w,height,facecolor=TDS, alpha=.5, fill=True)
    rectf = patches.Rectangle((init + m_w,.3), f_w,height,facecolor=TDS, fill=True)
    recto = patches.Rectangle((init + + space + m_w + f_w,.3), o_w,height,facecolor=DGREY, fill=True)
    ax.add_patch(rectm)
    ax.add_patch(rectf)
    ax.add_patch(recto)

    ax.annotate(
        f"  Men",
        (init - space + m_w/2, .51),
        (.4, .6),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.2", color=DGREY, alpha=.7),
    )

    ax.annotate(
        f"Women  ",
        (init + m_w + f_w / 2, .51),
        (.6, .6),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY, alpha=.7),
    )
    ax.annotate(
        f"Others",
        (init + space + m_w + f_w + o_w / 2, .51),
        (.8, .6),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY, alpha=.7),
    )
    plt.tick_params(
    bottom=False, left=False, labelleft=False, labelbottom=False) #
    ax.set_frame_on(False)
    ax.set_axisbelow(True)
    plt.show()
    
def friends_cumsum_by_gender(friends):
    fig, ax = plt.subplots(figsize=FIGSIZE)

    cs_males = friends.male.cumsum()
    cs_females = friends.female.cumsum()
    cs_others = friends.apply(lambda r: not(r.male or r.female), axis=1).cumsum()

    ax.annotate(
        f"1st Engineering school",
        (pd.to_datetime('09-01-2014'), 250),
        (pd.to_datetime('06-01-2011'), 320),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY, alpha=.7),
    )

    ax.annotate(
        f"2nd Engineering school",
        (pd.to_datetime('09-15-2017'), 410),
        (pd.to_datetime('01-01-2014'), 460),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY, alpha=.7),
    )

    ax.annotate(
        f" Prep. school 2nd year",
        (pd.to_datetime('09-15-2013'), 170),
        (pd.to_datetime('10-01-2014'), 110),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", color=DGREY, alpha=.7),
    )

    ax.annotate(
        "Preparatory school 1st year",
        (pd.to_datetime('09-15-2012'), 120),
        (pd.to_datetime('10-01-2012'), 30),
        size=16,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-.2", color=DGREY, alpha=.7),
    )

    plt.plot(cs_males.index, cs_males.values, c=TDS, alpha=.5, label="Men")
    plt.plot(cs_females.index, cs_females.values, c=TDS, label="Women")
    plt.plot(cs_others.index, cs_others.values, c=DGREY, label="Others")

    plt.title(
        "Facebook friends evolution (cumulated) by gender", 
        color=DGREY,
        fontdict=FONT, y=1.2
    )
    plt.xticks(color=DGREY, size=12)
    plt.yticks(color=DGREY, size=12)
    plt.ylabel("Nb friends\n", fontdict=FONT, color=DGREY)
    ax.tick_params(color='#fff', direction="out", length=8)
    ax.set_frame_on(False)
    ax.grid(axis="both", alpha=.5)
    plt.grid(True)
    plt.legend(prop={"size": FONT["size"]})
    plt.show()
    
def bar_name(df):
    males = df[df.male].fname.unique()
    fnames = df.fname.value_counts().head(30)
    names = fnames.index.values
    fnames = fnames.reset_index()

    fig, ax = plt.subplots(figsize=FIGSIZE)
    mask_males = fnames["index"].isin(males)

    plt.bar(
        x=fnames[mask_males].index,
        height=fnames[mask_males].fname,
        color=TDS,
        alpha=.5,
        label="Male",
    )
    plt.bar(
        x=fnames[~mask_males].index,
        height=fnames[~mask_males].fname,
        color=TDS,
        label="Female",
    )

    plt.title("First Names distribution", fontdict=FONT, color=DGREY, y=1.2)
    longest = fnames["index"].apply(lambda s : len(s)).max()
    tick_labels = fnames["index"]\
            .apply(lambda s : s.capitalize().rjust(longest))
    plt.xticks(
        [i - .4 for i in fnames.index],
        tick_labels,
        rotation=65,
        ha="center",
        size=FONT["size"],
    )
    plt.ylabel("Nb occurences\n", fontdict=FONT, color=DGREY)
    plt.yticks([5, 10, 15])
    ax.tick_params(color='#fff', direction="out")

    ax.set_frame_on(False)
    plt.grid(True)
    plt.legend(prop={"size": FONT["size"]})
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0)
    ax.grid(axis="y", alpha=.5)
    plt.show()

def bar_added(full, scaled=False):
    width = .55

    fig, ax = plt.subplots(figsize=(8,5))
    plt.grid(True)
    bars = full[['added', 'dow']].groupby('dow').sum()
    if scaled:
        bars = bars / bars.sum()
    plt.bar(
            x=bars.index,
            height=bars.added,
            color=TDS,
            alpha=.5,
            width=width
        )

    plt.xticks(
        bars.index,
        week,
        ha="center",
        color=DGREY,
        alpha=.9,
        size=FONT["size"],
    )
    if scaled:
        plt.yticks(
            [.05, .1, .15, .2],
            ['5%', '10%', '15%', '20%'],
            color=DGREY)
    plt.ylabel(f"{'%'*scaled}{'nb'*(1-scaled)} Friends added\n",
              fontdict=FONT,
              color=DGREY)
    ax.set_frame_on(False)
    ax.grid(axis="x", alpha=0)
    ax.grid(axis="y", alpha=.5)
    ax.set_axisbelow(True)
    ax.tick_params(color='#fff', direction="out", length=16)
    plt.show()

def bar_added_gender(males, females, scaled=False):
    width = .25

    fig, ax = plt.subplots(figsize=(12,5))
    plt.grid(True)
    bars = males[['added', 'dow']].groupby('dow').sum()
    if scaled:
        bars = bars / bars.sum()
    plt.bar(
            x=[int(i) - width / 2 for i in bars.index],
            height=bars.added,
            color=TDS,
            alpha=.5,
            label="Men",
            width=width
        )

    bars = females[['added', 'dow']].groupby('dow').sum()
    if scaled:
        bars = bars / bars.sum()
    plt.bar(
            x=[int(i) + width / 2 for i in bars.index],
            height=bars.added,
            color=TDS,
            label="Women",
            width=width
        )

    plt.xticks(
        bars.index,
        week,
        ha="center",
        color=DGREY,
        alpha=.9,
        size=FONT["size"],
    )
    if scaled:
        plt.yticks(
            [.05, .1, .15, .2],
            ['5%', '10%', '15%', '20%'],
            color=DGREY)
    plt.ylabel(f"{'%' * scaled}{'nb' * (1 - scaled)} Friends added\n",
              fontdict=FONT,
              color=DGREY)
    ax.tick_params(color='#fff', direction="out", length=16)

    ax.set_frame_on(False)
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0)
    ax.grid(axis="y", alpha=.5)
    plt.legend(prop={"size": FONT["size"]})
    plt.show()