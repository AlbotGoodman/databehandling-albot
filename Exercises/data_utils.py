import matplotlib.pyplot as plt
import seaborn as sns

def barplot(df):
    df = df.isna().sum()
    df = df[df != 0]
    pal = sns.color_palette("viridis", len(df)) # len as to not repeat colours
    sns.barplot(x=df.index, y=df.values, palette=pal, hue=df.index, legend=False)
    plt.title("All columns with NaN\n", fontweight="bold")


