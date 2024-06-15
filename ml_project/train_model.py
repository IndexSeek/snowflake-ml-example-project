import numpy as np
from snowflake.ml.modeling.pipeline import Pipeline
from snowflake.ml.modeling.preprocessing import MinMaxScaler, OrdinalEncoder
from snowflake.ml.modeling.xgboost import XGBRegressor
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session
from utils import get_next_version


def train_model(session: Session) -> str:
    # Load the data from the DATA.DIAMONDS table.
    df = session.table("DATA.DIAMONDS")
    # Split the data into train and test.
    train, test = df.random_split([0.8, 0.2], seed=117)
    diamond_cuts = ["Ideal", "Premium", "Very Good", "Good", "Fair"]
    diamond_clarities = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]
    diamond_colors = ["D", "E", "F", "G", "H", "I", "J"]

    oe = OrdinalEncoder(
        input_cols=["CUT", "COLOR", "CLARITY"],
        output_cols=["CUT", "COLOR", "CLARITY"],
        categories={
            "CUT": np.array(diamond_cuts),
            "COLOR": np.array(diamond_colors),
            "CLARITY": np.array(diamond_clarities),
        },
    )
    mms = MinMaxScaler(
        input_cols=["CARAT", "DEPTH", "TABLE_WIDTH"],
        output_cols=["CARAT", "DEPTH", "TABLE_WIDTH"],
    )
    reg = XGBRegressor(label_cols=["PRICE"])
    # Create a pipeline.
    pipeline = Pipeline(steps=[("OE", oe), ("MMS", mms), ("REG", reg)])
    # Fit the pipeline.
    pipeline = pipeline.fit(train)
    # Log the model.
    reg = Registry(session, schema_name="MODELS")
    model_name = "DIAMOND_PRICING"
    reg.log_model(
        model=pipeline,
        model_name=model_name,
        version_name=get_next_version(reg, model_name),
        options=dict(relax_version=True),
    )
    return "Trained and logged the DIAMONDS_MODEL."


if __name__ == "__main__":
    session = Session.builder.create()
    train_model(session)
    raise SystemExit()
