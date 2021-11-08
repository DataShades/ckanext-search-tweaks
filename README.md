[![Tests](https://github.com/DataShades/ckanext-search-tweaks/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/DataShades/ckanext-search-tweaks/actions)

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

## Usage

This extensions consists of multiple plugins. `search_tweaks` is the main
(major) one, that must be enabled all the time. And depending on the set of
secondary (minor) plugins, extra features and config options may be
available. Bellow are listed all the plugins with their side effects.

| Plugin                                                          | Functionality                                                                   |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------|
| [search_tweaks](#search_tweaks)                                 | Allow all the other plugins to be enabled                                       |
| [search_tweaks_query_relevance](#search_tweaks_query_relevance) | Promote datasets that were visited most frequently for the current search query |
| [search_tweaks_field_relevance](#search_tweaks_field_relevance) | Promote dataset depending on value of it's field                                |
| [search_tweaks_spellcheck](#search_tweaks_spellcheck)           | Provides "Did you mean?" feature                                                |
<!--
| [search_tweaks_advanced_search](#search_tweaks_advanced_search) | Basic configuration of ckanext-composite-search's search form                   |
-->

### <a id="search_tweaks"></a> search_tweaks

Provides base functionality and essential pieces of logic used by all the other
plugins. Must be enabled as long as at least one other plugin from this
extension is enabled.

- Switches search to `edismax` query parser if none was specified
- Enables `ckanext.search_tweaks.iterfaces.ISearchTweaks` interface with the
following methods:

		def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
			"""Returns optional boost function that will be applied to the search query.
			"""
			return None

		def get_extra_qf(self, search_params: dict[str, Any]) -> Optional[str]:
			"""Return an additional fragment of the Solr's qf.
		    This fragment will be appended to the current qf
			"""
			return None

#### CLI

	ckan search-tweaks -
		Root of all the extension specific commands.
		Every command from minor plugins is registered under this section.


#### Config settings

	# Rewrite the default value of the qf parameter sent to Solr
	# (optional, default: value of ckan.lib.search.query.QUERY_FIELDS).
	ckanext.search_tweaks.common.qf = title^5 text

	# Search by misspelled queries.
	# (optional, default: false).
	ckanext.search_tweaks.common.fuzzy_search.enabled = on

	# Maximum number of misspelled letters. Possible values are 1 and 2.
	# (optional, default: 1).
	ckanext.search_tweaks.common.fuzzy_search.distance = 2

	# Use `boost` instead of `bf` when `edismax` query parser is active
	# (optional, default: true).
	ckanext.search_tweaks.common.prefer_boost = no

	# MinimumShouldMatch used in queries
	# (optional, default: 1).
	ckanext.search_tweaks.common.mm = 2<-1 5<80%


---

### <a id="search_tweaks_query_relevance"></a> search_tweaks_query_relevance

Increase relevance of datasets for particular query depending on number of
direct visits of the dataset after running this search. I.e, if user searches
for `something` and then visits dataset **B** which is initially displayed in a
third row of search results, eventually this dataset will be displayed on the
second or even on the first row. This is implemented in three stages. On the
first stage, statistics collected and stored inside storage(redis, by default)
and then this statistics converted into numeric solr field via cronjob.
Finally, Solr's boost function that scales number of visits and improves score
for the given query is applied during search.

Following steps are required in order to configure this plugin:

- Add field that will store statistics to schema.xml(`query_relevance_` prefix
  can be changed via config option):

		<dynamicField name="query_relevance_*"  type="int" indexed="true" stored="true"/>

- Configure a cronjob which will update search-index periodically:

		0 0 * * * ckan search-index rebuild

#### CLI

	relevance query align - remove old data from storage. Actual result of this command depends
		on storage backend, that is controlled by config. At the momment, only `redis-daily` backend
		is affected by this command - all records older than `query_relevance.daily.age` days are removed.

	relevance query export - export statistics as CSV.

	relevance query import - import statistics from CSV. Note, records that are already in storage but
		are not listed in CSV won't be removed. It must be done manually


#### Config settings

	# Which backend to use in order to collect information about dataset
	# relevance for the particular search query. Possible values are:
	# "redis-permanent", "redis-daily"
	# (optional, default: redis-daily).
	ckanext.search_tweaks.query_relevance.backend = redis-permanent

	# How long(in days) information about dataset visits will be stored in order to
	# update relevance of dataset in search query.
	# (optional, default: 90).
	ckanext.search_tweaks.query_relevance.daily.age = 90

	# Solr boost function with $field placeholder that will be replaced by
	# the correspoinding field name
	# (optional, default: "scale(def($field,0),1,1.2)").
	ckanext.search_tweaks.query_relevance.boost_function = recip($field,1,1000,1000)

	# Prefix of the numeric field defined in Solr schema. This field will hold
	# dataset's relevance for the given query.
	# (optional, default: query_relevance_).
	ckanext.search_tweaks.query_relevance.field_prefix = custom_score_

---
### <a id="search_tweaks_field_relevance"></a> search_tweaks_field_relevance

Increases the relevance of a dataset depending on value of its *numeric*
field. For now it's impossible to promote dataset using field with textual type.

No magic here either, this plugin allows you to specify Solr's boost function
that will be used during all the searches. One can achieve exactly the same
result using `ISearchTweaks.get_search_boost_fn`. But I expect this option to
be used often, so there is a possibility to update relevance without any extra
line of code.

#### Config settings

	# Solr boost function for static numeric field
	# (optional, default: None).
	ckanext.search_tweaks.field_relevance.boost_function = pow(promoted_level,2)

	# Field with dataset promotion level
	# (optional, default: promotion_level).
	ckanext.search_tweaks.field_relevance.blueprint.promotion.field_name = promotion

	# Register pacakge promotion route
	# (optional, default: False).
	ckanext.search_tweaks.field_relevance.blueprint.promotion.enabled = true

#### Auth functions

	search_tweaks_field_relevance_promote: access package promotion route. Calls `package_update` by default.

---

### <a id="search_tweaks_spellcheck"></a> search_tweaks_spellcheck

Exposes search suggestions from the Solr's spellcheck component to CKAN
templates. This plugin doesn't do much and mainly relies on the Solr's built-in
functionality. Thus you have to make a lot of changes inside Solr in order to
use it:

- `solrconfig.xml`. Configure spellcheck component. Search for `<searchComponent
  name="spellcheck" class="solr.SpellCheckComponent">` section and add the
  following item under it:

		<lst name="spellchecker">
			<str name="name">did_you_mean</str>
			<str name="field">did_you_mean</str>
			<str name="buildOnCommit">false</str>
		</lst>

- Add cron job that will update suggestions dictionary periodically:

		ckan search-tweaks spellcheck rebuild

- `solrconfig.xml`. Add spellcheck component to the search handler (`<requestHandler
  name="/select" class="solr.SearchHandler">`):

		<arr name="last-components">
			<str>spellcheck</str>
		</arr>

- Define spellcheck field in the schema. If you want to use an existing
  field(`text` for example), change `<str name="field">did_you_mean</str>`
  value inside `solrconfig.xml` to the name of the selected field instead.

		<field name="did_you_mean" type="textgen" indexed="true" multiValued="true" />

- **Note:** skip if you've decided to use an existing field in the previous step.
  <br/>
  Copy meaningfull values into this field:

		<copyField source="title" dest="did_you_mean"/>
		<copyField source="notes" dest="did_you_mean"/>
		<copyField source="res_name" dest="did_you_mean"/>
		<copyField source="res_description" dest="did_you_mean"/>
		<copyField source="extras_*" dest="did_you_mean"/>

After that you have to restart Solr service and rebuild search index:

	ckan search-index rebuild

Now you can use `spellcheck_did_you_mean` template helper that returns better
search query when available instead of the current one. Consider including
`search_tweaks/did_you_mean.html` fragment under search form.

#### Config settings

	# Do not show suggestions that have fewer results than current query
	# (optional, default: true).
	ckanext.search_tweaks.spellcheck.more_results_only = off

	# How many different suggestions you expect to see for query
	# (optional, default: 1).
	ckanext.search_tweaks.spellcheck.max_suggestions = 3

#### CLI

	spellcheck rebuild - rebuild/reload spellcheck dictionary.

---
<!--
### <a id="search_tweaks_advanced_search"></a> search_tweaks_advanced_search

Configure `ckanext-composite-search` for the basic usage. One need
`composite_search default_composite_search` plugins enabled in order to use
this plugin. It registers `advanced_search/search_form.html` snippet which can
be just used instead of `search_input` block of CKAN's
`snippets/search_form.html`. It can take a number of parameters, check its
content for details.
-->

## Developer installation

To install ckanext-search-tweaks for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-search-tweaks.git
    cd ckanext-search-tweaks
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

Apart from the default configuration for CKAN testing, you have to create
`ckan_search_tweaks` Solr's core, replace its schema with
`ckanext/search_tweaks/tests/schema.xml` and make changes to `solrconfig.xml`
that are required by `search_tweaks_spellcheck`.

To run the tests, do:

    pytest --ckan-ini=test.ini ckanext/search_tweaks/tests


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
