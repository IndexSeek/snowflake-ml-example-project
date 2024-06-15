from snowflake.snowpark import Session
from snowflake.snowpark import types as T

from ml_project.utils import uppercase_columns


def load_data(session: Session) -> str:
    # Define a schema for reading the CSV.
    schema = T.StructType(
        [
            T.StructField('"carat"', T.DoubleType()),
            T.StructField('"cut"', T.StringType()),
            T.StructField('"color"', T.StringType()),
            T.StructField('"clarity"', T.StringType()),
            T.StructField('"depth"', T.DoubleType()),
            T.StructField('"table"', T.DoubleType()),
            T.StructField(
                '"price"',
                T.LongType(),
            ),
            T.StructField('"x"', T.DoubleType()),
            T.StructField('"y"', T.DoubleType()),
            T.StructField('"z"', T.DoubleType()),
        ]
    )
    # Create a Snowpark DataFrame from the file in the stage.
    df = session.read.option("skip_header", 1).schema(schema).csv("@DATA.DATA")
    # Uppercase the column names so they'll play nicely with Snowflake.
    df = uppercase_columns(df)
    # The column name "TABLE" is likely going to create an issue, let's rename it.
    df = df.with_column_renamed("TABLE", "TABLE_WIDTH")
    # Write the DataFrame to a Snowflake table.
    df.write.save_as_table("DATA.DIAMONDS", mode="overwrite")
    return "Wrote the DIAMONDS table to Snowflake."


if __name__ == "__main__":
    session = Session.builder.create()
    load_data(session)
    raise SystemExit()
