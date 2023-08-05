import pandas as pd

''' 
The utils methods can be used without an instance of a class over a DataFrame
'''
def filter_by_list(
    self,
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered by a list passed as argument.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        dim: str, default None
            Is the feature with which want to work
        list_to_filter: list, default None
            The attributes which want to filter into a list

    :return: A DataFrame filtered by the attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.filter_by_list(object,df,"COLUMN",["list","of","attributes"])
    ''' 

    try:
        df_res = df[df[dim].isin(list_to_filter)]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}")
        raise 
    return df_res    

def antifilter_by_list(
    self,
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered with a different attributes listed as argument.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        dim: str, default None
            Is the feature with which want to work
        list_to_filter: list, default None
            The attributes which want to not filter into a list

    :return: A DataFrame filtered by the differents attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.antifilter_by_list(object,df,"COLUMN",["list","of","attributes"])
    ''' 
    try:        
        df_res = df[~df[dim].isin(list_to_filter)]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise 
    return df_res

def reorder_columns(
    self,
    df,
    columns
):
    r'''
    Return a dataframe ordered by the columns passed.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        columns: list
            It is the list of columns for order

    :return: A DataFrame ordered by the columns passed
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.reorder_columns(object,df,["list","of","columns"])
    '''

    try:
        dims = df.columns.tolist()
        for col in reversed(columns):             
            dims.remove(col)
            dims.insert(0, col)
            df = df[dims]
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return df

def check_data_format(self,df):
    '''
    Return a dataframe of dimensions and its formats, e.g. int, float or string
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: A DataFrame of dimensions and its formats, e.g. int, float or string
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.check_data_format(object,df)
    '''

    try:
        dataformats = df.dtypes
        dims = list(dataformats.index.astype('str'))
        formats = list(dataformats.values.astype('str'))
        formats = list(zip(dims, formats))
        df_format = pd.DataFrame(formats, columns=['Dimension', 'Format']) 
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df_format

def count_na(self,df):
    '''
    Return a dataframe counting NaNs per dataframe columns
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: A DataFrame counting NaNs per column
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.count_na(object,df)    
    '''
    
    try:
        num_obs = df.shape[0]
        nan_list = []
        for dim in df.columns:
            nan_cnt = df[dim].isna().sum()
            nan_pct = nan_cnt/num_obs*100
            nan_list.append([dim, nan_cnt, nan_pct])
        df_nan = pd.DataFrame(nan_list, columns=['Dimension', 'Qty_NaNs', 'Pct_NaNs'])
        df_nan = df_nan.sort_values(by=['Pct_NaNs'], ascending=False)
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df_nan