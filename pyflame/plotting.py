import matplotlib.pyplot as plt
import numpy

def timeseries_plot(data, legends, title, linewidth=0.5, save_as_file=None, show=False):
    plt.clf()
    cmap = plt.get_cmap("tab10")
    for i in range(0, len(data)):
        for j in range(0,len(data[i])):
            if j==0:
                plt.plot(data[i][j], color=cmap(i), label=legends[i], linewidth=linewidth)
            else:
                plt.plot(data[i][j], color=cmap(i), label='__nolegend__', linewidth=linewidth)
    plt.title(title)
    plt.legend()
    if save_as_file is not None:
        plt.savefig(save_as_file + ".png")
    if show:
        plt.show()

    plt.close('all')

def histogram_plot(data, legends, title, plot_mean=True, bins=80, save_as_file=None, show=False):
    plt.clf()
    bins = numpy.linspace(numpy.amin(data), numpy.amax(data), bins)
    cmap = plt.get_cmap("tab10")
    for i in range(0, len(data)):
        plt.hist(data[i], bins, color=cmap(i), edgecolor='k', alpha=0.5, label=legends[i])
        if plot_mean:
            plt.axvline(numpy.mean(data[i]), color=cmap(i), linestyle='dashed', linewidth=2)
    plt.title(title)
    plt.legend()
    if save_as_file is not None:
        plt.savefig(save_as_file + ".png")
    if show:
        plt.show()

    plt.close('all')

def barchart_plot(data, legends, title, errors=None, save_as_file=None, show=False):
    plt.clf()

    no_sets = len(data)
    width = 0.8/no_sets
    ind = numpy.arange(len(data[0]))

    fig, ax = plt.subplots()

    for i in range(0, len(data)):
        if errors is not None:
            ax.bar(ind - i * width, data[i], width, label=legends[i], yerr=errors[i], ecolor='grey', error_kw=dict(lw=1))
        else:
            ax.bar(ind - i * width, data[i], width, label=legends[i])

    plt.title(title)
    plt.legend()

    ax.set_xticks(ind - width*(no_sets-1) / 2)
    ax.set_xticklabels(ind)

    if save_as_file is not None:
        plt.savefig(save_as_file + ".png")
    if show:
        plt.show()

    plt.close(fig)



