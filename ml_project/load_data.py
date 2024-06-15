import seaborn as sns
from snowflake.snowpark import Session

from ml_project.utils import uppercase_columns


def load_data(session: Session) -> str:
    # Load this dataset from seaborn.
    diamonds = sns.load_dataset("diamonds")
    # Create a Snowpark DataFrame from the pandas DataFrame.
    df = session.create_dataframe(diamonds)
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
