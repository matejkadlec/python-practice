from data_utils.data_load import get_model_objects_as_df
import database.crud as dc
import data_utils.data_transform as dt


if __name__ == "__main__":
    # Get user with id 1 and print their username and email
    user1 = dc.get_user_by_column("id", 1)
    print(f"User with id 1 has username {user1.username} and email {user1.email}.")

    # Get user with username charlie_brown and print their id and email
    user2 = dc.get_user_by_column("username", "charlie_brown")
    print(f"User with username charlie_brown has id {user2.id} and email {user2.email}.")

    # Load all data into separate pandas DataFrames
    df_user = get_model_objects_as_df("user")
    df_order = get_model_objects_as_df("order")
    df_product = get_model_objects_as_df("product")
    df_order_product = get_model_objects_as_df("order_product")

    # Create list with all DataFrames
    all_dataframes = [df_user, df_order, df_product, df_order_product]

    # Print some data transformations made over single DataFrame
    print(dt.get_total_amount_by_order_status(df_order))
    print(dt.flag_overdue_orders(df_order))
    print(dt.get_order_cumulative_total_per_user(df_order))

    # Print some data transformations made over two or more DataFrames
    print(dt.get_total_spend_per_user(dfs=all_dataframes))
    print(dt.get_best_selling_products(df_order_product=df_order_product, df_product=df_product))
    print(dt.count_user_orders_by_status(df_order=df_order, df_user=df_user))
