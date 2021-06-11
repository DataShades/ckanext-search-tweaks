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
	ckanext.search_tweaks.search_relevance.backend = redis-permanent

	# How long(in days) information about dataset visits will be stored in order to
	# update relevance of dataset in search query.
	# (optional, default: 90).
	ckanext.search_tweaks.search_relevance.daily.age = 90



## Developer installation

To install ckanext-search-tweaks for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-search-tweaks.git
    cd ckanext-search-tweaks
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-search-tweaks

If ckanext-search-tweaks should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
