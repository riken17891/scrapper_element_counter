import unittest

from scrapper import CustomHtmlParser
from utils import read_url, sort_dict_and_get_top_elements


class CustomHtmlParserTestCases(unittest.TestCase):

    def test_feed_and_collect_total_elements(self):
        parser = CustomHtmlParser()
        parser.feed_and_collect("<html><head></head><body>Text</body></html>")

        self.assertEqual(3, parser.total_elements)
        self.assertDictEqual(d1={"html": 1, "head": 1, "body": 1}, d2=parser.elements)
        self.assertEqual(1, parser.elements["html"])
        self.assertEqual(1, parser.elements["body"])

    def test_feed_and_collect_empty_html(self):
        parser = CustomHtmlParser()
        parser.feed_and_collect("")

        self.assertEqual(0, parser.total_elements)
        self.assertDictEqual(d1=dict(), d2=parser.elements)

    def test_top_elements(self):
        parser = CustomHtmlParser()
        parser.feed_and_collect("""
        <html>
            <head>
                <script></script>
                <script/>
            </head>
            <body>
                <div><h1><a></h1></div>
                <div>
                    <h1></h1><h2></h2><button></button>
                </div>
                <div>
                </div>
                <script></script>
                <script></script>
            </body>
        </html>""")

        self.assertEqual({"script": 4, "div": 3, "h1": 2, "body": 1, "a": 1},
                         parser.top_elements(number=5))

    def test_top_elements_out_of_index(self):
        parser = CustomHtmlParser()
        parser.feed_and_collect("""
        <html>
            <head>
            </head>
            <body>
            </body>
        </html>
        """)

        self.assertEqual({"body": 1, "head": 1, "html": 1},
                         parser.top_elements(number=5))

    def test_handle_starttag(self):
        parser = CustomHtmlParser()

        parser.handle_starttag("html", None)
        self.assertEqual(1, parser.total_elements)
        self.assertIsNotNone(parser.elements["html"])
        self.assertEqual(1, parser.elements["html"])

        parser.handle_starttag("html", None)
        self.assertEqual(2, parser.total_elements)
        self.assertEqual(2, parser.elements["html"])

        parser.handle_starttag("body", None)
        self.assertEqual(3, parser.total_elements)
        self.assertEqual(2, parser.elements["html"])
        self.assertEqual(1, parser.elements["body"])


class UtilitiesTestCases(unittest.TestCase):

    def test_read_url(self):
        response = read_url("http://ordergroove.com/company")
        self.assertNotEqual("", response)

    def test_read_url_none(self):
        response = read_url(None)
        self.assertEqual("", response)

    def test_sort_dict_and_get_top_elements(self):
        sorted_dict = sort_dict_and_get_top_elements(data_dict={"a": 5, "b": 15, "c": 7, "d": 60})
        self.assertEqual([("d", 60), ("b", 15), ("c", 7), ("a", 5)], sorted_dict)

    def test_sort_dict_and_get_top_elements_reverse(self):
        sorted_dict = sort_dict_and_get_top_elements(data_dict={"a": 5, "b": 15, "c": 7, "d": 60}, descending=False)
        self.assertEqual([("a", 5), ("c", 7), ("b", 15), ("d", 60)], sorted_dict)

    def test_sort_dict_and_get_top_elements_none(self):
        sorted_dict = sort_dict_and_get_top_elements(data_dict=None, descending=False)
        self.assertEqual(None, sorted_dict)


if __name__ == '__main__':
    unittest.main()
