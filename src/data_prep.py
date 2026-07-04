import os
import zipfile
import re

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

    print(f"Rows involved in duplication: {summary["rows_involved_in_duplication"]}")
    print(f"Duplicate rows to remove: {summary["duplicate_rows_to_remove"]} "f"({summary["percent_duplicated"]}%)")
    print(f"Unique duplicate groups: {summary["unique_duplicate_groups"]}")

    return duplicate_rows, summary, group_cols


def remove_duplicates(df):
    rows_before = len(df)
    df_clean = df.drop_duplicates(keep="first").reset_index(drop=True)
    rows_after = len(df_clean)

    print(f"Rows before: {rows_before}")
    print(f"Rows after: {rows_after}")
    print(f"Removed: {rows_before - rows_after}")

    return df_clean
