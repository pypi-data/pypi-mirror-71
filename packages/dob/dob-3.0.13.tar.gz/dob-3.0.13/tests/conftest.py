# This file exists within 'dob':
#
#   https://github.com/hotoffthehamster/dob
#
# Copyright © 2018-2020 Landon Bouma,  2015-2016 Eric Goller.  All rights reserved.
#
# 'dob' is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License  as  published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any   later    version.
#
# 'dob' is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY  or  FITNESS FOR A PARTICULAR
# PURPOSE.  See  the  GNU General Public License  for  more details.
#
# You can find the GNU General Public License reprinted in the file titled 'LICENSE',
# or visit <http://www.gnu.org/licenses/>.

"""
Fixtures available to the tests/.

- In general, fixtures should return a single instance.

- If a fixture is a factory, its name should reflect that.

- A fixture that is parametrized should be suffixed with
  ``_parametrized`` to imply it has increased complexity.
"""

import pytest

from dob_bright.crud.fact_dressed import FactDressed

# We leave this conftest out of pytest_plugins, otherwise its
# test_fact_cls fixture is not overridden by the one below.
# (lb): I tested a workaround, putting the test_fact_cls below in
# another module, which I then listed in pytest_plugins, trying
# it both before and after the other one ("dob_bright.tests.conftest"),
# but the other conftest's fixture always wins (so maybe pytest sorts
# pytest_plugins?).
from dob_bright.tests.conftest import *  # noqa: F401, F403

# Load all upstream fixtures into the test namespace, as
# though the fixtures from dob-bright were defined herein.
# - It's possible to import the fixtures with a *-glob, e.g.,
#     from dob_bright.tests.conftest import *  # noqa: F401, F403
#   but using the pytest_plugins mechanism is more proper.
#   Ref:
#     https://docs.pytest.org/en/2.7.3/plugins.html
pytest_plugins = (
    "nark.tests.backends.sqlalchemy.conftest",
    # Make sure fixtures required by fixtures available, e.g., 'base_config'.
    "nark.tests.conftest",
    # SKIP (see comment, below):
    #    "dob_bright.tests.conftest",
    "tests.cli_runner",
    "tests.dob_runner",
)


# ***

@pytest.fixture
def test_fact_cls():
    return FactDressed


@pytest.fixture(scope="session")
def test_fact_cls_ro():
    return FactDressed


# ***

# (lb): Possible scope values: function, class, module, package or session.
# - Let's try the broadest scope. This is just for testing reports.
#   It drastically improves runtime at the expense of always testing
#   the same data store input for each test that uses this fixture.
#   - But we test enough using item factories in 'function'-scoped tests
#     that we should be okay.
@pytest.fixture(scope="session")
def five_report_facts_ctl(
    alchemy_store_ro,
    test_fact_cls_ro,
    set_of_alchemy_facts_ro,
    controller_with_logging_ro,
):
    controller = controller_with_logging_ro
    # You'll see 5 Facts in the store:
    #   alchemy_store_ro.session.execute('SELECT COUNT(*) FROM facts;').fetchall()
    controller.store = alchemy_store_ro
    controller.store.fact_cls = test_fact_cls_ro  # FactDressed
    # Ignored: set_of_alchemy_facts_ro.
    yield controller

