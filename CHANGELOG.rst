ckanext-search-tweaks 0.4.12 (2023-03-16)
========================================

Deprecations and Removals
-------------------------

- Switch from deprecated `before_search` to `before_dataset_search`


ckanext-search-tweaks 0.1.7 (2021-06-18)
========================================

Features
--------

- Allow fuzzy-search ()


Deprecations and Removals
-------------------------

- `show_worse_suggestions` -> `more_results_only` ()


ckanext-search-tweaks 0.1.2 (2021-06-16)
========================================

Features
--------

- Added `ckanext.search_tweaks.common.qf` config option and `ISearchTweaks.get_extra_qf` method ()


ckanext-search-tweaks 0.1.0 (2021-06-15)
========================================

Features
--------

- Added `ISearchTweaks` interface ()
- Added `search_tweaks_field_relevance` plugin ()
- Added `search_tweaks_spellcheck` plugin ()


Deprecations and Removals
-------------------------

- `relevance` configuration moved to `query_relevance` ()
