import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def check_float_binary_columns(df, binary=True, continuous=True):
    """ 
    Identifies float64 columns that contain only binary values (0.0 and 1.0)
    or continuous/other numerical data, based on the provided flags.
    """
    if not binary and not continuous:
        raise ValueError("At least one of 'binary' or 'continuous' must be set to True.")
    
    float64_cols = df.select_dtypes(include=['float64']).columns
    
    binary_cols = []
    other_cols = []
    
    for col in float64_cols:
        unique_vals = set(df[col].dropna().unique())
        
        # Determine if the column is binary
        is_binary = unique_vals.issubset({0.0, 1.0})
        
        # Append to respective lists only if the corresponding flag is True
        if is_binary and binary:
            binary_cols.append(col)
        elif not is_binary and continuous:
            other_cols.append(col)
    
    return binary_cols, other_cols


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
    """
    Plots a Spearman correlation heatmap for the given columns, or for all
    numeric columns in the DataFrame if none are specified.
    """
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
    

def plot_group_means_heatmap(df, group_col, features, decimals=2):
    """
    Plots a heatmap comparing the mean value of each feature across the
    groups of a categorical/ordinal column (e.g. diabetes_012 classes).
    Each row is normalized independently (min-max) for color intensity,
    so features on very different scales (e.g. age vs a 0/1 flag) remain
    visually comparable, while the actual mean values are still annotated.
    """
    means = df.groupby(group_col)[features].mean().T

    normalized = means.sub(means.min(axis=1), axis=0).div(
        means.max(axis=1) - means.min(axis=1), axis=0
    )

    fig, ax = plt.subplots(figsize=(1.5 * len(means.columns) + 2, 0.5 * len(features) + 2))
    sns.heatmap(normalized, annot=means.round(decimals), fmt=f".{decimals}f",
                cmap="coolwarm", cbar=False, linewidths=0.5, ax=ax)

    ax.set_title(f"Feature Means by {group_col}")
    ax.set_xlabel(group_col)
    ax.set_ylabel("")
    plt.tight_layout()
    
    plt.show()


def plot_effect_size_comparison(comparison_df, feature_col="feature",
                                 effect_col_a="effect_size_vs_0",
                                 effect_col_b="effect_size_vs_2",
                                 label_a="vs. no diabetes", label_b="vs. diabetes"):
    """
    Plots a grouped bar chart comparing the signed effect size of a "middle"
    group against two reference groups. Signed values are preserved (not
    absolute) so that direction reversals are visible: for a feature that
    increases monotonically across three ordered groups, the two effect
    sizes are expected to have opposite signs.
    """
    df = comparison_df.copy()
    x = range(len(df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(max(6, len(df) * 1.2), 5))
    ax.bar([i - width / 2 for i in x], df[effect_col_a], width, label=label_a)
    ax.bar([i + width / 2 for i in x], df[effect_col_b], width, label=label_b)
    ax.axhline(0, color="black", linewidth=0.8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df[feature_col], rotation=30, ha="right")
    ax.set_ylabel("Effect size (signed)")
    ax.set_title("Effect Size Direction and Magnitude - Prediabetes vs. Each Reference Group")
    ax.legend()
    plt.tight_layout()
    
    plt.show()


def plot_centroid_distances(distances, title="Centroid Distance Comparison"):
    """
    Plots a simple bar chart comparing centroid distances between group pairs.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(distances.keys(), distances.values(), color=["#4C72B0", "#C44E52"])

    for bar, value in zip(bars, distances.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{value:.3f}", ha="center", va="bottom")

    ax.set_ylabel("Euclidean distance (standardized features)")
    ax.set_title(title)
    plt.tight_layout()

    plt.show()
