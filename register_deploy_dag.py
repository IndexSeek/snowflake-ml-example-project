from snowflake.core import Root
from snowflake.core._common import CreateMode
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask
from snowflake.snowpark import Session


def register_procedures(session: Session) -> str:
    session.sproc.register_from_file(
        "ml_project/load_data.py",
        func_name="load_data",
        name="COMMON.LOAD_DIAMONDS_DATA",
        is_permanent=True,
        stage_location="@COMMON.PYTHON_CODE",
        imports=["ml_project"],
        packages=["snowflake-ml-python==1.4.0"],
        replace=True,
        execute_as="caller",
    )
    session.sproc.register_from_file(
        "ml_project/train_model.py",
        func_name="train_model",
        name="COMMON.TRAIN_DIAMONDS_MODEL",
        is_permanent=True,
        stage_location="@COMMON.PYTHON_CODE",
        imports=["ml_project"],
        packages=["snowflake-ml-python==1.4.0"],
        replace=True,
        execute_as="caller",
    )
    return "Registered stored procedures."


def deploy_dag(session: Session) -> str:
    root = Root(session)
    with DAG(
        "MODEL_TRAINING_DAG",
        # We could schedule this to run every Monday at 8:00 AM EST.
        # schedule=Cron("0 8 * * 1", "America/New_York"),
        warehouse="COMPUTE_WH",
        stage_location="@PYTHON_CODE",
    ) as dag:
        load_task = DAGTask(
            name="LOAD_DATA_TASK",
            definition="CALL COMMON.LOAD_DIAMONDS_DATA();",
            warehouse="COMPUTE_WH",
        )
        train_task = DAGTask(
            name="TRAIN_MODEL_TASK",
            definition="CALL COMMON.TRAIN_DIAMONDS_MODEL();",
            warehouse="COMPUTE_WH",
        )
        load_task >> train_task
    schema = root.databases[session.get_current_database()].schemas[
        session.get_current_schema()
    ]
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag, mode=CreateMode.or_replace)
    return "Deployed the DAG."


if __name__ == "__main__":
    session = Session.builder.create()
    session.use_schema("COMMON")
    register_procedures(session)
    deploy_dag(session)
    raise SystemExit()
