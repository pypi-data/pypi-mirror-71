..
    : MolMod is a collection of molecular modelling tools for python.
    : Copyright (C) 2007 - 2019 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
    : for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all rights
    : reserved unless otherwise stated.
    :
    : This file is part of MolMod.
    :
    : MolMod is free software; you can redistribute it and/or
    : modify it under the terms of the GNU General Public License
    : as published by the Free Software Foundation; either version 3
    : of the License, or (at your option) any later version.
    :
    : MolMod is distributed in the hope that it will be useful,
    : but WITHOUT ANY WARRANTY; without even the implied warranty of
    : MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    : GNU General Public License for more details.
    :
    : You should have received a copy of the GNU General Public License
    : along with this program; if not, see <http://www.gnu.org/licenses/>
    :
    : --

Release history
###############

**Version 1.4.8** June 16, 2020

- Switch to PyTest for testing. The ``zip_unsafe`` option is no longer needed in
  ``setup.py``, because pytest can also collect unit tests inside egg installs.

**Version 1.4.7** May 14, 2020

- Fix version in the NumPy dependency (at least 1.16.00). This is needed to
  avoid data structure incompatibility issues in the Cython extension.

**Version 1.4.6** May 12, 2020

- Bug fix for Python 3.8.

**Version 1.4.5** September 11, 2019

- Conda packages for Python 3.7.
- Fix bug in bond-order algorithm in MolecularGraph.
- Make buffer tricks work in Python 2 and 3 in Graph class.
- Document algorithm to detect bonds.
- Fix unicode issues

**Version 1.4.4** November 20, 2017

- Fix Python 3 bug in CHK format
- Fix counter error in ring detection (Patrik Marschalik)

**Version 1.4.3** August 29, 2017

- First release on molmod conda channel.

**Version 1.4.2** August 18, 2017

- Fix bugs in the internal ``.chk`` file format.

**Version 1.4.1** August 7, 2017

- Fix windows compatibility bug.

**Version 1.4.0** August 6, 2017

- Testing on Windows instances with AppVeyor, with deployment of Windows packages to
  anaconda.
- Testing on Travis with OSX instances, with deployment of OSX packages to
  anaconda.
- Fix tests failing due to unfortunate random numbers.
- Skip tests on known weaknesses of binning.

**Version 1.3.5** August 5, 2017

- Python 3 bug fix

**Version 1.3.4** August 5, 2017

- Python 3 bug fixes

**Version 1.3.2** August 3, 2017

- Specify versions of dependencies in setup.py.

**Version 1.3.1** August 3, 2017

- Fix parallel testing issue with ``tmpdir`` contextwrapper.

**Version 1.3.0** August 3, 2017

- Python 3 support.

**Version 1.2.1** August 2, 2017

- Switch to setuptools in setup.py.
- Use Cython to compile the extension instead of f2py.
- Use Conda for testing on Travis-CI.
- Automatic deployment of new version on PyPI, Github and anaconda.org
- Simplified installation.
- Many cleanups.
- Fix mistake in the Kabsch algorithm.

**Version 1.1** September 9, 2014

- DLPoly history reader also works for restarted calculation.
- Testing on Travis-CI
- Various small improvements

**Version 1.0** June 5, 2013

- First stable release of MolMod on Github.
