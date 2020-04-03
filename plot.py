"""Plot data from the 10ft challenge."""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Set the plot's font sizes.
plt.rc("font", size=18)
plt.rc("axes", titlesize=22)
plt.rc("axes", labelsize=20)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=18)
plt.rc("legend", fontsize=16)
plt.rc("figure", titlesize=32)


class Player(object):
    """Data from one player."""

    def __init__(self, csv_row):
        """Parse a CSV row."""
        entities = csv_row.split(",")
        self.name = entities[0]
        self.starts_throwing_at = entities[1]
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

# Plot.
figure, axis = plt.subplots()
for p in players:
    axis.plot(p.times, p.distances, label=p.name)

# Format.
axis.set(
    ylabel="distance (ft)",
    title="Simon's 10ft, 1hr Challenge",
)
axis.grid(linestyle=":")
axis.legend()
formatter = matplotlib.ticker.FuncFormatter(
    lambda s, x: "{:d}min".format(int(s / 60))
)
axis.xaxis.set_major_formatter(formatter)
tick_spacing = 10 * 60
axis.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

# Save.
figure.set_size_inches(16, 10)
figure.savefig("/tmp/out.png")
