from snowflake.snowpark import Session


def register_procedures(session: Session) -> str:
    session.sproc.register_from_file(
        "ml_project/load_data.py",
        func_name="load_data",
        name="LOAD_DIAMONDS_DATA",
        is_permanent=True,
        stage_location="@COMMON.PYTHON_CODE",
        imports=["ml_project"],
        packages=["seaborn==0.12.2", "snowflake-ml-python==1.4.0"],
        replace=True,
        execute_as="caller",
    )
    session.sproc.register_from_file(
        "ml_project/train_model.py",
        func_name="train_model",
        name="TRAIN_DIAMONDS_MODEL",
        is_permanent=True,
        stage_location="@COMMON.PYTHON_CODE",
        imports=["ml_project"],
        packages=["seaborn==0.12.2", "snowflake-ml-python==1.4.0"],
        replace=True,
        execute_as="caller",
    )
    return "Registered stored procedures."


if __name__ == "__main__":
    session = Session.builder.create()
    register_procedures(session)
    raise SystemExit()
