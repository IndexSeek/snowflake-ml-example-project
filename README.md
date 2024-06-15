# Snowflake ML Example Project

This repository is intended to support the [Snowflake ML — An Example Project](https://medium.com/snowflake/snowpark-ml-an-example-project-5627e212520c)
story that is published on Medium.

For a more comprehensive explanation as to how the underlying Snowflake ML
components are working, please review the
[Intro to Machine Learning with Snowpark ML for Python](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python)
Quickstart.

## Setting things up

Python should first be installed installed. The following Python versions are
currently supported:
- 3.8
- 3.9
- 3.10
- 3.11

The usage of a virtual environment is encouraged. Here is an example of setting
things up using pip from the root of the project. (Please note, the activation
step may vary based on the shell.)

```sh
python3 -m venv venv
source .venv/bin/activate
pip install -e .
```

Now that the Python environment is working, a connection will need to be configured.
For more information on these parameters, please review the documentation at
https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect.

For the `Session.builder.create()` approach to work, a **connections.toml** or
**config.toml** file with a default connection key is required.

To setup the database, schemas, and the stage, the following command should be
executed.
```sh
python setup_db.py
```

This project can be executed either directly from the command line or can be
setup to run inside of Snowflake with a DAG.

Either/or may be used, but running both is not necessary.

### The command line

The approach is recommended if you prefer to use an external orchestrator. The
compute operations will still be pushed down to Snowflake and the model will
still be persisted in the Snowflake Model Registry.

```sh
python3 load_data.py
python3 train_model.py
```

### Inside Snowflake

The `EXECUTE TASK ON ACCOUNT` privilege is required for the role if using this
approach.

```sql
GRANT EXECUTE TASK ON ACCOUNT TO ROLE {YOUR_ROLE};
```

This approach is recommended for centralizing and managing compute tasks and
scheduling within the Snowflake platform. It will setup stored procedures and
tasks that can be executed automatically with the Python environment setup
taken care of.

```sh
python3 register_deploy_dags.py
```
