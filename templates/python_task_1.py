import pandas as pd

def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """

	""" 
	This function takes a DataFrame (df) as input.
	It uses the pivot function to create a matrix with 'car' values, where 'id_1' and 'id_2' are used as indices and columns, respectively.
	The fillna(0) is used to replace any missing values with 0.
	The diagonal values of the matrix are then set to 0 using the line car_matrix.values[[range(car_matrix.shape[0])]*2] = 0.
	The resulting matrix is returned.
	"""

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0
    return car_matrix


def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """

	"""
 	This function takes a DataFrame (df) as input.
	It creates a new column 'car_type' based on the values in the 'car' column using the pd.cut function. This categorizes 'car' values into three types: 'low', 'medium', and 'high'.
	It then counts the occurrences of each 'car_type' using value_counts(), sorts the result by index, and converts it to a dictionary.
	The resulting dictionary represents the count of occurrences for each car type.
	"""
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().sort_index().to_dict()
    return type_counts


def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
"""
This function takes a DataFrame (df) as input.
It calculates the mean of the 'bus' column.
It identifies the indices where the 'bus' values are greater than twice the mean using boolean indexing.
The resulting list contains the indices where 'bus' values exceed twice the mean, sorted in ascending order.
"""

    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
	"""
	This function takes a DataFrame (df) as input.
	It calculates the average 'truck' values for each route using groupby and mean.
	It filters and returns the routes where the average 'truck' values are greater than 7, sorted in ascending order.
	"""
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()
    return sorted(filtered_routes)


def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
"""
This function takes a DataFrame (matrix) as input.
It applies a custom logic to modify each value in the matrix:
If a value is greater than 20, it multiplies the value by 0.75.
If a value is 20 or less, it multiplies the value by 1.25.
The resulting DataFrame has modified values, rounded to one decimal place.
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    return modified_matrix
"""

def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """

"""
This function takes a DataFrame (df) as input.
It converts the 'startDay' and 'startTime' columns into a new column 'start_datetime', and similarly for 'endDay' and 'endTime'.
It then groups the DataFrame by unique combinations of 'id' and 'id_2'.
For each group, it checks if the timestamps cover a full 24-hour period and span all 7 days.
The result is a boolean series indicating whether each (id, id_2) pair has correct timestamps.

"""
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Group by id and id_2, check if the timestamps cover a full 24-hour period and span all 7 days
    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda x: (x['end_datetime'].max() - x['start_datetime'].min() == pd.Timedelta(days=6, hours=23, minutes=59, seconds=59))
                  and (x['start_datetime'].min().time() == pd.Timestamp("00:00:00").time())
                  and (x['end_datetime'].max().time() == pd.Timestamp("23:59:59").time())
    )

    return completeness_check
