import unittest
import ScrapingInfo

class TestScrapingInfo(unittest.TestCase):
    def test_MarketInfo(self):
        result = []
        self.assertEqual(ScrapingInfo.MarketInfo(result), "Success")

    def test_SliderInfo(self):
        result = []
        self.assertEqual(ScrapingInfo.SliderInfo(result), "Success")
    
    def test_CurrencyDetails(self):
        result = []
        self.assertEqual(ScrapingInfo.CurrencyDetails(result), "Success")

    def test_GetText(self):
        result = []
        self.assertEqual(ScrapingInfo.GetText(result), "Success")

if __name__ == '__main__':
    unittest.main()