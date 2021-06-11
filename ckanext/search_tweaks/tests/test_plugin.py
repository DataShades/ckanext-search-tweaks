import ckan.plugins as p


def test_plugin_loaded():
    assert p.plugin_loaded("search_tweaks")
