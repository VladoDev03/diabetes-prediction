import os
import zipfile

def test():
    print("Test function in data_prep.py is working correctly.")


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
