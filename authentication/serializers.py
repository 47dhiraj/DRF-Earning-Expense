from rest_framework import serializers
from .models import User

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from validate_email import validate_email

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)                      # password ko kura database ma matra halincha.. database batw fetch garinna i.e frontend ma dekhaidaina so tehi vayera fetch garna namilos vanera write_only = True gareko

    default_error_messages = {'username': 'The username should only contain alphanumeric characters'}

    email_error_messages = {'email': 'Enter a valid real email address.'}

    class Meta:
        model = User                                                                                    # Custom User model
        fields = ['email', 'username', 'password']                                                      # jun jun field ko data lai serialize garne ho tei tei field lai yaha lekhni

    
    def validate(self, attrs):                                                                          # serializers ko inbuilt validate() method lai override gareko
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():                                                                      # isalnum() method le alpha numeric ho ki nai vanera check garcha
            raise serializers.ValidationError(self.default_error_messages)

        is_valid = validate_email(email_address=email, check_format=True, check_blacklist=True, check_dns=True, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host='my.host.name', smtp_from_address='my@from.addr.ess')
        if is_valid == False:
            raise serializers.ValidationError(self.email_error_messages)

        return attrs                                                                                    # returning attributes or fields


    
    def create(self, validated_data):                                                                   # serializers ko inbuilt create() method lai override gareko
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)                                                                           # validated_data json format ma auncha but database ma data save garda model instance or as  a object ko rupma data save garnu parcha tesailey yo line le josn data lai model instance ma lai jancha.
        if password is not None:
            instance.set_password(password)                                                             # set_password method django ko inbuilt method ho... yesle paswword encryption gacha.
        instance.save()
        return instance

        # ALTERNATIVE CODE FOR CREATING A NEW USER
        # return User.objects.create_user(**validated_data)                                             # password thik cha ki nai check nai nagari autai line ma yesari user create pani garna sakincha .. tara tyo ramro kura haina


class EmailVerificationSerializer(serializers.ModelSerializer):                                         # khas yo serializer lai use nai nagari pani email tw verify garna sakincha... but yedi swagger ui batw pani garna milos vanera yesari serializer nai banayeko
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)                                        # yesari serializers.EmailField garyo vani front end batw yedi email halni thau ma aru nai kei kura halyo vani... serializer le nai request pass huna didaina i.e Invalid Email Field yesto response dincha front end ma.. i.e model le check garnai parena.. serialization mai check vayo invalid email field vanera
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)                      # NOTE : yedi modesl.py ma kunai field lai write_only = True gareko cha vani tyo field lai serializer.py ma pani write_only = True nai garna parcha... natra vani sabbai kura thik huda hudai pani error aaucha .. # write_only = True vaneko front end batw matra data line ho but front end tira display garne haina vani write_only = True ko use garincha
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)                      # user le login garda username nai provide garna namilos vanera read_only = True gareko ho
    tokens = serializers.SerializerMethodField()                                                        # by default SerializerMethodField read_only = True nai huncha so lekhi rakhna pardaina # Note : SerializerMethodField() banayo vani tyo field ko function pani banayera value return garne tarikalai override garna sakincha

    def get_tokens(self, obj):                                                                          # yo line ko object le current serialized instance vanni bujaucha # yo get_tokens() definition vannale tokens SerializerMethodField method lai override gareko vanni bujaucha, yo definition batw return vayeko data tokens vanni SerializerMethodField ma nai huncha
        user = User.objects.get(email=obj['email'])                                                     # obj['email'] vannale obj dictionary ko email vanni key lai grab gareko
        return {                                                                                        # dictionary return gareko
            'access': user.tokens()['access'],                                                          # models.py ko tokens() vanni method lai call garera uta batw return vayeko dictionary ko access key ko string lai grab gareko
            'refresh': user.tokens()['refresh']                                                         # models.py ko tokens() vanni method lai call garera uta batw return vayeko dictionary ko refresh key ko string lai grab gareko
        }


    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self, attrs):                                                                          # overriding the serializer's inbuilt validate() method
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)                                             # authenticate() method ma email & password halesi yedi authenticate user ho vani user object dincha.. yedi authenticate user haina vani user object didaina

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':      # hamro system ma email exist garera matra vayena ni, hamro system ma vayeko provider batw nai login gareko huna paryo .. arko provider batw login gareko cha vani .. user authenticate vaye pani testo user lai AuthenticationFailed garaune kaam gareko
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)


        if not user:                                                                                    # yedi user object vetiyana vani
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:                                                                          # yedi user is_active = True chaina vani
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:                                                                        # yedi user is_verified = True chaina vani
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return (user)

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Token is expired or invalid') }

    def validate(self, attrs):
        self.token = attrs['refresh']                                       
        return attrs                                                        


    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()                            
        except TokenError:
            self.fail('bad_token')                                         

            # Alternative Code
            # raise serializers.ValidationError('Token is expired or invalid')