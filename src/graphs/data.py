import pandas as pd

from src.graphs.style import INPUT_CSV, GRADES


def load_chart_data(line_metrics, rating_metric=None):
    data = pd.read_csv(INPUT_CSV)
    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data["team_count"] = pd.to_numeric(data["team_count"], errors="coerce")

    team_totals = data.groupby("year")["team_count"].sum()
    years = list(team_totals.index)

    line_values = {}
    for metric in line_metrics:
        data[metric] = pd.to_numeric(data[metric], errors="coerce").fillna(0)
        weighted_total = (data[metric] * data["team_count"]).groupby(data["year"]).sum()
        line_values[metric] = list(weighted_total / team_totals)

    rating_counts = None
    if rating_metric is not None:
        rating_columns = [f"{rating_metric}_{grade}" for grade in GRADES]
        data[rating_columns] = data[rating_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
        rating_data = data.groupby("year")[rating_columns].sum()
        yearly_totals = rating_data.sum(axis=1).replace(0, 1)
        rating_counts = {
            grade: list(rating_data[f"{rating_metric}_{grade}"] / yearly_totals * 100)
            for grade in GRADES
        }

    return years, line_values, rating_counts
