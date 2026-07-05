import matplotlib.pyplot as plt
import seaborn as sns


def plot_categorical_distribution(df, column, by_target=None, decimals=2):
    """
    Plots the distribution of a categorical column as a count bar chart with percentage labels. If by_target is provided, bars are split by that target variable instead of showing percentage labels.
    """
    n_categories = df[column].nunique()
    figsize = (max(5, n_categories * 1.2), 4)
    fig, ax = plt.subplots(figsize=figsize)

    if by_target:
        sns.countplot(x=column, hue=by_target, data=df, ax=ax)
        ax.set_title(f"{column} Distribution by {by_target}")
    else:
        counts = df[column].value_counts()
        percentages = df[column].value_counts(normalize=True) * 100

        sns.countplot(x=column, data=df, order=counts.index, ax=ax)

        ax.set_ylim(0, counts.max() * 1.15)

        for i, (count, pct) in enumerate(zip(counts, percentages)):
            ax.text(i, count, f"{count}\n({pct:.{decimals}f}%)", ha="center", va="bottom")

        ax.set_title(f"{column} Distribution")

    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    plt.tight_layout()

    plt.show()


def plot_numeric_distribution(df, column):
    plt.figure(figsize=(8, 5))
    
    sns.histplot(df[column], kde=True, color="skyblue")
    
    plt.title(f"Distribution of {column}", fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    
    plt.tight_layout()
    plt.show()

    print(f"Statistical Measures for {column}:")
    print(df[column].describe())


def plot_correlation_heatmap(df, title, columns=None, figsize=(14, 10)):
    plt.figure(figsize=figsize)

    if columns is None:
        columns = df.select_dtypes(include="number").columns

    sns.heatmap(
        df[columns].corr(method="spearman"),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )

    plt.title(title)
    plt.tight_layout()
    
    plt.show()
