import pytest
import mergeyaml


def test_shallow_dict_merge():
    a = {
        'one': [1, 2, 3]
    }
    b = {
        'two': [2, 3, 4]
    }

    expected = {
        'one': [1, 2, 3],
        'two': [2, 3, 4],
    }
    assert mergeyaml.merge(a, b) == expected


def test_deep_dict_merge():
    a = {
        'one': [1, 2, 3],
        'three': {'one': 1},
    }
    b = {
        'two': [2, 3, 4],
        'three': {'two': 2},
    }

    expected = {
        'one': [1, 2, 3],
        'two': [2, 3, 4],
        'three': {
            'one': 1,
            'two': 2,
        },
    }
    assert mergeyaml.merge(a, b) == expected


def test_list_within_dict_merge():
    a = {
        'one': [1, 2],
    }
    b = {
        'one': [2, 3],
    }

    expected = {
        'one': [1, 2, 3],
    }
    assert mergeyaml.merge(a, b) == expected


def test_list_merge():
    a = [1, 2]
    b = [2, 3]
    expected = [1, 2, 3]
    assert mergeyaml.merge(a, b) == expected


def test_different_types_merge():
    a = {}
    b = [1]
    assert mergeyaml.merge(a, b) == [1]

    a = []
    b = {'one': 1}
    assert mergeyaml.merge(a, b) == {'one': 1}

    a = []
    b = ""
    assert mergeyaml.merge(a, b) == ""

    a = {
        'one': {'two': {'three': [3]}}
    }
    b = {
        'one': {'two': {'three': ["three"]}}
    }
    expected = {
        'one': {'two': {'three': [3, "three"]}}
    }
    assert mergeyaml.merge(a, b) == expected

    a = {
        'one': {'two': {'three': [3]}}
    }
    b = {
        'one': {'two': {'three': "three"}}
    }
    expected = {
        'one': {'two': {'three': "three"}}
    }
    assert mergeyaml.merge(a, b) == expected
