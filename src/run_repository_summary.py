from src.aggregate_repository_metrics import (
    build_repository_summary,
    save_repository_summary_csv,
    save_repository_summary_json,
)


REPOSITORY = (
    "project-4-direct-geo-referencing"
)


if __name__ == "__main__":
    summary = build_repository_summary(
        repository=REPOSITORY,
    )

    csv_path = save_repository_summary_csv(
        repository=REPOSITORY,
        summary=summary,
    )

    json_path = save_repository_summary_json(
        repository=REPOSITORY,
        summary=summary,
    )

    print("Repository summary")
    print("------------------")

    for metric, value in summary.items():
        print(f"{metric}: {value}")

    print(f"\nSaved CSV  : {csv_path}")
    print(f"Saved JSON : {json_path}")


# Run:
# python -m src.run_repository_summary