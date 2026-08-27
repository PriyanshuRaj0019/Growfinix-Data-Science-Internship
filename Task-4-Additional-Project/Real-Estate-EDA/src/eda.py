from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "properties_messy.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data(path=DATA_PATH):
    return pd.read_csv(path)


def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Standardize text
    for col in ["neighborhood", "property_type"]:
        df[col] = df[col].astype("string").str.strip().str.title()

    # Convert numeric columns safely
    numeric_cols = ["price", "area_sqft", "bedrooms", "bathrooms", "age_years"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove impossible values first
    df.loc[df["price"] <= 0, "price"] = np.nan
    df.loc[df["area_sqft"] <= 100, "area_sqft"] = np.nan
    df.loc[~df["bedrooms"].between(1, 8), "bedrooms"] = np.nan
    df.loc[~df["bathrooms"].between(1, 8), "bathrooms"] = np.nan
    df.loc[df["age_years"] < 0, "age_years"] = np.nan

    # Fill missing categorical values with mode
    for col in ["neighborhood", "property_type"]:
        df[col] = df[col].fillna(df[col].mode().iloc[0])

    # Fill numeric values with neighborhood median where meaningful
    for col in ["price", "area_sqft"]:
        df[col] = df[col].fillna(df.groupby("neighborhood")[col].transform("median"))
        df[col] = df[col].fillna(df[col].median())

    for col in ["bedrooms", "bathrooms", "age_years"]:
        df[col] = df[col].fillna(df[col].median())

    # Remove duplicate property IDs
    df = df.drop_duplicates(subset="property_id", keep="first")

    # Flag outliers with IQR instead of silently deleting them
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df["price_outlier"] = ~df["price"].between(lower, upper)

    # Business-friendly engineered metrics
    df["price_per_sqft"] = df["price"] / df["area_sqft"]
    df["size_band"] = pd.cut(
        df["area_sqft"],
        bins=[0, 800, 1400, 2200, np.inf],
        labels=["Small", "Medium", "Large", "Very Large"],
    )
    return df


def save_summary(df):
    summary = (
        df.groupby("neighborhood", as_index=False)
        .agg(
            listings=("property_id", "count"),
            median_price=("price", "median"),
            median_area_sqft=("area_sqft", "median"),
            median_price_per_sqft=("price_per_sqft", "median"),
        )
        .sort_values("median_price", ascending=False)
    )
    summary.to_csv(OUTPUT_DIR / "neighborhood_summary.csv", index=False)
    return summary


def make_charts(df):
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(9, 5))
    plt.hist(df.loc[~df["price_outlier"], "price"].dropna(), bins=30)
    plt.title("Property Price Distribution")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "price_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    order = df.groupby("neighborhood")["price"].median().sort_values().index
    sns.boxplot(data=df, x="neighborhood", y="price", order=order)
    plt.xticks(rotation=30, ha="right")
    plt.title("Price Distribution by Neighborhood")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "price_by_neighborhood.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="area_sqft", y="price", hue="neighborhood", alpha=0.7)
    plt.title("Property Size vs Price")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "size_vs_price.png", dpi=160)
    plt.close()

    numeric = df[["price", "area_sqft", "bedrooms", "bathrooms", "age_years", "price_per_sqft"]]
    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_matrix.png", dpi=160)
    plt.close()


def main():
    raw = load_data()
    print("Raw shape:", raw.shape)
    print("Missing values before cleaning:\n", raw.isna().sum())

    clean = clean_data(raw)
    clean.to_csv(OUTPUT_DIR / "properties_clean.csv", index=False)
    summary = save_summary(clean)
    make_charts(clean)

    print("\nClean shape:", clean.shape)
    print("\nNeighborhood summary:\n", summary.to_string(index=False))
    print(f"\nOutliers flagged: {clean['price_outlier'].sum()}")


if __name__ == "__main__":
    main()
