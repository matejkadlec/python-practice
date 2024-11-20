import database.crud as db_crud
import pandas as pd


def get_model_objects_as_df(model_name: str) -> pd.DataFrame:
    model_list = db_crud.get_list_of_models(model_name=model_name)

    # Create dictionary from list of model objecs
    data = []
    for obj in model_list:
        row = {col.name: getattr(obj, col.name) for col in obj.__table__.columns}
        data.append(row)

    # Create pandas DataFrame from the dictionary and return it
    return pd.DataFrame(data)
