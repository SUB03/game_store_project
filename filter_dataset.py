import pandas as pd
import ast

if __name__ == "__main__":
    with open("datasets/games_march2025_cleaned.csv", 'r') as file:
        data_df = pd.read_csv(file)

    correct_columns = [
        "appid",
        "name",
        "release_date",
        "required_age",
        "price",
        "dlc_count",
        "detailed_description",
        "about_the_game",
        "short_description",
        "reviews",
        "header_image",
        "website",
        "support_url",
        "support_email",
        "windows",
        "mac",
        "linux",
        "metacritic_score",
        "metacritic_url",
        "achievements",
        "recommendations",
        "notes",
        "positive",
        "negative",
        "discount",
    ]
    to_convert_columns = [
        "supported_languages",
        "full_audio_languages",
        "developers",
        "publishers",
        "categories",
        "genres",
        "screenshots",
        "movies",
        "tags",
    ]
    data_df = data_df[correct_columns + to_convert_columns]

    def parse(val):
        try:
            return ast.literal_eval(str(val))
        except (ValueError, SyntaxError):
            return []

    for col in data_df.columns:
        if col in to_convert_columns:
            data_df[col] = data_df[col].apply(parse)
            data_df[['appid', col]].explode(col, ignore_index=True).to_csv(f"datasets/{col}.csv", index=False)
            data_df.drop(columns=[col], inplace=True)
        elif col not in correct_columns:
            data_df.drop(columns=[col], inplace=True)

    data_df.to_csv("datasets/games_filtered.csv", index=False, header=True)