# Python App Store API Client
A python implmentation of the Intelligent Plant industrial appstore API client

See the example folder for example on how to use the library for authorization code and implicit OAuth grant flows.

## Getting started

### Installing using pip

`pip install intelligent-plant`

### Installing from Source

Using pip:

`pip install git+https://github.com/intelligentplant/py-app-store-api`

Alternatively clone the Git repo:

`git clone https://github.com/intelligentplant/py-app-store-api.git`

To install necessary dependancies run:

`pip install -r requirements.txt`

## Examples

To run the implicit grant flow (client) example run:

`python example\implicit_grant_flow.py`

To run the authorization code grant flow (server) example run:

`python example\authorization_code_grant_flow.py`

To run the example Jupyter notebook run:

`jupyter notebook`

The web UI should open, the examples can be found in `jupyter/App Store Client Example.ipynb`

The default Jupyter URL is http://localhost:8888
