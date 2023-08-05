# KGTK: Knowledge Graph Toolkit 

[![doi](https://zenodo.org/badge/DOI/10.5281/zenodo.3828068.svg)](https://doi.org/10.5281/zenodo.3828068)  ![travis ci](https://travis-ci.org/usc-isi-i2/kgtk.svg?branch=dev)

KGTK is a Python library for easy manipulation with knowledge graphs. It provides a flexible framework that allows chaining of common graph operations, such as: extraction of subgraphs, filtering, computation of graph metrics, validation, cleaning, generating embeddings, and so on. Its principal format is TSV, though we do support a number of other inputs. 

## Documentation

https://kgtk.readthedocs.io/en/latest/

## Features

* Computation of class instances
* Computation of reachable nodes
* Filtering based on property values
* Removal of columns
* Sorting
* Computation of various embeddings
* Cleaning and validation
* Computation of graph metrics
* Joining and concatenation of graphs
* Manipulation of Wikidata data

## Releases

* [Source code](https://github.com/usc-isi-i2/kgtk/releases)

## Installation through Docker

```
docker pull uscisii2/kgtk:0.2.0
```

More information about versions and tags here: https://hub.docker.com/repository/docker/uscisii2/kgtk

## Local installation

0. Our installations will be in a conda environment. If you don't have a conda installed, follow [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to install it.
1. Set up your own conda environment:
```
conda create -n kgtk-env python=3.7
conda activate kgtk-env
```
 **Note:** Installing Graph-tool is problematic on python 3.8 and out of a virtual environment. Thus: **the advised installation path is by using a virtual environment.**

2. Install (the dev branch at this point): `pip install kgtk`

You can test if `kgtk` is installed properly now with: `kgtk -h`.

3. Install `graph-tool`: `conda install -c conda-forge graph-tool`. If you don't use conda or run into problems, see these [instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions). 

4. Install `mlr`. Depending on your environment, you can run one of the following:
  * `brew update && brew install miller` (on mac)
  * `sudo port selfupdate && sudo port install miller` (on mac)
  * `sudo apt-get install miller` (linux)
  * `sudo apt install miller` (linux)
  * `sudo yum install miller` (linux)
  
More installation options for `mlr` can be found [here](https://johnkerl.org/miller/doc/build.html).

If you can't install miller with `yum install` on centOS, please follow this [link](https://centos.pkgs.org/7/openfusion-x86_64/miller-5.3.0-1.of.el7.x86_64.rpm.html).


## Running KGTK commands

To list all the available KGTK commands, run:

`kgtk -h`

To see the arguments of a particular commands, run:

`kgtk <command> -h`

An example command that computes instances of the subclasses of two classes:

`kgtk instances --transitive --class Q13442814,Q12345678`

## Additional information

### The Miller Package

1. Our code uses the "miller" package to manipulate formatted data.

2. TheGitHub repository for miller is:
```
https://github.com/johnkerl/miller
```
3. The documentaton is:
```
https://www.mankier.com/1/mlr
```
4. You may need to install the miller command (mlr) on your system.
   * OpenSUSE Tumbleweed Linux: install package `miller` from Main Repository (OSS)

### List of supported tools
* `instances`
* `reachable_nodes`
* `filter`
* `text_embedding`
* `remove_columns`
* `sort`
* `gt_loader`
* `merge_identical_nodes`
* `zconcat`
* `export_neo4j`

To get an information on how to use each of them, run:
`kgtk [TOOL] -h`

More detailed description of the arguments will be added here promptly.

### Developer Instructions

Please refer to [this](README_dev.md)
