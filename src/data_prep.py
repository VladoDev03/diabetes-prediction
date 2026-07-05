import os
import zipfile
import re

import pandas as pd

from scipy.stats import mannwhitneyu
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import StandardScaler


def to_snake_case(col_name):
    col_name = col_name.strip()

    # insert underscore between a lowercase/digit and a following uppercase letter
    col_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", col_name)

    # insert underscore between consecutive uppercase letters followed by a lowercase letter (splits acronym+word boundaries
    col_name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", col_name)

    # insert underscore between a letter and a following digit, and vice versa
    col_name = re.sub(r"([a-zA-Z])([0-9])", r"\1_\2", col_name)
    col_name = re.sub(r"([0-9])([a-zA-Z])", r"\1_\2", col_name)

    col_name = col_name.lower()
    col_name = re.sub(r"[^\w\s]", "_", col_name)  # replace non-alphanumeric characters with underscores
    col_name = re.sub(r"\s+", "_", col_name)      # regex is used instead of replace to handle multiple spaces
    col_name = re.sub(r"_+", "_", col_name)       # replace multiple underscores with a single underscore
    col_name = col_name.rstrip("_")

    return col_name


def unzip_csv(zip_file_path, extract_to_folder):
    if not os.path.exists(zip_file_path):
        print(f"File {zip_file_path} not found.")
        return
    
    os.makedirs(extract_to_folder, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to_folder)
        
        extracted_files = zip_ref.namelist()
        print(f"Successfully extracted files: {", ".join(extracted_files)}")


def find_duplicates(df, subset=None):
    dup_mask = df.duplicated(subset=subset, keep=False)
    group_cols = subset or list(df.columns)
    duplicate_rows = df[dup_mask].sort_values(by=group_cols)

    n_duplicate_rows = df.duplicated(subset=subset, keep="first").sum()
    n_groups = duplicate_rows.groupby(group_cols).ngroups if not duplicate_rows.empty else 0

    summary = {
        "rows_involved_in_duplication": len(duplicate_rows),
        "duplicate_rows_to_remove": n_duplicate_rows,
        "percent_duplicated": round(n_duplicate_rows / len(df) * 100, 2),
        "unique_duplicate_groups": n_groups
    }

    print(f"Rows involved in duplication: {summary['rows_involved_in_duplication']}")
    print(f"Duplicate rows to remove: {summary['duplicate_rows_to_remove']} "f"({summary['percent_duplicated']}%)")
    print(f"Unique duplicate groups: {summary['unique_duplicate_groups']}")

    return duplicate_rows, summary, group_cols


def remove_duplicates(df):
    rows_before = len(df)
    df_clean = df.drop_duplicates(keep="first").reset_index(drop=True)
    rows_after = len(df_clean)

    print(f"Rows before: {rows_before}")
    print(f"Rows after: {rows_after}")
    print(f"Removed: {rows_before - rows_after}")

    return df_clean


def compare_groups_mannwhitney(df, group_col, features, group_a, group_b):
    """
    Runs a Mann-Whitney U test comparing two groups across multiple features,
    including a rank-biserial effect size (more informative than the raw
    p-value alone at large sample sizes, where nearly any difference
    becomes "statistically significant").
    """
    results = []

    for feature in features:
        a = df[df[group_col] == group_a][feature]
        b = df[df[group_col] == group_b][feature]

        stat, p_value = mannwhitneyu(a, b)
        effect_size = 1 - (2 * stat) / (len(a) * len(b))

        results.append({
            "feature": feature,
            "p_value": p_value,
            "effect_size": round(effect_size, 3)
        })

    return pd.DataFrame(results)


def compare_group_centroids(df, group_col, features, group_a, group_b, scaler=None):
    """
    Computes the Euclidean distance between the centroids (mean feature
    vectors) of two groups, using standardized features so that columns
    on different scales contribute comparably to the distance.
    """
    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[features])
    else:
        X_scaled = scaler.transform(df[features])

    X_scaled_df = pd.DataFrame(X_scaled, columns=features, index=df.index)

    centroid_a = X_scaled_df[df[group_col] == group_a].mean()
    centroid_b = X_scaled_df[df[group_col] == group_b].mean()

    return euclidean(centroid_a, centroid_b)
