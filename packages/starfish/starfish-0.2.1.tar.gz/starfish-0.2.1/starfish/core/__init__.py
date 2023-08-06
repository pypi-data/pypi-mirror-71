# deal with numpy import warnings due to cython
# See: https://stackoverflow.com/questions/40845304/
#      runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility)
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")  # noqa
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")  # noqa

# generated version number and commit hash
from ._version import get_versions


# NOTE: if we move to python 3.7, we can produce this value at call time via __getattr__
version = get_versions()['version']
is_release_tag = None
if "+" not in str(version):
    is_release_tag = f"Release: {version}"
