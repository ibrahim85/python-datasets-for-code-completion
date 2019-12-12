import webbrowser
import unittest
import subprocess
from unittest import mock
from test import support


URL = 'http://www.example.com'
CMD_NAME = 'test'


class PopenMock(mock.MagicMock):

    def poll(self):
        return 0

    def wait(self, seconds=None):
        return 0


class CommandTestMixin:

    def _test(self, meth, *, args=[URL], kw={}, options, arguments):
        """Given a web browser instance method name along with arguments and
        keywords for same (which defaults to the single argument URL), creates
        a browser instance from the class pointed to by self.browser, calls the
        indicated instance method with the indicated arguments, and compares
        the resulting options and arguments passed to Popen by the browser
        instance against the 'options' and 'args' lists.  Options are compared
        in a position independent fashion, and the arguments are compared in
        sequence order to whatever is left over after removing the options.

        """
        popen = PopenMock()
        support.patch(self, subprocess, 'Popen', popen)
        browser = self.browser_class(name=CMD_NAME)
        getattr(browser, meth)(*args, **kw)
        popen_args = subprocess.Popen.call_args[0][0]
        self.assertEqual(popen_args[0], CMD_NAME)
        popen_args.pop(0)
        for option in options:
            self.assertIn(option, popen_args)
            popen_args.pop(popen_args.index(option))
        self.assertEqual(popen_args, arguments)


class GenericBrowserCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.GenericBrowser

    def test_open(self):
        self._test('open',
                   options=[],
                   arguments=[URL])


class BackgroundBrowserCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.BackgroundBrowser

    def test_open(self):
        self._test('open',
                   options=[],
                   arguments=[URL])


class ChromeCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Chrome

    def test_open(self):
        self._test('open',
                   options=[],
                   arguments=[URL])

    def test_open_with_autoraise_false(self):
        self._test('open', kw=dict(autoraise=False),
                   options=[],
                   arguments=[URL])

    def test_open_new(self):
        self._test('open_new',
                   options=['--new-window'],
                   arguments=[URL])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=[],
                   arguments=[URL])


class MozillaCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Mozilla

    def test_open(self):
        self._test('open',
                   options=[],
                   arguments=[URL])

    def test_open_with_autoraise_false(self):
        self._test('open', kw=dict(autoraise=False),
                   options=[],
                   arguments=[URL])

    def test_open_new(self):
        self._test('open_new',
                   options=[],
                   arguments=['-new-window', URL])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=[],
                   arguments=['-new-tab', URL])


class NetscapeCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Netscape

    def test_open(self):
        self._test('open',
                   options=['-raise', '-remote'],
                   arguments=['openURL({})'.format(URL)])

    def test_open_with_autoraise_false(self):
        self._test('open', kw=dict(autoraise=False),
                   options=['-noraise', '-remote'],
                   arguments=['openURL({})'.format(URL)])

    def test_open_new(self):
        self._test('open_new',
                   options=['-raise', '-remote'],
                   arguments=['openURL({},new-window)'.format(URL)])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=['-raise', '-remote'],
                   arguments=['openURL({},new-tab)'.format(URL)])


class GaleonCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Galeon

    def test_open(self):
        self._test('open',
                   options=['-n'],
                   arguments=[URL])

    def test_open_with_autoraise_false(self):
        self._test('open', kw=dict(autoraise=False),
                   options=['-noraise', '-n'],
                   arguments=[URL])

    def test_open_new(self):
        self._test('open_new',
                   options=['-w'],
                   arguments=[URL])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=['-w'],
                   arguments=[URL])


class OperaCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Opera

    def test_open(self):
        self._test('open',
                   options=['-remote'],
                   arguments=['openURL({})'.format(URL)])

    def test_open_with_autoraise_false(self):
        self._test('open', kw=dict(autoraise=False),
                   options=['-remote', '-noraise'],
                   arguments=['openURL({})'.format(URL)])

    def test_open_new(self):
        self._test('open_new',
                   options=['-remote'],
                   arguments=['openURL({},new-window)'.format(URL)])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=['-remote'],
                   arguments=['openURL({},new-page)'.format(URL)])


class ELinksCommandTest(CommandTestMixin, unittest.TestCase):

    browser_class = webbrowser.Elinks

    def test_open(self):
        self._test('open', options=['-remote'],
                           arguments=['openURL({})'.format(URL)])

    def test_open_with_autoraise_false(self):
        self._test('open',
                   options=['-remote'],
                   arguments=['openURL({})'.format(URL)])

    def test_open_new(self):
        self._test('open_new',
                   options=['-remote'],
                   arguments=['openURL({},new-window)'.format(URL)])

    def test_open_new_tab(self):
        self._test('open_new_tab',
                   options=['-remote'],
                   arguments=['openURL({},new-tab)'.format(URL)])


class BrowserRegistrationTest(unittest.TestCase):

    def setUp(self):
        # Ensure we don't alter the real registered browser details
        self._saved_tryorder = webbrowser._tryorder
        webbrowser._tryorder = []
        self._saved_browsers = webbrowser._browsers
        webbrowser._browsers = {}

    def tearDown(self):
        webbrowser._tryorder = self._saved_tryorder
        webbrowser._browsers = self._saved_browsers

    def _check_registration(self, preferred):
        class ExampleBrowser:
            pass

        expected_tryorder = []
        expected_browsers = {}

        self.assertEqual(webbrowser._tryorder, expected_tryorder)
        self.assertEqual(webbrowser._browsers, expected_browsers)

        webbrowser.register('Example1', ExampleBrowser)
        expected_tryorder = ['Example1']
        expected_browsers['example1'] = [ExampleBrowser, None]
        self.assertEqual(webbrowser._tryorder, expected_tryorder)
        self.assertEqual(webbrowser._browsers, expected_browsers)

        instance = ExampleBrowser()
        if preferred is not None:
            webbrowser.register('example2', ExampleBrowser, instance,
                                preferred=preferred)
        else:
            webbrowser.register('example2', ExampleBrowser, instance)
        if preferred:
            expected_tryorder = ['example2', 'Example1']
        else:
            expected_tryorder = ['Example1', 'example2']
        expected_browsers['example2'] = [ExampleBrowser, instance]
        self.assertEqual(webbrowser._tryorder, expected_tryorder)
        self.assertEqual(webbrowser._browsers, expected_browsers)

    def test_register(self):
        self._check_registration(preferred=False)

    def test_register_default(self):
        self._check_registration(preferred=None)

    def test_register_preferred(self):
        self._check_registration(preferred=True)


if __name__=='__main__':
    unittest.main()