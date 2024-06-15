# Snowflake ML Example Project

This repository is intended to support the [Snowflake ML — An Example Project](https://medium.com/snowflake/snowpark-ml-an-example-project-5627e212520c)
story that is published on Medium.

For a more comprehensive explanation of how the underlying Snowflake ML
components are working; please review the
[Intro to Machine Learning with Snowpark ML for Python](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python)
Quickstart.

## Setting things up

Python should first be installed. The following Python versions are
currently supported:
- 3.8
- 3.9
- 3.10
- 3.11

The usage of a virtual environment is encouraged. Here is an example of setting
things up using pip from the project's root. (Please note, the activation
step may vary based on the shell.)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Now that the Python environment is working, a connection must be configured.
For more information on these parameters, please review the documentation at
https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect.

For the `Session.builder.create()` approach to work, a **connections.toml** or
**config.toml** file with a default connection key is required.

The following command should be executed to set up the database, schemas, and stage.
```sh
python setup_db.py
```

This project can be executed either directly from the command line or can be
setup to run inside of Snowflake with a DAG. Either/or may be used, but running
both is not necessary.

### The command line

The approach is recommended if you prefer to use an external orchestrator. The
compute operations will still be pushed down to Snowflake, and the model will
still be persisted in the Snowflake Model Registry.

```sh
python3 ml_project/load_data.py
python3 ml_project/train_model.py
```

### Inside Snowflake

This approach is recommended for centralizing and managing compute tasks and
scheduling within the Snowflake platform. It will set up stored procedures and
tasks that can be executed automatically with the Python environment setup
taken care of.

The `EXECUTE TASK ON ACCOUNT` privilege is required for the role if using this
approach.

```sql
GRANT EXECUTE TASK ON ACCOUNT TO ROLE {YOUR_ROLE};
```

Please note the task is suspended by default for testing; scheduling
is recommended. Adjusting warehouses in the task definitions is encouraged to
demonstrate configurable compute specifications. For example, the load_data task
could use a smaller warehouse, where you may want to use a larger warehouse to
train a model in practice.

```sh
python3 register_deploy_dags.py
```

<img width="967" alt="image" src="https://github.com/IndexSeek/snowflake-ml-example-project/assets/50381805/63f47739-4601-46c3-b93e-e3f8c2e6fdeb">
