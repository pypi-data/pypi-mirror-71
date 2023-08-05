<!--
TODO: add explanation of the request part of the vintage.
-->

[![image](https://img.shields.io/pypi/v/datapungi_imf.svg)](https://pypi.org/project/datapungi_imf/) 
[![build Status](https://travis-ci.com/jjotterson/datapungi_imf.svg?branch=master)](https://travis-ci.com/jjotterson/datapungi_imf)
[![downloads](https://img.shields.io/pypi/dm/datapungi_imf.svg)](https://pypi.org/project/datapungi_imf/)
[![image](https://img.shields.io/pypi/pyversions/datapungi_imf.svg)](https://pypi.org/project/datapungi_imf/)

install code: pip install datapungi_imf 

<h1> datapungi_imf  </h1>

  datapungi_imf is a python package that provides a simplified way to extract data from the API of IMF (IMF).  Overall it:
  - 
  -      
  - can read a saved API key (in json/yaml files or environment variables (default)) to avoid having a copy of it on a script.
  - can automatically test: 
      * the connectivity to all BEA datasets, 
      * the quality of the cleaned up data, and 
      * if the provided requests code snippet returns the correct result. 

## Sections
  -  [Short sample runs](#Sample-runs)
  -  [Short sample runs of all drivers](#Sample-run-of-all-drivers)
  -  [Description of a full return](#Full-request-result) 
  -  [Setting up datapungi_imf](#Setting-up-datapungi_imf)
  -  [Testing the package](#Running-Tests) 

## Sample runs

First, [set the package up](#Setting-up-datapungi_imf) (get an API key from BEA, save it somewhere and let datapungi_imf know its location).  After setting datapungi_imf up, you can run the following:

```python
'''
  Short datapungi_imf sample run
'''

import datapungi_imf as dpi

data = dpi.data() #or data = dpi.data("API Key"), see setting up section   

data.list()
data.params('IFS')
data.data('IFS/A.GB.PMP_IX')
data.meta('IFS/A.GB.PMP_IX')
```