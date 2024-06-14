from snowflake.snowpark import DataFrame


def uppercase_columns(df: DataFrame) -> DataFrame:
    return df.to_df([c.upper() for c in df.columns])
