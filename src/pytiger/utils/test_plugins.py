import os
import sys
import unittest

from .plugins import load as load_plugins
from tempfile import mkdtemp
from shutil import rmtree


class Test_plugins_load(unittest.TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()

    def tearDown(self):
        rmtree(self.tempdir)

    def _make_plugin(self, name, content):
        p = os.path.join(self.tempdir, name)

        d = os.path.dirname(p)
        if not os.path.isdir(d):
            os.makedirs(d)

        f = open(p, 'w')
        f.write(content)
        f.close()

    def test_empty_plugin_directory(self):
        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 0)

    def test_load_one_module(self):
        self._make_plugin('test_plugin1.py', """_var = 'some data'\n""")

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 1)

        # Check that the plugin was loaded with the correct module name, that
        # its internally defined variable exists and has the right value, and
        # that it exists in the module table
        plugin1 = mods[0]
        self.assertEqual(plugin1.__name__,
                         'pytiger.utils.plugins.test_plugin1')
        self.assertEqual(plugin1._var, 'some data')
        self.assertEqual(sys.modules[plugin1.__name__], plugin1)

    def test_load_two_modules(self):
        self._make_plugin('test_theta.py', """foo = 'bar'\n""")
        self._make_plugin('test_lambda.py', """lab = 'Black Mesa'\n""")

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 2)

        # The order in which plugins are loaded is undefined, so we can't
        # assume the module objects will appear at a particular index. We'll
        # pull them out the module table instead.

        theta = sys.modules['pytiger.utils.plugins.test_theta']
        self.assertEqual(theta.foo, 'bar')

        l = sys.modules['pytiger.utils.plugins.test_lambda']
        self.assertEqual(l.lab, 'Black Mesa')

    def test_load_package(self):
        self._make_plugin('test_mypkg/__init__.py', """lemon = 'orange'\n""")

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 1)

        mypkg = mods[0]
        self.assertEqual(mypkg.__name__, 'pytiger.utils.plugins.test_mypkg')
        self.assertEqual(mypkg.lemon, 'orange')
        self.assertEqual(sys.modules[mypkg.__name__], mypkg)

    def test_ignore_init_py(self):
        self._make_plugin('__init__.py', 'deliberate syntax error!')

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 0)

    def test_ignore_non_py(self):
        self._make_plugin('random.txt', 'nothing to see here move along')

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 0)

    def test_ignore_non_package_dir(self):
        self._make_plugin('notapkg/readme.txt', 'this is not a package, ok?')

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 0)

    def test_load_package_but_not_its_modules(self):
        self._make_plugin('test_mypkg2/__init__.py', """steve = 'wozniak'\n""")
        self._make_plugin('test_mypkg2/ignored.py',
                          """raise NotImplementedError()\n""")

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 1)

        mypkg = mods[0]
        self.assertEqual(mypkg.__name__, 'pytiger.utils.plugins.test_mypkg2')
        self.assertEqual(mypkg.steve, 'wozniak')

    def test_package_can_load_its_modules(self):
        self._make_plugin('test_mypkg3/__init__.py',
                          """from .plumbing import mario\n""")
        self._make_plugin('test_mypkg3/plumbing.py',
                          """def mario():\n    return "It's a-me, Mario!"\n""")

        mods = load_plugins(self.tempdir)
        self.assertEqual(len(mods), 1)

        mypkg = mods[0]
        self.assertEqual(mypkg.__name__, 'pytiger.utils.plugins.test_mypkg3')
        whoareyou = mypkg.mario()
        self.assertEqual(whoareyou, "It's a-me, Mario!")

    def test_load_into_other_package(self):
        # This test actually loads a plugin into the sys module, so we pick a
        # very unlikely name for the module ('pytiger_plugins_test') to ensure
        # we don't clobber something vital.
        self._make_plugin('pytiger_plugins_test.py',
                          """i_am_a_virus = 'just messing with you'\n""")

        mods = load_plugins(self.tempdir, 'sys')
        self.assertEqual(len(mods), 1)

        plugin = mods[0]
        self.assertEqual(plugin.__name__, 'sys.pytiger_plugins_test')
        self.assertEqual(plugin.i_am_a_virus, "just messing with you")
