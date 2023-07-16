import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = plt.barh(x, y, color='cornflowerblue')
    ax.spines[['right', 'top', 'left']].set_visible(False)
    ax.bar_label(bars, padding=5, color='grey',
             fontsize=8,
            fontweight='bold', fontname='serif')
    ax.axvline(x=100, zorder=0, color='grey', ls='--', lw=1)
    plt.xticks(fontname='serif', fontsize=8)
    plt.yticks(fontname='serif', fontsize=8)
    #plt.xlim(0, 150)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_cityplot(x, y):
    plt.switch_backend('AGG')
    colors = ['gold', 'cornflowerblue', 'orchid']
    fig, ax = plt.subplots(figsize=(4, 4))
    bars = plt.bar(x, y, color = colors)
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    ax.bar_label(bars, padding=3, color='grey',
                 fontsize=8,
                 fontweight='bold', fontname='serif')
    plt.xticks(fontname='serif', fontsize=8)
    plt.yticks(fontname='serif', fontsize=8)
    plt.tight_layout()
    graph = get_graph()
    return graph
