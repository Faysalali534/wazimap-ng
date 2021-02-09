from unittest.mock import patch
from unittest.mock import Mock
import pytest

from wazimap_ng.datasets.models import Indicator, Dataset, DatasetData

from tests.datasets.factories import IndicatorFactory



@pytest.mark.django_db
class TestIndicatorModel:
    def test_primary_group(self):
        indicator = IndicatorFactory()
        indicator.groups = ["group1", "group2", "group3"]

        assert indicator.primary_group == "group1"

    def test_missing_primary_group(self):
        indicator = IndicatorFactory()
        indicator.groups = []

        assert indicator.primary_group is None

class TestIndicatorGetUniqueSubindicators:
    @patch("wazimap_ng.datasets.models.DatasetData.objects")
    def test_get_subindicators(self, mock_datasetdata_objects):
        indicator = Indicator()
        indicator.groups = ["A", "B"]
        indicator.dataset = Dataset()

        mock_datasetdata_objects.filter.return_value.get_unique_subindicators.return_value = [1, 2, 3]
        subindicators = indicator.get_unique_subindicators()

        assert subindicators == [1, 2, 3]

    @patch("wazimap_ng.datasets.models.DatasetData.objects")
    def test_get_subindicators_no_groups(self, mock_datasetdata_objects):
        indicator = Indicator()
        indicator.groups = []
        indicator.dataset = Dataset()
        mock_datasetdata_objects.filter.return_value.get_unique_subindicators.return_value = [1, 2, 3]

        subindicators = indicator.get_unique_subindicators()
        assert subindicators == []


class TestIndicatorSave:

    @patch("wazimap_ng.datasets.models.indicator.super")
    @patch("wazimap_ng.datasets.models.Indicator.get_unique_subindicators")
    def test_first_save(self, mock_get_unique_subindicators, mock_super):
        indicator = Indicator()
        mock_get_unique_subindicators.return_value = "first"

        indicator.save()

        assert indicator.subindicators == "first"

    @patch("wazimap_ng.datasets.models.indicator.super")
    @patch("wazimap_ng.datasets.models.Indicator.get_unique_subindicators")
    def test_second_save(self, mock_get_unique_subindicators, mock_super):
        indicator = Indicator()
        indicator.subindicators = "second"
        mock_get_unique_subindicators.return_value = "first"

        indicator.save()

        assert indicator.subindicators == "second"

    @patch("wazimap_ng.datasets.models.indicator.super")
    @patch("wazimap_ng.datasets.models.Indicator.get_unique_subindicators")
    def test_force_update(self, mock_get_unique_subindicators, mock_super):
        indicator = Indicator()
        indicator.subindicators = "existing subindicators"
        mock_get_unique_subindicators.return_value = "new subindicators"

        indicator.save(force_subindicator_update=True)

        assert indicator.subindicators == "new subindicators"
