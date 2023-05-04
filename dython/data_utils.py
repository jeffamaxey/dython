import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ._private import convert


__all__ = [
    "identify_columns_by_type",
    "identify_columns_with_na",
    "one_hot_encode",
    "split_hist",
]


def one_hot_encode(arr, classes=None):
    """
    One-hot encode a 1D array.
    Based on this StackOverflow answer: https://stackoverflow.com/a/29831596/5863503

    Parameters:
    -----------
    arr : array-like
        An array to be one-hot encoded. Must contain only non-negative integers
    classes : int or None
        number of classes. if None, max value of the array will be used

    Returns:
    --------
    2D one-hot encoded array

    Example:
    --------
    >>> one_hot_encode([1,0,5])
    array([[0., 1., 0., 0., 0., 0.],
           [1., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 1.]])
    """
    arr = convert(arr, "array").astype(int)
    if len(arr.shape) != 1:
        raise ValueError(
            f"array must have only one dimension, but has shape: {arr.shape}"
        )
    if arr.min() < 0:
        raise ValueError("array cannot contain negative values")
    classes = classes if classes is not None else arr.max() + 1
    h = np.zeros((arr.size, classes))
    h[np.arange(arr.size), arr] = 1
    return h


def split_hist(
    dataset,
    values,
    split_by,
    title="",
    xlabel="",
    ylabel=None,
    figsize=None,
    legend="best",
    plot=True,
    **hist_kwargs,
):
    """
    Plot a histogram of values from a given dataset, split by the values of a chosen column

    Parameters:
    -----------
    dataset : Pandas DataFrame
    values : string
        The column name of the values to be displayed in the histogram
    split_by : string
        The column name of the values to split the histogram by
    title : string or None, default = ''
        The plot's title. If empty string, will be '{values} by {split_by}'
    xlabel: string or None, default = ''
        x-axis label. If empty string, will be '{values}'
    ylabel: string or None, default: None
        y-axis label
    figsize: (int,int) or None, default = None
        A Matplotlib figure-size tuple. If `None`, falls back to Matplotlib's
        default.
    legend: string or None, default = 'best'
        A Matplotlib legend location string. See Matplotlib documentation for possible options
    plot: Boolean, default = True
        Plot the histogram
    hist_kwargs: key-value pairs
        A key-value pairs to be passed to Matplotlib hist method. See Matplotlib documentation for possible options

    Returns:
    --------
    A Matplotlib `Axe`

    Example:
    --------
    See example under `dython.examples`
    """
    plt.figure(figsize=figsize)
    split_vals = dataset[split_by].unique()
    data_split = [dataset[dataset[split_by] == val][values] for val in split_vals]
    hist_kwargs["label"] = split_vals
    plt.hist(data_split, **hist_kwargs)
    if legend:
        plt.legend(loc=legend)
    if xlabel is not None:
        if xlabel == "":
            xlabel = values
        plt.xlabel(xlabel)
    if title is not None:
        if title == "":
            title = values + " by " + split_by
        plt.title(title)
    plt.ylabel(ylabel)
    ax = plt.gca()
    if plot:
        plt.show()
    return ax


def identify_columns_by_type(dataset, include):
    """
    Given a dataset, identify columns of the types requested.

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame
    include : list of strings
        Desired column types

    Returns:
    --------
    A list of columns names

    Example:
    --------
    >>> df = pd.DataFrame({'col1': ['a', 'b', 'c', 'a'], 'col2': [3, 4, 2, 1], 'col3': [1., 2., 3., 4.]})
    >>> identify_columns_by_type(df, include=['int64', 'float64'])
    ['col2', 'col3']

    """
    dataset = convert(dataset, "dataframe")
    columns = list(dataset.select_dtypes(include=include).columns)
    return columns


def identify_columns_with_na(dataset):
    """
    Return columns names having NA values, sorted in descending order by their number of NAs

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame

    Returns:
    --------
    A DataFrame of two columns (['column', 'na_count']), consisting of only the names
    of columns with NA values, sorted by their number of NA values.

    Example:
    --------
    >>> df = pd.DataFrame({'col1': ['a', np.nan, 'a', 'a'], 'col2': [3, np.nan, 2, np.nan], 'col3': [1., 2., 3., 4.]})
    >>> identify_columns_with_na(df)
      column  na_count
    1   col2         2
    0   col1         1
    """
    dataset = convert(dataset, "dataframe")
    na_count = [sum(dataset[cc].isnull()) for cc in dataset.columns]
    return (
        pd.DataFrame({"column": dataset.columns, "na_count": na_count})
        .query("na_count > 0")
        .sort_values("na_count", ascending=False)
    )
