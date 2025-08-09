def calculate_fit_score(row, weights):
    return (
        (100 - row['Median_Home_Price'] / 10000) * weights['affordability'] +
        row['Walk_Score'] * weights['culture'] +
        row['Transit_Score'] * weights['transportation']
    ) / sum(weights.values())
