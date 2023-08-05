# mls-model-registry (sktmls)

## Contents

- [Description](#description)
- [How to use](#how-to-use)
- [Version](#version)

## Description

A Python package for MLS model registry.

This python package includes
- Customized prediction pipelines inheriting MLSModel
- Model uploader to AWS S3 for meta management and online prediction

## Installation

Installation is automatically done by training containers in YE. If you want to install manually for local machines,

```bash
# develop
pip install --index-url https://test.pypi.org/simple/ --no-deps sktmls

# production
pip install sktmls
```

## How to use

[MLS Docs](https://ab.sktmls.com/docs/model-registry)

### Version
`sktmls` package version is automatically genereated followd by a production release on format `YY.MM.DD`  
We use [Calendar Versioning](https://calver.org). For version available, see the [tags on this repository](https://github.com/sktaiflow/mls-model-registry/releases).  
