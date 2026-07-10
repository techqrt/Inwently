from biller_apps.places.models.country import Country
from biller_apps.places.models.states import States
from biller_apps.test_setup import TestSetUp
import datetime

class TestPlacesModels(TestSetUp):


    def test_get_country(self):
        Country.objects.create(country='India')

        countries = Country.get_country()

        self.assertEqual(len(countries), 2)
        self.assertEqual(countries[0]['country'], 'India')

    def test_get_states(self):

        States.objects.create(country='India', states='Uttar Pradesh')
        
        india_states = States.get_states(country='India')
        self.assertEqual(len(india_states), 2)
        self.assertEqual(india_states[0]['states'], 'Maharashtra')
       
    