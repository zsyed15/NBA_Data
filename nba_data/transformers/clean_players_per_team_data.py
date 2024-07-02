if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    """

    
    data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
    
    #Ensure percentages are valid
    data = data[(data['fg_pct'] >= 0) & (data['fg_pct'] <= 1)]
    data = data[(data['fg3_pct'] >= 0) & (data['fg3_pct'] <= 1)]
    data = data[(data['ft_pct'] >= 0) & (data['ft_pct'] <= 1)]

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
