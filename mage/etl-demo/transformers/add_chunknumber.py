from pandas import DataFrame
import math
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """
    # Specify your transformation logic here
    max_sequence_length = 128
    input_length = len(df)
    num_chunks = input_length // max_sequence_length + 1
    chunks = []
    for i in range(num_chunks):
        start_idx = i * max_sequence_length
        end_idx = min((i + 1) * max_sequence_length, input_length)
        chunk = df[start_idx:end_idx]
        chunk['chunkNumber']= i + 1
        chunks.append(chunk)


    return pd.concat(chunks)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
