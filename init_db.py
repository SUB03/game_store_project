import ast, sys

from sqlalchemy import create_engine, text

def init_auth_tables(engine):
    from auth_service.models.models import metadata_obj
    metadata_obj.create_all(engine)

def init_store_table(engine):
    from store_service.models.models import metadata_obj
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)

if __name__ == "__main__":
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/learning", echo=True)
    
    init_auth_tables(engine)
    init_store_table(engine)

    args = sys.argv
    if len(args) >= 2 and args[1] == "filter":
        import pandas as pd
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

        #games table
        df = pd.read_csv("datasets/games_filtered.csv")
        df["release_date"] = pd.to_datetime(df["release_date"])
        df.to_sql("games", engine, if_exists="append", index=False)

        # other tables
        for col in to_convert_columns:
            df = pd.read_csv(f"datasets/{col}.csv")
            df.dropna(subset=[col], inplace=True)
            df.drop_duplicates(inplace=True)
            df.to_sql(col, engine, if_exists="append", index=False)