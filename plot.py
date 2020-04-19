"""Plot data from the 10ft challenge."""

import itertools

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Set the plot font sizes.
plt.rc("font", size=18)
plt.rc("axes", titlesize=22)
plt.rc("axes", labelsize=20)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=18)
plt.rc("legend", fontsize=16)
plt.rc("figure", titlesize=32)


class Player(object):
    """Encapsulate data from one player."""

    def __init__(self, csv_row):
        """Parse a CSV row."""
        entities = csv_row.split(",")
        self.name = entities[0]
        if entities[1] != "":
            self.starts_throwing_at = int(entities[1])
        else:
            self.starts_throwing_at = None
        # Parse the timing data.  Each value is of the form "59:54" or "44:01" which is
        # how much time is *remaining* when they made the shot.  We'll invert that to be
        # the time that had elapsed.
        self.times = []
        self.distances = []
        for index, value in enumerate(entities[2:]):
            if not value:
                continue
            seconds_remaining = 60 * int(value.split(":")[0]) + int(value.split(":")[1])
            self.times.append(60 * 60 - seconds_remaining)
            self.distances.append(10 * (index + 1))


# Parse the datafile.
players = []
with open("data.csv") as datafile:
    for line in datafile.readlines():
        if line.startswith("#"):
            continue
        players.append(Player(line.strip()))

# Plot, starting with a faint background line.
figure, axis = plt.subplots()
for player in players:
    axis.step(
        player.times,
        player.distances,
        "--",
        label=None,
        linewidth=1,
        color="#cccccc",
        where="post",
    )

# Then plot the markers on top.
markerstyles = itertools.cycle(("o", "x", "+", "*", "^", "d", ">", "<", "s"))
for player in players:
    marker = next(markerstyles)
    if marker in ("+", "x"):
        edge_width = 2
    else:
        edge_width = 1
    axis.step(
        player.times,
        player.distances,
        marker=marker,
        label=player.name,
        linewidth=0,
        markersize=10,
        markeredgewidth=edge_width,
        where="post",
    )

# Then circle the transition from putting -> throwing.
for player in players:
    if player.starts_throwing_at:
        index = player.distances.index(player.starts_throwing_at)
        axis.step(
            player.times[index],
            player.starts_throwing_at,
            marker="o",
            label=None,
            linewidth=1,
            markersize=20,
            markeredgewidth=1,
            fillstyle='none',
            color="#cccccc",
            where="post",
        )

# Finally plot one more entry as a hack to update the legend with some explanatory text.
axis.step(
    [],
    [],
    'o',
    label="Player starts throwing",
    linewidth=1,
    markersize=20,
    markeredgewidth=1,
    fillstyle='none',
    color="#cccccc",
)


# Format.
axis.set(
    ylabel="distance (ft)",
    title="Simon's 10ft, 1hr Challenge",
)
formatter = matplotlib.ticker.FuncFormatter(
    lambda s, x: "{:d}min".format(int(s / 60))
)
axis.xaxis.set_major_formatter(formatter)
tick_spacing = 10 * 60
axis.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
axis.yaxis.set_ticks(range(0, 200, 20))
axis.legend()

# Save.
figure.set_size_inches(16, 10)
figure.savefig("/tmp/out.png")
