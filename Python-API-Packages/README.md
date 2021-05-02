# Python API Packages

These contain the original Python API from the LGSVL team and a version that I modified when I was debugging the API.

The difference is that `Controllables` have an attribute that hold the entire remote API JSON response. Unfortunately this did not help fix the problems being faced. 

The JSON response from the SVL Remote API only includes a limited amount of information about the state of the simulator. To change this you would have to rewrite the remote API and rebuild the simulator from source. If we were to do that, there is no reason that we would want to use the Python API.

To install these packages, navigate inside the folders and run `pip install .`

(Make sure any previous versions of the API is uninstalled.)