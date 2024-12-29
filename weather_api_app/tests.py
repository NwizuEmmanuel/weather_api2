from django.test import TestCase, Client

# Create your tests here.
class IndexTestCase(TestCase):
    def test_homepage(self):
        client = Client()
        response = client.get("/")
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, "submit")
        self.assertContains(response, "Enter location")
        
    def test_location_search(self):
        client = Client()
        response = client.post("/", {"location": "New York"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New York")
        self.assertContains(response, "Temperature")