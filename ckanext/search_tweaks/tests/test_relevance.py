import pytest

import ckan.model as model
import ckanext.search_tweaks.relevance as relevance


@pytest.mark.usefixtures("with_request_context")
class TestPathHasScore:
    @pytest.mark.parametrize(
        "path, has_score",
        [
            ("/dataset", True),
            ("/dataset/hello", False),
            ("/invalid-type", False),
        ],
    )
    def test_search_referrer(self, path, has_score):
        pkg = model.Package(type="dataset")
        assert relevance._path_has_score_for(path, pkg) is has_score

    @pytest.mark.parametrize(
        "path, has_score",
        [
            ("/organization/valid", True),
            ("/group/valid", False),
            ("/organization/invalid", False),
        ],
    )
    def test_organization_referrer(self, path, has_score, monkeypatch):
        pkg = model.Package(type="dataset")
        monkeypatch.setattr(
            model.Group, "get", lambda _: model.Group(name="valid", type="organization")
        )
        assert relevance._path_has_score_for(path, pkg) is has_score

    @pytest.mark.parametrize(
        "path, has_score",
        [
            ("/organization/valid", True),
            ("/group/valid", True),
            ("/organization/invalid", False),
        ],
    )
    def test_group_referrer(self, path, has_score, monkeypatch):
        pkg = model.Package(type="dataset")
        monkeypatch.setattr(model.Group, "get", lambda _: model.Group(name="valid"))
        assert relevance._path_has_score_for(path, pkg) is has_score


@pytest.mark.usefixtures("with_request_context")
class TestUpdateScore:
    @pytest.mark.parametrize(
        "url, repeat, value",
        [
            ("/dataset?q=hello", 2, 2),
            ("/dataset?query=hello", 2, 0),
            ("/datasets?q=hello", 2, 0),
            ("/about?q=hello", 2, 0),
        ],
    )
    def test_final_score(self, url, repeat, value):
        pkg = model.Package(type="dataset", id="random")
        relevance.QueryScore(pkg.id, "hello").reset()
        for _ in range(repeat):
            relevance.update_score_by_url(pkg, url)

        assert int(relevance.QueryScore(pkg.id, "hello")) == value
