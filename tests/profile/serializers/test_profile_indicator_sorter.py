import pytest
import unittest
from collections import OrderedDict

from tests.profile.factories import ProfileFactory, ProfileIndicatorFactory

from tests.datasets.factories import GroupFactory

from wazimap_ng.profile.serializers.profile_indicator_sorter import ProfileIndicatorSorter

@pytest.fixture
def profile_indicators(profile):
    profile_indicator1 = ProfileIndicatorFactory(profile=profile)
    profile_indicator2 = ProfileIndicatorFactory(profile=profile)
    profile_indicator3 = ProfileIndicatorFactory()

    return [profile_indicator1, profile_indicator2, profile_indicator3]

@pytest.fixture
def datasets(profile_indicators):
    return [
        profile_indicators[0].indicator.dataset,
        profile_indicators[1].indicator.dataset,
        profile_indicators[2].indicator.dataset,
    ]

@pytest.fixture
def groups(datasets):
    subindicators1 = ["g1s3", "g1s2", "g1s1"]
    subindicators2 = ["g2s2", "g2s1", "g2s3"]
    subindicators3 = ["g3s1", "g3s2", "g3s3"]
    subindicators4 = ["a", "b"]

    return [
        GroupFactory(name="group1", dataset=datasets[0], subindicators=subindicators1),
        GroupFactory(name="group2", dataset=datasets[0], subindicators=subindicators2),
        GroupFactory(name="group3", dataset=datasets[1], subindicators=subindicators3),
        GroupFactory(name="unrelated group", dataset=datasets[2], subindicators=subindicators4),
    ]


@pytest.fixture
def subindicators_data():
    return OrderedDict(a="x", b="y", c="z")

@pytest.fixture
def profile_indicator_sorter(profile, groups):
    """
    groups passed in to make sure that appropriate objects are created
    """
    return ProfileIndicatorSorter(profile)

@pytest.fixture
def test_data(datasets):
    data = [{
        "dataset": datasets[0].id,
        "indicator_group": ["group1", "group2"],
        "jsdata": {
            "subindicators": {"g1s1": "ABC", "g1s2": "DEF", "g1s3": "GHI", },
            "groups": {
                "group2": {
                    "g2s2": {"g1s1": 4, "g1s2": 5, "g1s3": 6},
                    "g2s1": {"g1s1": 1, "g1s2": 2, "g1s3": 3},
                    "g2s3": {"g1s1": 7, "g1s2": 8, "g1s3": 9},
                }
            }
        }
    }, {
        "dataset": datasets[0].id,
        "indicator_group": ["group1", "group2"],
        "jsdata": {
            "subindicators": {"g1s2": "123", "g1s1": "456", "g1s3": "789", },
            "groups": {
                "group2": {
                    "g2s2": {"g1s1": 40, "g1s2": 50, "g1s3": 60},
                    "g2s1": {"g1s1": 10, "g1s2": 20, "g1s3": 30},
                    "g2s3": {"g1s1": 70, "g1s2": 80, "g1s3": 90},
                }
            }
        }
    }]

    return data 

@pytest.fixture
def expected_subindicators():
    return [
        {"g1s3": "GHI", "g1s2": "DEF", "g1s1": "ABC", },
        {"g1s3": "789", "g1s2": "123", "g1s1": "456", }
    ]

@pytest.fixture
def expected_groups():
    return [
        {
            "group2": OrderedDict(
                    g2s2=OrderedDict(g1s3=6, g1s2=5, g1s1=4),
                    g2s1=OrderedDict(g1s3=3, g1s2=2, g1s1=1),
                    g2s3=OrderedDict(g1s3=9, g1s2=8, g1s1=7),
                ),
        },
        {
            "group2": OrderedDict(
                g2s2=OrderedDict(g1s3=60, g1s2=50, g1s1=40),
                g2s1=OrderedDict(g1s3=30, g1s2=20, g1s1=10),
                g2s3=OrderedDict(g1s3=90, g1s2=80, g1s1=70),
            )
        }
    ]
    return {
        "group2": [
            OrderedDict(
                g2s2=OrderedDict(g1s3=6, g1s2=5, g1s1=4),
                g2s1=OrderedDict(g1s3=3, g1s2=2, g1s1=1),
                g2s3=OrderedDict(g1s3=9, g1s2=8, g1s1=7),
            ),
            OrderedDict(
                g2s2=OrderedDict(g1s3=60, g1s2=50, g1s1=40),
                g2s1=OrderedDict(g1s3=30, g1s2=20, g1s1=10),
                g2s3=OrderedDict(g1s3=90, g1s2=80, g1s1=70),
            )
        ]
    }
    

@pytest.fixture
def alternative_expected_groups():
    return [{
        "group2": {
            "g2s1": OrderedDict(g1s3=3, g1s2=2, g1s1=1),
            "g2s3": OrderedDict(g1s3=9, g1s2=8, g1s1=7),
            "g2s2": OrderedDict(g1s3=6, g1s2=5, g1s1=4),
        }
    },
    {
        "group2": {
            "g2s1": OrderedDict(g1s3=30, g1s2=20, g1s1=10),
            "g2s3": OrderedDict(g1s3=90, g1s2=80, g1s1=70),
            "g2s2": OrderedDict(g1s3=60, g1s2=50, g1s1=40),
        }
    }]

@pytest.mark.django_db
class TestProfileIndicatorSorter:
    def test_create_profile_indicator_sorter(self, datasets, groups, profile_indicator_sorter):

        sorters = profile_indicator_sorter._sorters

        assert len(sorters) == 2
        assert list(sorters.keys()) == [datasets[0].id, datasets[1].id]

        subindicator_sorter1 = sorters[datasets[0].id]
        si_groups1 = subindicator_sorter1._group_orders
        assert list(si_groups1.keys()) == [groups[0].name, groups[1].name]
        assert si_groups1[groups[0].name] == groups[0].subindicators
        assert si_groups1[groups[1].name] == groups[1].subindicators

        subindicator_sorter2 = sorters[datasets[1].id]
        si_groups2 = subindicator_sorter2._group_orders
        assert list(si_groups2.keys()) == [groups[2].name]
        assert si_groups2[groups[2].name] ==  groups[2].subindicators

    @pytest.mark.django_db
    def test_sort_subindicators(self, profile_indicator_sorter, datasets, test_data, expected_subindicators):
        sorted_data = profile_indicator_sorter.sort_subindicators(test_data)
        sorted_data = list(sorted_data)
        assert sorted_data[0]["jsdata"]["subindicators"] == expected_subindicators[0]
        assert sorted_data[1]["jsdata"]["subindicators"] == expected_subindicators[1]

    @pytest.mark.django_db
    def test_sort_groups(self, profile_indicator_sorter, test_data, expected_groups):
        sorted_data = profile_indicator_sorter.sort_groups(test_data)
        sorted_data = list(sorted_data)
        assert sorted_data[0]["jsdata"]["groups"] == expected_groups[0]
        assert sorted_data[1]["jsdata"]["groups"] == expected_groups[1]

    @pytest.mark.django_db
    def test_sort(self, profile_indicator_sorter, test_data, expected_subindicators, expected_groups):
        sorted_data = profile_indicator_sorter.sort_groups(test_data)
        sorted_data = list(sorted_data)

        assert sorted_data[0]["jsdata"]["subindicators"] == expected_subindicators[0]
        assert sorted_data[1]["jsdata"]["subindicators"] == expected_subindicators[1]

        assert sorted_data[0]["jsdata"]["groups"] == expected_groups[0]
        assert sorted_data[1]["jsdata"]["groups"] == expected_groups[1]
