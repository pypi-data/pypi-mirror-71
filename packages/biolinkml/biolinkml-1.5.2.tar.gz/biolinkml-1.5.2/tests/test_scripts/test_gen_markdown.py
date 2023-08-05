import os
import unittest

from biolinkml.generators.markdowngen import cli
from tests import source_yaml_path
from tests.test_scripts.clicktestcase import ClickTestCase


class GenMarkdownTestCase(ClickTestCase):
    testdir = "genmarkdown"
    click_ep = cli
    prog_name = "gen-markdown"

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        outdir = self.temp_directory('meta')
        self.do_test(source_yaml_path + f" -d {outdir}", dirbase='meta')

    def test_issue_2(self):
        outdir = self.temp_directory('issue2')
        self.do_test(source_yaml_path + f" -d {outdir} -c example -i ", dirbase='issue2')
        ex_file = os.path.join(outdir, 'images', 'Example.svg')
        self.assertTrue(os.path.exists(ex_file), f"Filed to create {ex_file}")
        self.assertFalse(os.path.exists(os.path.join(outdir, 'abstract.md')))


if __name__ == '__main__':
    unittest.main()
