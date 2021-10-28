
import unittest

from reddit import build_parser, load_reddit_data, format_reddit_data


class RedditTestCases(unittest.TestCase):
    def test_build_parser(self):
        """tests the returned ArgumentParser from build_parser()"""
        parser = build_parser()

        # tests whether running the script with the help flag exits the script
        with self.assertRaises(SystemExit):
            parser.parse_args(['-h'])

        # test default values
        test_url = 'https://www.reddit.com/r/python/.json'
        args = parser.parse_args([test_url])
        self.assertEqual(args.url, test_url)
        self.assertEqual(args.n, 10)
        self.assertEqual(args.o, "score")
        self.assertEqual(args.t, 60)

    def test_load_reddit_data(self):
        """Tests the returned dict from load_reddit_data()."""
        test_url = 'https://www.reddit.com/r/python/.json'
        actualJsonList = load_reddit_data(test_url)
        for i in range(len(actualJsonList)):
            self.assertTrue('data' in actualJsonList[i])
            self.assertTrue('title' in actualJsonList[i]['data'])
            self.assertTrue('url' in actualJsonList[i]['data'])
            self.assertTrue('score' in actualJsonList[i]['data'])

    def test_format_reddit_data(self):
        """Tests the sorted and formatted list from format_reddit_data()."""
        test_url = 'https://www.reddit.com/r/python/.json'
        actualJsonList = load_reddit_data(test_url)
        formattedList = format_reddit_data(actualJsonList, 12, "score", 20)
        self.assertEqual(12, len(formattedList))
        greatestScore = formattedList[0]['score']
        for i in range(len(formattedList)):
            self.assertLessEqual(20, len(formattedList[i]['title']))
            if (greatestScore < formattedList[i]['score']):
                self.fail('list is not sorted correctly')


if __name__ == "__main__":
    unittest.main()
