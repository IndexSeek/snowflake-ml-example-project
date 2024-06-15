from snowflake.snowpark import Session

if __name__ == "__main__":
    session = Session.builder.create()
    session.sql("CREATE OR REPLACE DATABASE ML_EXAMPLE_PROJECT").collect()
    session.use_database("ML_EXAMPLE_PROJECT")
    session.sql("CREATE SCHEMA COMMON").collect()
    session.sql("CREATE SCHEMA DATA").collect()
    session.sql("CREATE SCHEMA MODELS").collect()
    session.sql(
        "CREATE OR REPLACE STAGE DATA.DATA URL = 's3://sfquickstarts/intro-to-machine-learning-with-snowpark-ml-for-python/diamonds.csv'"
    ).collect()
    session.sql("CREATE STAGE COMMON.PYTHON_CODE").collect()
    raise SystemExit()
