from datetime import datetime
from datetime import timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def addTime(time,ms,item):
    change = ms * item.name
    return time + (timedelta(milliseconds=change))


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # get timestamp and interval from the wesad file.
    timestamp_utc = datetime.fromtimestamp(data['raw_eda'][0])
    time_interval_hz = data['raw_eda'][1]
    time_interval_ms = 1 / time_interval_hz * 1000

    # use remaining data and add timestamp to it
    raw_data = data.iloc[2:(len(data) - 1)]
    raw_data.reset_index(drop=True, inplace=True)
    indexCount = 0
    raw_data['timestamp'] = raw_data.apply(lambda x: addTime(timestamp_utc,time_interval_ms,x), axis=1)
    # for item in raw_data:
    #     
    #     indexCount = indexCount + 1
    

    return raw_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
