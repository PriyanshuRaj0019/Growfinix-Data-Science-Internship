# Project 1 — Real Estate Exploratory Data Analysis

## Business problem
A property analytics team receives an unreliable listing file. The objective is to convert it into analysis-ready data and identify how property prices vary by neighborhood and size.

## What you practice
Pandas cleaning, missing-value strategy, duplicates, validity rules, IQR outlier detection, feature engineering, groupby analysis, Matplotlib and Seaborn.

## Step-by-step
1. Load `data/properties_messy.csv` and inspect `head`, `shape`, `dtypes`, missing values and duplicates.
2. Standardize column names and categorical text.
3. Convert expected numeric columns with `errors='coerce'`.
4. Turn impossible values into missing values rather than treating them as valid observations.
5. Impute `price` and `area_sqft` using neighborhood medians; use robust medians for other numeric fields.
6. Remove duplicate property IDs.
7. Detect price outliers with the IQR rule and keep a `price_outlier` flag so the analyst can decide whether to include them.
8. Create `price_per_sqft` and property `size_band`.
9. Compare neighborhoods using median price and median price per square foot.
10. Build price histogram, neighborhood box plot, size-vs-price scatter plot and correlation heatmap.
11. Export the cleaned dataset and neighborhood summary.

## Run
```bash
python src/eda.py
```

## Deliverables
- `outputs/properties_clean.csv`
- `outputs/neighborhood_summary.csv`
- four analysis charts

## Interview explanation
“I first profiled data quality, standardized the schema, validated numerical ranges and used robust median imputation. I did not automatically delete expensive properties; I flagged IQR outliers because they may be legitimate luxury listings. I then engineered price per square foot and size bands to make neighborhood comparisons more meaningful.”

## Improvements
Use geospatial features, inflation-adjusted prices, multivariate outlier detection, automated data-quality tests, or a regression model.
