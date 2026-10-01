def export(file, city, rows):
    lines = [
        "# Прогноз погоды",
        "",
        f"Локация: {city}",
        "",
        "| Дата | Мин. тепм. | Макс. темп. | Описание | Влажность | Ветер |",
        "|------|------------|-------------|----------|-----------|-------|",
    ]

    for row in rows:
        lines.append(
            f"| {row.date} | {row.temp_min} | {row.temp_max} | {row.description} | {row.humidity} | {row.wind}"
        )

    with open(file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return file