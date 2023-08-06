**********
PYTEST-POP
**********
**A pytest plugin to help with testing pop projects**

INSTALLATION
============

Install with pip::

    pip install pytest-pop

DEVELOPMENT INSTALLATION
========================


Clone the `pytest-pop` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/pytest-pop.git
    pip install -e pytest-pop


Getting the Hub
===============

Extend the `hub` fixture in your conftest.py so that it includes your subs::

    @pytest.fixture(scope="function")
    def hub(hub):
        # TODO Add dynes that will be used for your tests
        for dyne in ("exec", "states"):
            hub.pop.sub.add(dyne_name=dyne)
            if dyne in ("corn", "exec", "states"):
                hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)

        args = [
            # TODO patch in whatever cli args are necessary to run your test
        ]
        with mock.patch("sys.argv", ["pytest-pop"] + args):
            hub.pop.config.load(["pytest_pop"], "pytest_pop")

        yield hub

        # TODO Hub cleanup
        pass


Markers
=======
Make use of pytest markers from `pytest-salt-factoroies <https://github.com/saltstack/pytest-salt-factories/blob/master/saltfactories/plugins/markers.py>`_


root
----
Marks a test as needing elevated privileges.
On UNIX-like systems the test will be skipped if the user running the tests is not root.
On Windows systems the test will be skipped if the tests aren't run with admin privileges.

Example::

    @pytest.mark.skip_if_not_root
    def test_root(hub):
        pass

expensive
---------
Marks a test as being expensive.
Run pytest with the '--run-expensive' flag or set the `EXPENSIVE_TESTS` environment variable to "True" to run these tests.
By default they will be skipped

Example::

    @pytest.mark.expensive_test
    def test_expensive(hub):
        pass

destructive
-----------
Marks a test as being destructive.
Run pytest with the '--run-destructive' flag or set the `DESTRUCTIVE_TESTS` environment variable to "True" to run these tests.
By default they will be skipped

Example::

    @pytest.mark.destructive_test
    def test_destructive(hub):
        pass

Logging
=======

You can use the hub to log without setting up a logger in every single file that uses a hub

Example::

    hub.log.debug("debug message")


Be sure to run pytest with '--cli-log-level=10' in order to see debug messages

Mocking
=======

Get access to a fully mocked/autospecced version of the hub with::

    mock_hub = hub.pop.testing.mock_hub()


A mock_hub fixture with common substitutions of real plugins is available as a fixture::

    def test_thing(mock_hub):
        pass


Extend the mock hub in your own fixture::

    # Scope the mock_hub to a function so that the autospec gets reset after each use.
    @pytest.fixture(scope="function")
    def mock_hub(mock_hub, hub):
        # replace mocked functions with necessary real ones
        # extend this on a per-module or per-function basis if necessary
        mock_hub.sub.func = hub.sub.func
        yield mock_hub

You can now do autospec assertions on contracted functions::

    import project.sub.plugin as plugin

    def test_cmd_run(mock_hub):
        plugin.func(mock_hub, "arg")
        mock_hub.sub.plugin.func.assert_called_with("arg")


ACCT
====

Some projects, specifically `idem-cloud` need credentials from idem's ctx generator.
A ctx fixture exists, but it won't work unless you override the `acct_file` and `acct_profile` fixtures::

    @pytest.fixture
    def acct_subs() -> List[str]:
        return ["azurerm", "vultr"]


    @pytest.fixture
    def acct_profile() -> str:
        return "test_development_idem_cloud"

Once these fixtures are overridden, the `ctx` fixture will become available to your test::

    test_cloud_instance_present(hub, ctx):
        hub.state.cloud.present(ctx, "instance_name")

Examples
========

Mock a hub exec function::

    with patch.object(mock_hub.exec, 'dummy', return_value="some result") as mock_exec:
        pass

Set return value for mock_hub function::

    mock_hub.sub.function.return_value = "Pass"

Mock hub assert called with::

    mock_hub.sub.function.assert_called_with("myinput", True)
