from django.http import HttpRequest
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from accounts.models import Account

from datasets.models import Dataset

from main.views import portal, load_dataset

class AboutViewTests(TestCase):
    """
    This view is actually simply a TemplateView implemented in the urls section
    of the main app. So making sure that the template and url are correct is
    all that really needs to be done.
    """

    def test_AboutView_url_resolves(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_AboutView_uses_correct_template(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response,
            template_name="about.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_AboutView_url_title_is_correct(self):
        response = self.client.get(reverse("about"))
        self.assertIn("<title>ZMT | About</title>", response.content.decode("utf-8"))


class ContactViewTests(TestCase):
    """
    This view is actually simply a TemplateView implemented in the urls section
    of the main app. So making sure that the template and url are correct is
    all that really needs to be done.
    """

    def test_ContactView_url_resolves(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_ContactView_uses_correct_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response,
            template_name="contact.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_ContactView_url_title_is_correct(self):
        response = self.client.get(reverse("contact"))
        self.assertIn("<title>ZMT | Contact</title>", response.content.decode("utf-8"))


class PortalViewTests_EMPTY_DATABASE(TestCase):

    def test_that_PortalView_without_datasets_says_none_available(self):
        response = self.client.get(reverse('portal'))
        self.assertIn('There are no datasets available',
            response.content.decode('utf-8'))

    def test_that_PortalView_brings_in_correct_number_of_dataset_objects(self):
        response = self.client.get(reverse('portal'))
        self.assertEqual(0, len(response.context['dataset_list']))


class PortalViewTests(TestCase):

    def setUp(self):
        self.a1 = Account.objects.create(user="test_user",
            affiliation="Zentrum für Marine Tropenökologie")

        self.ds1 = Dataset.objects.create(account=self.a1,
            author="Google",
            title="Google GeoJSON Example",
            description="Polygons spelling 'GOOGLE' over Australia",
            url="https://storage.googleapis.com/maps-devrel/google.json",
            public_access=True)

#        self.ds2 = Dataset.objects.create(account=self.a1,
#            author="zmtdummy",
#            title="Password Protected Dataset",
#            description="Just a page that requires login and password info",
#            url="https://bitbucket.org/zmtdummy/geojsondata/raw/ad675d6fd6e2256b365e79e785603c2ab454006b/password_protected_dataset.json",
#            dataset_user="zmtdummy",
#            dataset_password="zmtBremen1991",
#            public_access=False)

        self.ds3 = Dataset.objects.create(account=self.a1,
            author="Pat",
            title="Bienvenidos",
            description="Polygons spelling 'Bienvenidos' over the United States",
            url="https://raw.githubusercontent.com/zmtdummy/GeoJsonData/master/bienvenidos.json",
            public_access=True)


    def test_portal_url_resolves(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_portal_function_resolves(self):
        request = HttpRequest()
        response = portal(request)
        self.assertEqual(response.status_code, 200)

    def test_dataset_detail_view_uses_correct_templates(self):
        response = self.client.get(reverse("portal"))
        self.assertTemplateUsed(response,
            template_name="portal.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_dataset_detail_view_title_is_correct(self):
        response = self.client.get(reverse("portal"))
        self.assertIn("<title>ZMT | Portal</title>" , response.content.decode("utf-8"))

    def test_that_dataset_detail_view_brings_in_correct_dataset_object(self):
        response = self.client.get(reverse("portal"))
        self.assertTrue(response.context["dataset_list"])

    # it is probably unnecessary to run these two tests with these 4
    # assertions, they are redundant 
    def test_portal_search_function_1(self):
       response = self.client.get('/?q=Bien')
       self.assertEqual(response.status_code, 200)
       self.assertIn('Bienvenidos', response.content.decode('utf-8'))
       self.assertNotIn('Google GeoJSON Example', response.content.decode('utf-8'))


class LoadDatasetTests(TestCase):

    def setUp(self):
        self.a1 = Account.objects.create(user="test_user",
            affiliation="Zentrum für Marine Tropenökologie")

        self.ds1 = Dataset.objects.create(account=self.a1,
            author="Google",
            title="Google GeoJSON Example",
            description="Polygons spelling 'GOOGLE' over Australia",
            url="https://storage.googleapis.com/maps-devrel/google.json",
            public_access=True)

#        self.ds2 = Dataset.objects.create(account=self.a1,
#            author="zmtdummy",
#            title="Password Protected Dataset",
#            description="Just a page that requires login and password info",
#            url="https://bitbucket.org/zmtdummy/geojsondata/raw/ad675d6fd6e2256b365e79e785603c2ab454006b/password_protected_dataset.json",
#            dataset_user="zmtdummy",
#            dataset_password="zmtBremen1991",
#            public_access=False)

    def test_load_dataset_returns_status_code_200(self):
        response = self.client.get(reverse("load_dataset",
            kwargs={"pk": self.ds1.pk}))
        self.assertEqual(200, response.status_code)

#    def test_load_dataset_returns_status_code_200_PASSWORD_PROTECTED(self):
#        response = self.client.get(reverse("load_dataset",
#            kwargs={"pk": self.ds2.pk}))
#        self.assertEqual(200, response.status_code)

    def test_load_dataset_returns_content(self):
        response = self.client.get(reverse('load_dataset',
            kwargs={'pk': self.ds1.pk}))
        self.assertIn(b'properties', response.content)

