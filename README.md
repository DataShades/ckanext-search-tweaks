# ckanext-search-tweaks

Set of tools providing control over search results, sorting, etc.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
|-----------------|-------------|
| 2.8 and earlier | no          |
| 2.9             | yes         |


## Installation

To install ckanext-search-tweaks:

1. Activate your CKAN virtual environment, for example:

		. /usr/lib/ckan/default/bin/activate

2. Install it on the virtualenv

		pip install ckanext-search-tweaks

3. Add `search_tweaks` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN.

## Config settings

	# Which backend to use in order to collect information about dataset
	# relevance for the particular search query. Possible values are:
	# "redis-permanent", "redis-daily"
	# (optional, default: redis-daily).
	ckanext.search_tweaks.relevance.backend = redis-permanent

	# How long(in days) information about dataset visits will be stored in order to
	# update relevance of dataset in search query.
	# (optional, default: 90).
	ckanext.search_tweaks.relevance.daily.age = 90

	# Solr boost function with $field placeholder that will be replaced by
	# the correspoinding field name
	# (optional, default: "scale(def($field,0),0,2)").
	ckanext.search_tweaks.relevance.boost_function = recip($field,1,1000,1000)

	# Prefix of the numeric field defined in Solr schema. This field will hold
	# dataset's relevance for the given query.
	# (optional, default: query_relevance_).
	ckanext.search_tweaks.relevance.field_prefix = custom_score_

<!--
<dynamicField name="query_relevance_*"  type="int" indexed="true" stored="true"/>
-->

## Developer installation

To install ckanext-search-tweaks for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-search-tweaks.git
    cd ckanext-search-tweaks
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini ckanext/search_tweaks/tests


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
