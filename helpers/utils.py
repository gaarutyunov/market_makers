import matplotlib.pyplot as plt
import numpy as np
from main import MAIN, GRAPH_PATH
import os


def group(df, rename=True):
    tp = df.iloc[0, 2] if rename else 'Все ценные бумаги'
    bt = df[['Тип ценной бумаги', 'liquidity']]\
        .rename(index=str, columns={'liquidity': 'Ликвидность', 'Тип ценной бумаги': tp})
    return bt.groupby('Ликвидность').count().rename(index={'l': 'Ликвидные', 'nl': 'Низколиквидные'})


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{p:.2f}%\n({v:d})".format(p=float(pct), v=absolute)


def create_pie(dt_f):
    title = dt_f.columns.values[0]
    labels = [dt_f.index[i] for i in range(0, len(dt_f))]
    values = dt_f.values
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: func(pct, values),
                                      textprops=dict(color="w"))
    ax.legend(wedges, labels,
              title="Ликвидность",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(title)
    plt.setp(autotexts, size=8, weight="bold")
    plt.savefig(os.path.join(GRAPH_PATH, title + '.png'))


def create_plot(dt_f, title, div):
    df = dt_f.divide(div)
    indexes = df.index.values[::5]
    ax = df.plot(figsize=(30, 20))
    plt.xlabel('Дата', fontsize=12)
    start_x, end_x = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(0, end_x, div / 100 if div == 1000 else div * 25000))
    start_y, end_y = ax.get_xlim()
    plt.xticks(list(range(len(indexes))), indexes)
    ax.xaxis.set_ticks(np.arange(0, end_y, 5))
    plt.yticks(fontsize=12)
    plt.ylabel('Объем, тыс шт. ценных бумаг' if div == 1000 else 'Объем, шт. ценных бумаг', fontsize=12)
    ax.set_title(title)
    title = title.replace(' ', '_').replace('/', '_')
    # plt.show()
    plt.savefig(os.path.join(GRAPH_PATH, title + '.png'))
