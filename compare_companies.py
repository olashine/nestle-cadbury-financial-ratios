# Nestle Nigeria vs Cadbury Nigeria: Financial Ratio Comparison
# Data sources (all amounts in thousands of naira):
#   Nestle Nigeria PLC annual reports for 2022, 2023 and 2025 (covers 2021-2025)
#   Cadbury Nigeria PLC annual reports for 2024 and 2025 (covers 2023-2025; the 2023
#   figures are the RESTATED ones shown in the 2024 report)
# Note: ROE and Debt-to-Equity are left out because both companies had very small
# or negative equity in some years, which makes those two ratios misleading.

# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
df_nestle = pd.read_csv("nestle_financials.csv")
df_cadbury = pd.read_csv("cadbury_financials.csv")

print("--- Nestle data ---")
print(df_nestle.head())
print("\n--- Cadbury data ---")
print(df_cadbury.head())

# 2. A reusable function (DRY principle): calculate all ratios for ONE company
def calculate_ratios(df):
    df = df.copy()

    # Liquidity: can the company pay its short-term bills?
    df["Current_Ratio"] = df["Current_Assets"] / df["Current_Liabilities"]
    df["Quick_Ratio"] = (df["Current_Assets"] - df["Inventory"]) / df["Current_Liabilities"]

    # Profitability: how much profit is the company making?
    df["Gross_Margin"] = df["Gross_Profit"] / df["Revenue"] * 100
    df["Net_Margin"] = df["Net_Income"] / df["Revenue"] * 100
    df["ROA"] = df["Net_Income"] / df["Total_Assets"] * 100

    # Leverage: how much does the company depend on debt?
    df["Debt_Ratio"] = df["Total_Liabilities"] / df["Total_Assets"]

    # Efficiency: how well does the company use its assets to make sales?
    df["Asset_Turnover"] = df["Revenue"] / df["Total_Assets"]

    return df

# 3. Use the function on both companies
ratio_columns = ["Year", "Current_Ratio", "Quick_Ratio", "Gross_Margin", "Net_Margin",
                 "ROA", "Debt_Ratio", "Asset_Turnover"]

nestle_ratios = calculate_ratios(df_nestle)[ratio_columns].round(2)
cadbury_ratios = calculate_ratios(df_cadbury)[ratio_columns].round(2)

print("\n--- Nestle Ratios (2021-2025) ---")
print(nestle_ratios)
print("\n--- Cadbury Ratios (2023-2025) ---")
print(cadbury_ratios)

# 4. Merge the two tables on Year (inner merge keeps only years both companies have)
comparison = pd.merge(nestle_ratios, cadbury_ratios, on="Year", how="inner",
                      suffixes=("_Nestle", "_Cadbury"))

# .T flips the table (rows become columns) so it is easier to read
print("\n--- Side-by-Side Comparison (2023 to 2025) ---")
print(comparison.T)

# 5. Save the results
nestle_ratios.to_csv("nestle_ratios.csv", index=False)
cadbury_ratios.to_csv("cadbury_ratios.csv", index=False)
comparison.to_csv("comparison_2023_2025.csv", index=False)

# 6. Visualize the story
# Figure 1: Net Margin and Current Ratio
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(nestle_ratios["Year"], nestle_ratios["Net_Margin"], marker="o", color="navy", label="Nestle")
axes[0].plot(cadbury_ratios["Year"], cadbury_ratios["Net_Margin"], marker="s", color="darkorange", label="Cadbury")
axes[0].set_title("Net Margin (%)", fontweight="bold")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Percent (%)")
axes[0].set_xticks(nestle_ratios["Year"])
axes[0].legend()
axes[0].grid(True, linestyle="--", alpha=0.6)

axes[1].plot(nestle_ratios["Year"], nestle_ratios["Current_Ratio"], marker="o", color="navy", label="Nestle")
axes[1].plot(cadbury_ratios["Year"], cadbury_ratios["Current_Ratio"], marker="s", color="darkorange", label="Cadbury")
axes[1].set_title("Current Ratio", fontweight="bold")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Ratio")
axes[1].set_xticks(nestle_ratios["Year"])
axes[1].legend()
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("comparison_chart_1.png")
plt.show()

# Figure 2: Gross Margin and Asset Turnover
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(nestle_ratios["Year"], nestle_ratios["Gross_Margin"], marker="o", color="navy", label="Nestle")
axes[0].plot(cadbury_ratios["Year"], cadbury_ratios["Gross_Margin"], marker="s", color="darkorange", label="Cadbury")
axes[0].set_title("Gross Margin (%)", fontweight="bold")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Percent (%)")
axes[0].set_xticks(nestle_ratios["Year"])
axes[0].legend()
axes[0].grid(True, linestyle="--", alpha=0.6)

axes[1].plot(nestle_ratios["Year"], nestle_ratios["Asset_Turnover"], marker="o", color="navy", label="Nestle")
axes[1].plot(cadbury_ratios["Year"], cadbury_ratios["Asset_Turnover"], marker="s", color="darkorange", label="Cadbury")
axes[1].set_title("Asset Turnover", fontweight="bold")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Ratio")
axes[1].set_xticks(nestle_ratios["Year"])
axes[1].legend()
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("comparison_chart_2.png")
plt.show()

# Explanation:
# I wrote one function that calculates every ratio then used it on both companies
# instead of repeating the same code twice. pd.merge() joined the two ratio tables on
# Year so we could compare them side by side. Cadbury only has 2023-2025, so its lines
# are shorter than Nestle's 5-year lines on the charts.
