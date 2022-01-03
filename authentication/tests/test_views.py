from .test_setup import TestSetUp                                                       # TestSetUp hami aafaile banayeko class ho
from ..models import User                                                               # . vannale current directory ma vanni bujincha vane .. vannale 1 directory bahira ko directory vanni bujincha


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)                                       # since when user data is not sent while registering the user we will surely get error or we can say 400 BAD Request response
        self.assertEqual(res.status_code, 400)                                          # response status code should be equal to 400

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")        # user register vaye or navaye pani response tw aaucha nai so response lai res vanni property ma rakheko # user register garna ko lagi user ko data in json format ma  post method ma pathauna parcha
        self.assertEqual(res.data['email'], self.user_data['email'])                    # hamile user_data batw pathayeko email address & register vai sake pachi response ma aayeko email address equal or same huna parcha
        self.assertEqual(res.data['username'], self.user_data['username'])              # hamile user_data batw pathayeko username & register vai sake pachi response ma aayeko username equal or same huna parcha
        self.assertEqual(res.status_code, 201)                                          # user registration vai sake pachi aayeko response ko status code 201 huna parcha

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")              # login garna vanda pahila user register vako huna parcha so tei vayera suru ma user registration gareko
        res = self.client.post(self.login_url, self.user_data, format="json")           # user login garda login credentioal or user data json format ma pathauna parcha
        self.assertEqual(res.status_code, 401)                                          # but user.is_verified lai True nagari or user lai verfiy nagari user login garna khojda kheri 401 response aauna parcha

    def test_user_can_login_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")   # suru ma user registration gareko & response ma user ko email & username aaucha
        email = response.data['email']                                                  # response ma aayeko email lai grab gareko
        user = User.objects.get(email=email)                                            # response ma aayeko email ko help batw particular user lai access gareko
        user.is_active = True                                                           # kunai user lai django le login garna facility dina cha vani sabai vanda pahila tes user ko is_active = True vako nai huna parcha .. tehi vayera email verification garda kheri user ko is_active lai pani True gareko cha so yaha testing garda pani True nai garnu paryo
        user.is_verified = True                                                         # user ko is_verified field ko value lai change garera True garayeko i.e user verify vayo vanera vanna khojeko
        user.save()                                                                     # user object or instance lai feri save gareko
        res = self.client.post(self.login_url, self.user_data, format="json")           # finally user lai login gareko
        self.assertEqual(res.status_code, 200)                                          # login successfull vayepachi response status code 200 aauna parcha
