import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(font_scale=1.5, style="darkgrid")

data = pd.read_csv("./data.csv", usecols=["date", "new"], parse_dates=["date"])
data["day"] = data["date"].dt.strftime("%A")
data["digit"] = data["date"].dt.strftime("%w")
data = data[data["date"] > pd.to_datetime("2021-08-15")]

fig, ax = plt.subplots(
    figsize=(12, 6.75),
    tight_layout=True
)
sns.barplot(
    data=data.groupby(["day", "digit"]).mean().reset_index().sort_values("digit"),
    x="new",
    y="day",
    ax=ax
)
plt.xlabel(None)
plt.ylabel(None)
ax.set_title(
    "Average cases per weekday",
    fontsize=20,
    fontweight="bold"
)
plt.savefig("day_of_week.png")
plt.show()
