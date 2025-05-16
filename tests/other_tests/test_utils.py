from app.core.utils import exclude_falsy_from_dict

def test_exclude_falsy_from_dict():
    """
    Test the exclude_falsy_from_dict function to ensure it correctly excludes falsy values.
    This includes None, 0, False, and empty strings, but keeps boolean True.
    The function should return a new dictionary with only the truthy values.
    """

    test_dict = {
        "key1": "value1",
        "key2": None,
        "key3": 0,
        "key4": False,
        "key5": True,
        "key6": "",
        "key7": 42,
        "key8": [],
        "key9": {},
        "key10": set(),
        "key11": "non-empty",
        "key12": 3.14,
        "key13": -1,
        "key14": 0.0,
        "key15": tuple(),
    }

    expected_result = {
        "key1": "value1",
        "key5": True,
        "key7": 42,
        "key11": "non-empty",
        "key12": 3.14,
        "key13": -1,
    }

    result = exclude_falsy_from_dict(test_dict)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
