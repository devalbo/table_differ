
import unittest
import verify_lists


class VerifyListTest(unittest.TestCase):

    def testContains(self):
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A;D;C", "contains"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A;D;C;E", "contains"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "C;D;A", "contains"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A", "contains"))
        self.assertFalse(
            verify_lists.verify_lists("", "A;D;C;E", "contains"))


    def testOnlyContains(self):
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A", "only contains"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A;D;C;E", "only contains"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "C;D;A", "only contains"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "", "only contains"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A;B;C;D", "only contains"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "D;C;A;B", "only contains"))


    def testContainsInOrder(self):
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A", "contains in order"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A;B;C;D", "contains in order"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C", "A;B;C;D", "contains in order"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A;D;C;E", "contains in order"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "C;D;A", "contains in order"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "", "contains in order"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A;B;C;D", "contains in order"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D;E", "D;C;A;B", "contains in order"))


    def testDoesNotContain(self):
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A", "does not contain"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A;D;C;E", "does not contain"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "1;2;9", "does not contain"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "x", "does not contain"))


    def testContainsByDefault(self):
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A;D;C"))
        self.assertFalse(
            verify_lists.verify_lists("A;B;C;D", "A;D;C;E"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "C;D;A"))
        self.assertTrue(
            verify_lists.verify_lists("A;B;C;D", "A"))
        self.assertFalse(
            verify_lists.verify_lists("", "A;D;C;E"))

    


if __name__ == "__main__":
    unittest.main()
