import requests
import json
from datetime import datetime

# https://github.com/add-ons/plugin.video.vrt.nu/blob/master/resources/lib/tokenresolver.py
_SSO_INIT_URL = 'https://www.vrt.be/vrtnu/sso/login?scope=openid,mid'
_SSO_LOGIN_URL = 'https://login.vrt.be/perform_login'
_SSO_REFRESH_URL = 'https://www.vrt.be/vrtnu/sso/refresh'
_SSO_TOKEN_URL = 'https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v2/tokens'

class VRT:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.sesssion = requests.Session()
        redirectUrl = self._get_login_info(email,password)['redirectUrl']
        self._get_token(redirectUrl)
        self.player_token = self.get_player_token()
        
    def _post_request(self,url, data={}, headers={}):
        return self.sesssion.post(url, data=data, headers=headers)

    def _get_request(self,url, headers={}):
        return self.sesssion.get(url, headers=headers)

    def _get_session_token(self,key):
        return self.sesssion.cookies.get(key)

    def _init_login(self):
        self.sesssion.get(_SSO_INIT_URL)

    def _get_login_info(self,email,password):
        self._init_login()
        oidcxsrf = self._get_session_token('OIDCXSRF')
        session_token = self._get_session_token('SESSION')

        headers = {
            'Content-Type': 'application/json',
            'OIDCXSRF': oidcxsrf,
            'Cookie': 'SESSION={}; OIDCXSRF={}'.format(session_token, oidcxsrf),
        }

        data = {"loginID":email,"password":password,"clientId":"vrtnu-site"}

        result = self._post_request(_SSO_LOGIN_URL,json.dumps(data).encode(),headers)
        if result.status_code == 200:
            return result.json()
        elif result.text != "":
            return result.json()['error']
        else:
            print(result.status_code)

    def _get_token(self,redirectUrl):
        oidcstate = self._get_session_token('oidcstate')
        session_token = self._get_session_token('SESSION')

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'SESSION=' + session_token + '; oidcstate=' + oidcstate,
        }

        response = self._get_request(redirectUrl,headers)
        return response
    
    def _generate_playerinfo(self):
        import time
        from json import dumps
        import base64
        import hmac
        import hashlib
        import re

        playerinfo = None
        data = None

        # Get data from player javascript
        player_url = 'https://player.vrt.be/vrtnu/js/main.js'
        crypt_data = None
        while not crypt_data:
            response = self._get_request(player_url)
            if response:
                data = response.text

                if data:
                    # Extract JWT key id and secret
                    crypt_rx = re.compile(r'atob\(\"(==[A-Za-z0-9+/]*)\"')
                    crypt_data = re.findall(crypt_rx, data)
                    if not crypt_data:
                        # Try redirect
                        redirect_rx = re.compile(r"'([a-z]+\.[a-z0-9]{20}\.js)';")
                        redirect_path = re.search(redirect_rx, data)
                        if redirect_path:
                            player_url = '{}/{}'.format(player_url[:player_url.rfind('/')], redirect_path.group(1))
                        else:
                            return playerinfo

        kid_source = crypt_data[0]
        secret_source = crypt_data[-1]
        kid = base64.b64decode(kid_source[::-1]).decode('utf-8')
        secret = base64.b64decode(secret_source[::-1]).decode('utf-8')

        # Extract player version
        player_version = '3.1.1'
        pv_rx = re.compile(r'playerVersion:\"(\S*)\"')
        match = re.search(pv_rx, data)
        if match:
            player_version = match.group(1)

        # Generate JWT
        segments = []
        header = {
            'alg': 'HS256',
            'kid': kid
        }
        payload = {
            'exp': time.time() + 1000,
            'platform': 'desktop',
            'app': {
                'type': 'browser',
                'name': 'Firefox',
                'version': '114.0'
            },
            'device': 'undefined (undefined)',
            'os': {
                'name': 'Linux',
                'version': 'x86_64'
            },
            'player': {
                'name': 'VRT web player',
                'version': player_version
            }
        }
        json_header = dumps(header).encode()
        json_payload = dumps(payload).encode()
        segments.append(base64.urlsafe_b64encode(json_header).decode('utf-8').replace('=', ''))
        segments.append(base64.urlsafe_b64encode(json_payload).decode('utf-8').replace('=', ''))
        signing_input = '.'.join(segments).encode()
        signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
        segments.append(base64.urlsafe_b64encode(signature).decode('utf-8').replace('=', ''))
        playerinfo = '.'.join(segments)
        return playerinfo
    
    def refresh_token(self):
        refresh_token = self._get_session_token('vrtnu-site_profile_rt')

        headers = {'Cookie': 'vrtnu-site_profile_rt=' + refresh_token}

        response = self._get_request(_SSO_REFRESH_URL,headers)
        if response.status_code == 200:
            self.token_expires = self._get_session_token('vrtnu-site_profile_et')
        else:
            print(response.status_code)
    

    def get_player_token(self):
        self.token_expires = self._get_session_token('vrtnu-site_profile_et')
        # get unix timestamp from datetime
        now = int(datetime.now().timestamp()*1000)
        # check if token is still valid
        if now > int(self.token_expires):
            self.refresh_token()

        headers = {'Content-Type': 'application/json'}

        headers = {'Content-Type': 'application/json'}
        playerinfo = self._generate_playerinfo()
        payload = {
            'playerInfo': playerinfo
        }

        videotoken = self._get_session_token('vrtnu-site_profile_vt')
        payload['identityToken'] = videotoken
        data = json.dumps(payload).encode()

        # make a post request to get the player token
        response = self._post_request(_SSO_TOKEN_URL,headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['vrtPlayerToken']
        else:
            print(response.status_code)
        