from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker                                                                    # faker package use garna ko lagi faker package install garna parcha
# Note :  faker class doesnot use real database .. it simple use fake or virtual database to run testing process

from authentication.models import User




class TestSetUp(APITestCase):                                                              # our custom TestSetUp class is inherting from inbuilt APITestCase class

    # Note: each test run huda kheri setUp() & tearDown() method run huncha
    def setUp(self):                                                                        # SetUp() inbuilt method ho jaslai hamile override gareko ho
        self.register_url = reverse('register')                                             # register_url vanni property ma user register garni url lai rakheko
        self.login_url = reverse('login')                                                   # login_url vanni propery ma user login garney url lai rakheko

        # self.fake = Faker()                                                                 # fake is the newsly created instance or object of Faker class

        # create fake dynamic user data using faker to test our api   .. hamile static user data pani test garna sakchau... tara hamro API realistic dynamic data sanga khelna saki rako cha ki nai vanera check garna ko lagi dynamic data rakheko
        # self.user_data = {                                                                  # user_data hamile auta dictionary create gareko jasma Faker batw automatic create vayeko dynamic data huncha
        #     'email': self.fake.email(),                                                     # fake email address create garcha yo statement le
        #     'username': self.fake.email().split('@')[0],                                    # fake email address lai @  ko thau ma split garera @ vanda agadi ko kura i.e username lai grab gareko
        #     'password': self.fake.email(),                                                  # password pani email address nai rakheko
        # }

        # using static user data for testing our api
        self.user_data = {
            'email': 'dhirajkafle553@gmail.com',
            'username': 'Dhiraj',
            'password': 'superuser',
        }

        return super().setUp()


    def tearDown(self):                                                                     # tearDown() pani inbuilt method ho
        return super().tearDown()
