from django.test import TestCase

# Create your tests here.
from .models import UploadIcons
from .forms import UploadIconModelForm

# Model Tests


# Form Tests
class UploadFormLable(TestCase):
    def test_form_label(self):
        form = UploadIconModelForm()
        self.assertEqual(form.fields['Title'].label,'Icon Title')