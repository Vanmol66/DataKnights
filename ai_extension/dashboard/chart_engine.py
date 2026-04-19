def recommend_charts(df):
    recommendations = []

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # Bar chart
    if cat_cols and num_cols:
        recommendations.append({
            "type": "bar",
            "x": cat_cols[0],
            "y": num_cols[0],
            "title": f"{num_cols[0]} by {cat_cols[0]}"
        })

    # Histogram
    if num_cols:
        recommendations.append({
            "type": "hist",
            "x": num_cols[0],
            "title": f"Distribution of {num_cols[0]}"
        })

    # Scatter
    if len(num_cols) >= 2:
        recommendations.append({
            "type": "scatter",
            "x": num_cols[0],
            "y": num_cols[1],
            "title": f"{num_cols[0]} vs {num_cols[1]}"
        })

    return recommendations