# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v1.0.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v1.0.0) - 2025-07-23

<small>[Compare with v0.6.5](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.5...v1.0.0)</small>

### Features

- rework query relevance to use boost/bf, rework storage logic ([fdb1e22](https://github.com/DataShades/ckanext-search-tweaks/commit/fdb1e228ed5095566b94a2a3643e46e28f63565c) by mutantsan).

### Bug Fixes

- remove redeclaration of boost_parts var ([736f70f](https://github.com/DataShades/ckanext-search-tweaks/commit/736f70f2d77ec93a28565324f3d659d333539f6f) by mutantsan).
- fix tests, part 3 ([d168db4](https://github.com/DataShades/ckanext-search-tweaks/commit/d168db482c09b17b1ea12041a215a5ae6ffab2d6) by mutantsan).
- fix tests, part 2 ([d52c309](https://github.com/DataShades/ckanext-search-tweaks/commit/d52c30985113e18ce9ba138596f23cabe7d7ab1a) by mutantsan).
- fix tests, part 1 ([6402026](https://github.com/DataShades/ckanext-search-tweaks/commit/640202636dba5f2fb7f12f544ad75a4dee9e164b) by mutantsan).
- incorrect HTML tag closure ([518af2d](https://github.com/DataShades/ckanext-search-tweaks/commit/518af2d0d4f8a322f685eee2c7a6ef7e32203353) by oleksandrivaniuk).

## [v0.6.5](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.5) - 2025-06-11

<small>[Compare with v0.6.4](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.4...v0.6.5)</small>

### Features

- advanced_search_config API action for external search forms ([0126cff](https://github.com/DataShades/ckanext-search-tweaks/commit/0126cff513c46da759f16460287ba85172eb3554) by Sergey Motornyuk).

## [v0.6.4](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.4) - 2025-06-01

<small>[Compare with v0.6.3](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.3...v0.6.4)</small>

### Features

- do not remove after-content of the label on advanced search ([c61d319](https://github.com/DataShades/ckanext-search-tweaks/commit/c61d31928ed42715d90807737081cd1cf9ef8bf4) by Sergey Motornyuk).

### Bug Fixes

- accessibility issues ([5371de1](https://github.com/DataShades/ckanext-search-tweaks/commit/5371de1add0af9e7267bd99a0096554180892c9e) by oleksandrivaniuk).

## [v0.6.3](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.3) - 2025-01-08

<small>[Compare with v0.6.2](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.2...v0.6.3)</small>

### Features

- add `relevance query index` command ([4ff0e00](https://github.com/DataShades/ckanext-search-tweaks/commit/4ff0e007752dabde7df6fcca340fdf7e2fea438c) by Sergey Motornyuk).
- field_relevance accept minimal promotion level ([800db76](https://github.com/DataShades/ckanext-search-tweaks/commit/800db76463f79ace5190e84bb428120e4c0d0283) by Sergey Motornyuk).

### Bug Fixes

- config declaration is not included in the package ([c038b10](https://github.com/DataShades/ckanext-search-tweaks/commit/c038b10b94b88dec7802167119c51e886cdb6ab6) by Sergey Motornyuk).

## [v0.6.2](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.2) - 2024-10-30

<small>[Compare with v0.6.1](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.1...v0.6.2)</small>

### Bug Fixes

- fix registering conditional bp ([aef3213](https://github.com/DataShades/ckanext-search-tweaks/commit/aef3213af2b9e01e40facbdd9e14f6ad2d5d350f) by mutantsan).

## [v0.6.1](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.1) - 2024-06-04

<small>[Compare with v0.6.0](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.6.0...v0.6.1)</small>

## [v0.6.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.6.0) - 2023-11-04

<small>[Compare with v0.5.0](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.5.0...v0.6.0)</small>

### Features

- drop CKAN v2.9 support ([31d1840](https://github.com/DataShades/ckanext-search-tweaks/commit/31d1840cac706f1e438601b6a4638d15ead60263) by Sergey Motornyuk).
- query_popularity plugin ([27ef0c4](https://github.com/DataShades/ckanext-search-tweaks/commit/27ef0c4f89ad11bf295db62f65d0a7262189edc9) by Sergey Motornyuk).

## [v0.5.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.5.0) - 2023-05-30

<small>[Compare with v0.4.12](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.4.12...v0.5.0)</small>

### Features

- CKAN v2.10 support ([1e48497](https://github.com/DataShades/ckanext-search-tweaks/commit/1e48497301ea2fe488709b08958c427c7c63c79d) by Sergey Motornyuk).

## [v0.4.12](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.4.12) - 2023-03-16

<small>[Compare with v0.3.10](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.10...v0.4.12)</small>

## [v0.3.10](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.10) - 2021-11-08

<small>[Compare with v0.3.8](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.8...v0.3.10)</small>

## [v0.3.8](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.8) - 2021-09-13

<small>[Compare with v0.3.7](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.7...v0.3.8)</small>

## [v0.3.7](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.7) - 2021-08-19

<small>[Compare with v0.3.6](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.6...v0.3.7)</small>

## [v0.3.6](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.6) - 2021-08-16

<small>[Compare with v0.3.4](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.4...v0.3.6)</small>

## [v0.3.4](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.4) - 2021-08-16

<small>[Compare with v0.3.3](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.3...v0.3.4)</small>

## [v0.3.3](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.3) - 2021-08-13

<small>[Compare with v0.3.2](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.2...v0.3.3)</small>

## [v0.3.2](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.2) - 2021-08-11

<small>[Compare with v0.3.1](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.1...v0.3.2)</small>

## [v0.3.1](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.1) - 2021-07-19

<small>[Compare with v0.3.0](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.3.0...v0.3.1)</small>

## [v0.3.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.3.0) - 2021-07-09

<small>[Compare with v0.2.8](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.8...v0.3.0)</small>

## [v0.2.8](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.8) - 2021-07-05

<small>[Compare with v0.2.7](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.7...v0.2.8)</small>

## [v0.2.7](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.7) - 2021-07-01

<small>[Compare with v0.2.6](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.6...v0.2.7)</small>

## [v0.2.6](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.6) - 2021-06-30

<small>[Compare with v0.2.5](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.5...v0.2.6)</small>

## [v0.2.5](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.5) - 2021-06-24

<small>[Compare with v0.2.4](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.4...v0.2.5)</small>

## [v0.2.4](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.4) - 2021-06-24

<small>[Compare with v0.2.3](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.3...v0.2.4)</small>

## [v0.2.3](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.3) - 2021-06-24

<small>[Compare with v0.2.2](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.2...v0.2.3)</small>

## [v0.2.2](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.2) - 2021-06-24

<small>[Compare with v0.2.1](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.1...v0.2.2)</small>

## [v0.2.1](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.1) - 2021-06-21

<small>[Compare with v0.2.0](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.2.0...v0.2.1)</small>

## [v0.2.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.2.0) - 2021-06-21

<small>[Compare with v0.1.7](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.7...v0.2.0)</small>

## [v0.1.7](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.7) - 2021-06-18

<small>[Compare with v0.1.6](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.6...v0.1.7)</small>

## [v0.1.6](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.6) - 2021-06-16

<small>[Compare with v0.1.5](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.5...v0.1.6)</small>

## [v0.1.5](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.5) - 2021-06-16

<small>[Compare with v0.1.4](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.4...v0.1.5)</small>

## [v0.1.4](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.4) - 2021-06-16

<small>[Compare with v0.1.3](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.3...v0.1.4)</small>

## [v0.1.3](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.3) - 2021-06-16

<small>[Compare with v0.1.2](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.2...v0.1.3)</small>

## [v0.1.2](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.2) - 2021-06-16

<small>[Compare with v0.1.1](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.1...v0.1.2)</small>

## [v0.1.1](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.1) - 2021-06-16

<small>[Compare with v0.1.0](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.1.0...v0.1.1)</small>

## [v0.1.0](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.1.0) - 2021-06-15

<small>[Compare with v0.0.2](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.0.2...v0.1.0)</small>

## [v0.0.2](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.0.2) - 2021-06-11

<small>[Compare with v0.0.1](https://github.com/DataShades/ckanext-search-tweaks/compare/v0.0.1...v0.0.2)</small>

## [v0.0.1](https://github.com/DataShades/ckanext-search-tweaks/releases/tag/v0.0.1) - 2021-06-11

<small>[Compare with first commit](https://github.com/DataShades/ckanext-search-tweaks/compare/990e2ae0dd6781a4d32d2bda6929c5ce11975703...v0.0.1)</small>

