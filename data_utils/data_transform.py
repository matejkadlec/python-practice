import pandas as pd
from datetime import datetime
from utils.exceptions import WrongDatasetError

# Get sum of total_amount by status
def get_total_amount_by_order_status(df: pd.DataFrame) -> pd.DataFrame:
    # Check if we have orders dataset by it's unique column name
    if "order_date" not in df.columns:
        raise WrongDatasetError()
    
    return df.groupby('status')['total_amount'].sum().reset_index()


# Flag orders that are older than 3 days
def flag_overdue_orders(df: pd.DataFrame) -> pd.DataFrame:
    # Check if we have orders dataset by it's unique column name
    if "order_date" not in df.columns:
        raise WrongDatasetError()

    # Conver order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Flag orders older than 3 days
    df['is_overdue'] = (datetime.now() - df['order_date']).dt.days > 3

    return df


# Get cumulative total for each user
def get_order_cumulative_total_per_user(df: pd.DataFrame) -> pd.DataFrame:
    # Check if we have orders dataset by it's unique column name
    if "order_date" not in df.columns:
        raise WrongDatasetError()
    
    # Conver order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Convert total_amount to numeric and use NaN when it's not possible
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')

    # Sort the dataframe by user_id and order_date
    df = df.sort_values(by=['user_id', 'order_date'])
    
    # Group by user_id and calculate cumulative total of total_amount for each user
    df['cumulative_total'] = df.groupby('user_id')['total_amount'].cumsum()
    
    return df


def get_total_spend_per_user(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
        dfs[0] -> user
        dfs[1] -> order
        dfs[2] -> product
        dfs[3] -> order_product
    """
    # Check if we have correct datasets by their unique column names
    if "username" not in dfs[0] or "order_date" not in dfs[1].columns or "price" not in dfs[2].columns or "quantity" not in dfs[3].columns:
        raise WrongDatasetError()
    
    # Merge df_order with df with df_order_product to get to the product_id
    df_order_details = pd.merge(dfs[1], dfs[3], left_on='id', right_on='order_id')

    # Merge result with df_product to get to the product price
    df_order_details = pd.merge(df_order_details, dfs[2], left_on='product_id', right_on='id', suffixes=('_order', '_product'))

    # Multiply quantity and price to get the total spending
    df_order_details['total_spent'] = df_order_details['quantity'] * df_order_details['price']

    # Group by user_id and use sum aggregation to get total_spent for each user
    total_spent_per_user = df_order_details.groupby('user_id').agg(total_spent=pd.NamedAgg(column='total_spent', aggfunc='sum')).reset_index()

    # Merge result with the df_user to get user username and email and return it
    return pd.merge(total_spent_per_user, dfs[0][['id', 'username', 'email']], left_on='user_id', right_on='id', how='left').drop('id', axis=1)


def get_best_selling_products(df_order_product: pd.DataFrame, df_product: pd.DataFrame) -> pd.DataFrame:
    # Check if we have correct datasets by it's unique column name
    if "quantity" not in df_order_product.columns or "price" not in df_product.columns:
        raise WrongDatasetError()
    
    # Merge order_product with product to get to the product names
    df_order_product_details = pd.merge(df_order_product, df_product, left_on='product_id', right_on='id')

    # Group by product name and use sum aggregation to calculate the total quantity sold
    product_sales = df_order_product_details.groupby('name').agg(total_quantity_sold=pd.NamedAgg(column='quantity', aggfunc='sum')).reset_index()

    # Return descendly (from highest to lowest) sorted result
    return product_sales.sort_values(by='total_quantity_sold', ascending=False)


def count_user_orders_by_status(df_order: pd.DataFrame, df_user: pd.DataFrame) -> pd.DataFrame:
    # Check if we have correct dataset's by their unique column names
    if "order_date" not in df_order.columns or "username" not in df_user:
        raise WrongDatasetError()
    
    # Group by user_id and order status and count the number of orders and sum total amount per status using aggregate functions
    count_orders_by_status = df_order.groupby(['user_id', 'status']).agg(
        order_count=pd.NamedAgg(column='id', aggfunc='count'),
        total_amount=pd.NamedAgg(column='total_amount', aggfunc='sum')
    ).reset_index()

    # Merge result with the df_user to get user username and email and return it
    return pd.merge(count_orders_by_status, df_user[['id', 'username', 'email']], left_on='user_id', right_on='id', how='left').drop('id', axis=1)
