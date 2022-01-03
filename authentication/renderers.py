from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):                                                         # hamile banayeko custom UserRenderer class le JSONRenderer lai inherit gareko cha
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):                        # overriding inbuilt render method
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        return response
