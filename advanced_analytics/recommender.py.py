import pandas as pd

# Load the dataset
performance = pd.read_csv("07_scheme_performance.csv")

# Get user input
risk = input("Enter Risk Appetite (Low/Moderate/High): ")

# Filter funds based on risk
recommended = performance[
    performance["risk_grade"].str.lower() == risk.lower()
]

# Sort by Sharpe Ratio
recommended = recommended.sort_values(
    by="sharpe_ratio",
    ascending=False
)

# Select Top 3
top3 = recommended.head(3)

# Display recommendations
print("\nTop 3 Recommended Funds:\n")
print(
    top3[
        [
            "scheme_name",
            "risk_grade",
            "sharpe_ratio",
            "return_3yr_pct",
            "morningstar_rating"
        ]
    ]
)