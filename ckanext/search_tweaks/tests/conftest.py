import types

from unittest import mock
from typing import cast

import factory
import pytest
from pytest_factoryboy import register

import ckan.lib.search.query as query
from ckan.tests.helpers import call_action
from ckan.tests import factories


@pytest.fixture
def search(monkeypatch):
    """Call package_search and return dict, passed to search_query.run"""
    run = query.PackageSearchQuery.run
    patch = cast(
        mock.Mock,
        types.MethodType(mock.Mock(side_effect=run), query.PackageSearchQuery),
    )

    monkeypatch.setattr(query.PackageSearchQuery, "run", patch)

    def expose_args(*args, **kwargs):
        call_action("package_search", *args, **kwargs)
        return patch.call_args.args[1]

    return expose_args


@register(_name="dataset")
class DatasetFactory(factories.Dataset):
    owner_org = factory.LazyFunction(lambda: OrganizationFactory()["id"])


@register(_name="organization")
class OrganizationFactory(factories.Organization):
    pass
