from django.db import models
from HTMLParser import HTMLParser

class Viewer(models.Model):
    jtv_handle = models.CharField(max_length=64)
    sc2_name = models.CharField(max_length=32)
    sc2_charcode = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    
    JTV_COOKIE_NAME = '_jtv3_session_id'
    JTV_INITIAL_PAGE = 'http://www.justin.tv/user/login'
    JTV_LOGIN_PAGE = 'http://www.justin.tv/login'
    JTV_SUBS_PAGE = 'http://www.justin.tv/settings?section=purchases&subsection=subscriptions'
    
    def verify(self, password):
        import urllib2, re
        from urllib import urlencode
        
        # get the authenticity token and session id from JTV
        url = Viewer.get_jtv_url(self.JTV_INITIAL_PAGE)
        if url is None:
            return False
        cookie = url.info().getheader('set-cookie')
        html = url.read()
        url.close()
        
        session_id = self.get_value_from_header(cookie, self.JTV_COOKIE_NAME)
        if session_id is None:
            return False
        
        pattern = re.compile('<input(.*)authenticity_token(.*)value=\"(.*)\"(.*)>')
        match = re.search(pattern, html)
        
        if not match:
            return False
        
        auth_token = match.group(3)
        
        # send login request
        req = urllib2.Request(self.JTV_LOGIN_PAGE)
        req.add_header('Cookie', cookie)
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        req.add_header('Referrer', self.JTV_INITIAL_PAGE)
        req.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
        data = {
            'authenticity_token':   auth_token,
            'user[login]':          self.jtv_handle,
            'user[password]':       password,
            'commit':               'Sign In'
        }
        
        url = Viewer.get_jtv_url(req, data)
        cookie = url.info().getheader('set-cookie')
        url.close()
        
        cookie = ''.join([cookie, '; ', self.JTV_COOKIE_NAME, session_id])
        req = urllib2.Request(self.JTV_SUBS_PAGE)
        req.add_header('Cookie', cookie)
        url = Viewer.get_jtv_url(req)
        html = url.read()
        url.close()
        
        pattern = re.compile("<table class='subscriptions_table'>(.*)</table>", re.DOTALL)
        match = re.search(pattern, html)
        
        if not match:
            return False
        
        return self.parse_subs(match.group(1))
        
    def parse_subs(self, content):
        import re
        pattern = re.compile('<tr>(.*?)</tr>', re.DOTALL)
        subs = re.split(pattern, content.strip())
        
        if not subs:
            return False

        for i in range(len(subs)):
            print subs[i]
            
        return False
        
    def __unicode__(self):
        return ''.join([self.jtv_handle, ' - ', self.sc2_name, '.', str(self.sc2_charcode)])
        
    @staticmethod
    def get_value_from_header(header_str, key):
        params = header_str.split('; ')
        for i in range(len(params)):
            args = params[i].split('=')
            if args[0] == key:
                return args[1]
        
        return None
        
    @staticmethod
    def get_jtv_url(req, data=None):
        import urllib2
        from urllib import urlencode
        
        try:
            if data is not None:
                data = urlencode(data)
                
            return urllib2.urlopen(req, data)
        except:
            return None

class SubsParser(HTMLParser):
    def __init__(self):
        self.verified = False
        HTMLParser.__init__(self)
        
    def feed(self, data):
        HTMLParser.feed(self, data)
        print data
        
    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            pass
    
class ViewerSubmission(models.Model):
    viewer = models.ForeignKey(Viewer)
    submit_time = models.DecimalField(max_digits=15, decimal_places=3)
    
    def __unicode__(self):
        from time import time
        from decimal import Decimal
        time_ago = Decimal(str(time())) - self.submit_time
        return ''.join([str(time_ago), ' seconds ago'])