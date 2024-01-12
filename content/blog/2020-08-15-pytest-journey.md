---

title: 'PyTest: A Journey of 3 Years'
summary: "Salt is ending a journey that started 3 years ago with the first pull request to add support for PyTest. In the upcoming weeks, Salt will finally switch to PyTest as its sole test runner, and the previous, and heavily customized unittest runner, runtests.py, finally reaches EOL."
date: "2020-08-15"
author: Pedro Algarvio
url: "blog/pytest-a-journey-of-3-years"
image: images/blog/datacenter-03.jpg
image_alt:
tags:
    - news
    - community
---

# PyTest: A Journey of 3 Years

> Pedro Algarvio is a core member of the Salt Project team. This blog entry also appears on his personal blog at: <https://blog.algarvio.me/blog/pytest-a-journey-of-3-years/>

Salt is ending a journey that started 3 years ago with the [first pull request](https://github.com/saltstack/salt/pull/39625) to add support for [PyTest](https://docs.pytest.org). In the upcoming weeks, Salt [will finally switch](https://github.com/saltstack/salt/pull/57897) to PyTest as its **sole** test runner, and the previous, and heavily customized unittest runner, [`runtests.py`](https://github.com/saltstack/salt/blob/v3001.1/tests/runtests.py), finally reaches EOL.

## Why?

`runtests.py` served us well, but every time the Salt test suite got a new sub-directory, `runtests.py` had to be updated in order to pick up those new tests. Often enough, those tests, or sub-directories, would be added and never actually run on the CI pipelines because the needed updates to `runtests.py` were lacking.

When we needed additional daemons running for the test suite, for example the multimaster tests, again, it required an update to `runtests.py` and [quite](https://github.com/saltstack/salt/blob/v3001.1/tests/integration/__init__.py#L177-L1494) a [bit](https://github.com/saltstack/salt/blob/v3001.1/tests/multimaster/__init__.py#L61-L779) of code duplication.

There needed to be a better way going forward.

### What's The Gain?
If you know PyTest, you already know what it brings to the table. If you're not familiar, here are a few highlights:
* If you need "something" added to your test suite, it's likely that someone already [created a plugin](https://docs.pytest.org/en/latest/reference/plugin_list.html) implementing that.

* Selecting a group of tests, a single test, a test class, is [incredibly poweful and simple](https://docs.pytest.org/en/stable/usage.html#specifying-tests-selecting-tests), especially when compared to `runtests.py`.

  * Running all fileserver related tests:

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k fileserver

  * Running all proxy related tests:

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k proxy


  * Running windows specific tests(which commonly contain ``win`` in either the test module name or test name):

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k win


  * Running the failed tests after a test run, stopping at first failure:

        nox -e 'pytest-zeromq-3(coverage=False)' -- --lf --maxfail=1


* [Fixtures!](https://docs.pytest.org/en/stable/fixture.html)

    These are **powerful** and bring code deduplication to the table. The less code you have to maintain, the better, especially when talking about the test suite.
    Imagine you have a big setup routine to prepare for a test. In the [unittest](https://docs.python.org/3/library/unittest.html) world you would use [setUp](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) or [setUpClass](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUpClass).
    Now, what if that setup routine had to be used in multiple test classes?
    Likely you would either duplicate code or create a base class to reuse the code.
    In PyTest, you create a function, the fixture, and every test that needs that *prep work* just needs to add the function name(fixture name) as an [argument to the test function](https://docs.pytest.org/en/stable/fixture.html#fixtures-as-function-arguments), and

    ![Magic](https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif)

    it *"Just Works!"*

    You can even [parametrize](https://docs.pytest.org/en/stable/fixture.html#fixture-parametrize) and provide [scope](https://docs.pytest.org/en/stable/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session) for the fixtures!

* [Assertions!](https://docs.pytest.org/en/stable/assert.html)

    PyTest is smart enough that all you need to do on your test function is [`assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) something. It knows how to handle python's builtin types and [more](https://docs.pytest.org/en/stable/assert.html#defining-your-own-explanation-for-failed-assertions) if needed. Also, in case of failure, it adds useful information on the error output to hint as to why it failed. For example:

        $ pytest test_assert2.py
        =========================== test session starts ============================
        platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
        cachedir: $PYTHON_PREFIX/.pytest_cache
        rootdir: $REGENDOC_TMPDIR
        collected 1 item

        test_assert2.py F                                                    [100%]

        ================================= FAILURES =================================
        ___________________________ test_set_comparison ____________________________

            def test_set_comparison():
                set1 = set("1308")
                set2 = set("8035")
        >       assert set1 == set2
        E       AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
        E         Extra items in the left set:
        E         '1'
        E         Extra items in the right set:
        E         '5'
        E         Use -v to get the full diff

        test_assert2.py:6: AssertionError
        ========================= short test summary info ==========================
        FAILED test_assert2.py::test_set_comparison - AssertionError: assert {'0'...
        ============================ 1 failed in 0.12s =============================

There's a lot more to gain by using PyTest and also a lot of resources on the internet that you can read to know more.

## What Changes?
To begin with, most of what changes is the way we run the test suite.

* Run Unit Tests:

        nox -e 'pytest-zeromq-3(coverage=False)' -- tests/unit/

    using the deprecated ``runtests.py`` the command would have been:

        nox -e 'runtests-zeromq-3(coverage=False)' -- --unit-tests

* Run unit and integration tests for states:

        nox -e 'pytest-zeromq-3(coverage=False)' -- tests/unit/states/ tests/integration/states/

    using the deprecated ``runtests.py`` the command would have been:

        nox -e 'runtests-zeromq-3(coverage=False)' -- --state-tests

* Run integration tests for an individual module:

        nox -e 'pytest-zeromq-3(coverage=False)' -- tests/integration/modules/test_virt.py

      using the deprecated ``runtests.py`` the command would have been:

        nox -e 'runtests-zeromq-3(coverage=False)' -- -n integration.modules.test_virt

* Run unit tests for an individual module:

        nox -e 'pytest-zeromq-3(coverage=False)' -- tests/unit/modules/test_virt.py

      using the deprecated ``runtests.py`` the command would have been:

        nox -e 'runtests-zeromq-3(coverage=False)' -- -n unit.modules.test_virt

* Run an individual test by using the class and test name:

        nox -e 'pytest-zeromq-3(coverage=False)' -- 'tests/integration/modules/test_virt.py::VirtTest::test_default_kvm_profile'

      using the deprecated ``runtests.py`` the command would have been:

        nox -e 'runtests-zeromq-3(coverage=False)' -- -n integration.modules.test_virt.VirtTest.test_default_kvm_profile

* Run all macOS related tests(which commonly contain ``mac`` on the test module or test name):

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k mac

      using the deprecated ``runtests.py`` the command would have been, **impossible**.

* Run all macOS and Windows tests:

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k 'mac or win'

      using the deprecated ``runtests.py`` the command would have been, **impossible**.

* Run all MySQL related tests(which commonly contain ``mysql`` on the test module or test name):

        nox -e 'pytest-zeromq-3(coverage=False)' -- -k mysql

      using the deprecated ``runtests.py`` the command would have been, **impossible**.


As the Salt test suite evolves, [new tests](https://github.com/saltstack/salt/tree/master/tests/pytests) are going to be written for PyTest. Existing tests will likely be [rewritten](https://github.com/saltstack/salt/pull/57599) for PyTest (most, likely not all, since we have +11k tests).

### What About My Open Pull Requests?
At this stage, the Salt project will not require open pull requests to rewrite their tests for PyTest.

For new code submissions, PyTest tests are preferred. In the event that tests are being added to an existing unittest test module, it's really not a problem. We're already super exited that you're contributing code with tests!

However, please note that [unittest](https://docs.python.org/3/library/unittest.html) tests only get a [subset](https://docs.pytest.org/en/stable/unittest.html) of PyTest's mighty power.

## What's Next?
We will continue to adapt the test suite for PyTest by creating any neccessary foundational code required and rewrting almost **all** of the testing documentation.

