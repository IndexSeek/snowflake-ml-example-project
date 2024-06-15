import json

from snowflake.ml.registry import Registry
from snowflake.snowpark import DataFrame


def uppercase_columns(df: DataFrame) -> DataFrame:
    return df.to_df([c.upper() for c in df.columns])


def get_next_version(reg: Registry, model_name: str):
    models = reg.show_models()
    if models.empty:
        return "v1"
    models = models[models["name"] == model_name]
    if len(models.index) == 0:
        return "v1"
    versions = json.loads(models["versions"][0])
    max_version = max(int(v[1:]) for v in versions)
    return f"v{max_version + 1}"
