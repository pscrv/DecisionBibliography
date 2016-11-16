import unittest
from Classifiers.Issue_Extraction import Features

class test_WordClassificationFeature(unittest.TestCase):
            
    def test_WordBoundaries(self):
        haystack = 'This is just some text to search in.'
        needle = 'is'

        feature = Features.WordClassificationFeature(needle)
        occurences = feature.CountOccurrences(haystack)
        self.assertEqual(occurences, 1)
        
    def test_wordWithApostrophe(self):
        haystack = """This is just, some text's to search in."""
        needle1 = "text's"
        needle2 = 'text'

        feature1 = Features.WordClassificationFeature(needle1)
        feature2 = Features.WordClassificationFeature(needle2)
        occurences1 = feature1.CountOccurrences(haystack)
        occurences2 = feature2.CountOccurrences(haystack)
        self.assertEqual(occurences1, 1)
        self.assertEqual(occurences2, 1)

    def test_StringInWord(self):
        haystack = """This is just some text's to search's'n't in, but doesn't make sense."""
        needles = ['tex', "sn't", 'ear',]
        features = {n : Features.StringClassificationFeature(n) for n in needles}
        occurrences = {n : features[n].CountOccurrences(haystack)  for n in needles}
        for n in needles:
            self.assertEqual(occurrences[n], 1)

