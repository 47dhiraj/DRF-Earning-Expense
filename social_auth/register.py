
from django.contrib.auth import authenticate
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings



def generate_username(name):                                                                        # name argument ma social auth provider server le pathayeko full name aaucha

    username = "".join(name.split(' ')).lower()                                                     # full name lai kaat chaat garera first name grab gareko
    if not User.objects.filter(username=username).exists():                                         # yedi tyo name ko user name hamro system ma pahilaii exist gardain vani
        return username                                                                             # kei nagari username return gardiye vai halyo
    else:                                                                                           # yedi tyo name ko user name hamro system ma pahilaii exist cha vani
        random_username = username + str(random.randint(0, 1000))                                   # username pachadi random integer rakheko..
        return generate_username(random_username)                                                   # kahile kei mathi ko random number same generate vayera same name username bandina sakcha.. tei vayera jahile samma alag naam aaudaina teti bela samma else part run huncha & generate_username() recrursive call huncha & finally jaba hamro system mai navako username aaucha ani mathi ko if part run huncha & tehi batw username return huncha  ... yesto condition bahut rare huncha.. tara huna sakcha vanera yesto preventive logic use gareko ho


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():                                                                 # yedi tyo email vayeko or gareko hamro system ma pahilai registered user cha vani

        if provider == filtered_user_by_email[0].auth_provider:                                         # yedi auth provider pani same cha vani

            registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)                # yo line le login garaucha

            return {
                'username': registered_user.username,                                                   # models.py ko current user object ko username field ko value lai grab gareko
                'email': registered_user.email,                                                         # models.py ko current user object ko email field ko value lai grab gareko
                'tokens': registered_user.tokens()                                                      # models.py ko tokens() vanni definition lai call gareko & uta batw token as a dictionary return huncha
            }

        else:                                                                                           # tyo email gareko or vayeko user system ma chai pahila cha but hamro system ma vayeko auth_provider ma arko kunrai social provider batw login garna khoji rako cha vani testo bela ko case ho
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)   # suru ma hamro system register huda jun auth provider batw login vako thyo tei provider batw nai login gar vanne message dincha yo line le

    else:                                                                                               # yedi tyo email gareko hamro system ma pahilai user chaina vani (i.e for new unregistered user)
        user = {'username': generate_username(name), 'email': email, 'password': settings.SOCIAL_SECRET}        # generate_username() vanni method call gareko cha jasle server batw response ma aayeko full name lai kaat chaat garera first name matra return garcha
        user = User.objects.create_user(**user)                                                         # new user create gareko
        user.is_verified = True
        user.is_active = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=settings.SOCIAL_SECRET)                           # .env file ma SOCIAL_SECRET key garaune.. and sabai social site batw register garney userko ko password same rakhdine logic use gareko cha... login garda pani sabai social login garne same password ... tara production field ma chai yesto garnu hudaina
        return {
            'email': new_user.email,                                                                    # models.py batw current user object ko email field ko value lai grab gareko cha
            'username': new_user.username,                                                              # models.py batw current user object ko username field ko value lai grab gareko cha
            'tokens': new_user.tokens()                                                                 # models.py ko tokens() vanni definition lai call gareko & uta batw token as a dictionary return huncha
        }
