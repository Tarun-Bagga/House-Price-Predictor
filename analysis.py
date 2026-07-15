import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

def load_data():
    df = pd.read_csv("data/house_prices.csv")
    return df

def explore_data(df):
    print("\n Dataset Shape: ")
    print(df.shape)

    print("\n Dataset Columns: ")
    print(df.columns.tolist())

    print("\n Data types: ")
    print(df.dtypes)

    print("\n First 5 rows: ")
    print(df.head(5))

    print("\n Summary Stats: ")
    print(df.describe())

    print("Missing values: ")
    print(df.isnull().sum())

    print("\n Duplicate Rows: ")
    print(df.duplicated().sum())

def plot_price_distillation(df):

    plt.figure(figsize = (10,6))
    plt.hist(df['price'], bins = 30, color = 'Green', edgecolor = 'black')

    plt.title("House Price Distribution", fontsize = 16, weight = 'bold')
    plt.xlabel("Price (Million)", fontsize = 12)
    plt.ylabel("Number of Houses", fontsize = 12)

    plt.gca().xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1_000_000:.1f}M" ))

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    plt.savefig(
        "images/charts/price_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def plot_correlation_heatmap(df):

    plt.figure(figsize = (10,8))
    numeric_df = df.select_dtypes(include=["int64", "float64"])

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="Reds",
        linewidths=0.5,
        fmt=".2f"
    )

    plt.title("Correlation Heatmap", fontsize = 16, weight = 'bold')
    plt.tight_layout()

    plt.savefig(
        "images/charts/correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def plot_price_vs_area(df):
    plt.figure(figsize = (10,6))

    plt.scatter(df['area'], df['price'],
                color="#E50914",
                alpha=0.7
                )

    plt.title("House Price vs. Area", fontsize = 16, weight = 'bold')
    plt.xlabel("Area(Square Feet)", fontsize = 12)
    plt.ylabel("Price (Million)", fontsize = 12)

    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1_000_000:.1f}M" )
    )

    plt.grid(alpha = 0.3)
    plt.tight_layout()
    plt.savefig("images/charts/price_vs_area.png",
                dpi=300,
                bbox_inches="tight")

    plt.show()

def plot_furnishing_status(df):
    plt.figure(figsize = (8,6))

    df.boxplot(column = 'price',
                by = 'furnishingstatus',
                grid = False)
    plt.title("House Price by Furnishing Status", fontsize = 16, weight = 'bold')
    plt.suptitle("")
    plt.xlabel("Furnishing Status", fontsize = 12)
    plt.ylabel("Price (Million)", fontsize = 12)
    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1_000_000:.1f}M" )
    )
    plt.tight_layout()
    plt.savefig(
        "images/charts/furnishing_status.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def main():
    df = load_data()
    explore_data(df)

    plot_price_distillation(df)
    plot_correlation_heatmap(df)
    plot_price_vs_area(df)
    plot_furnishing_status(df)

if __name__ == "__main__":
    main()