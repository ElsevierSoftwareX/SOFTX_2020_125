import sys
import httplib
import urlparse
import urllib2
import socket
from glue import LDBDWClient

#
# =============================================================================
#
#                Library for DQSEGDB API Providing URL Functions 
#
# =============================================================================
#

certfile,keyfile=LDBDWClient.findCredential()

class HTTPSClientAuthConnection(httplib.HTTPSConnection):
  def __init__(self, host, timeout=None):
      httplib.HTTPSConnection.__init__(self, host, key_file=keyfile, cert_file=certfile)
      self.timeout = timeout # Only valid in Python 2.6

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
  def https_open(self, req):
      return self.do_open(HTTPSClientAuthConnection, req)


def getDataHttplib(url):
    """
    DEPRECATED!
    Optional fall back in case of failure in getDataUrllib2
    Takes a url such as:
    url="http://segdb-test-internal/dq/H1/DMT-SCIENCE/1/active?s=10&e=20"
    Returns JSON response from server
    """
    print "Warning: using function that my not work any more!"
    urlsplit=urlparse.urlparse(url)
    conn=httplib.HTTPConnection(urlsplit.netloc)
    conn.request("GET",'?'.join([urlsplit.path,urlsplit.query]))
    r1=conn.getresponse()
    if r1.status!=200:
        print "Return status code: %s, %s" % r1.status,r1.reason
        print url
        raise(urllib2.URLError)
    data1=r1.read()
    return data1

def getDataUrllib2(url,timeout=900,logger=None):
    socket.setdefaulttimeout(timeout)
    """
    Takes a url such as:
    url="http://segdb-test-internal/dq/dq/H1/DMT-SCIENCE/1/active?s=10&e=20"
    Returns JSON response from server
    Also handles https requests with grid certs (or proxy certs).
    """
    if logger:
        logger.debug("Beginning url call: %s" % url)
    try:
        if urlparse.urlparse(url).scheme == 'https':
            #print "attempting to send https query"
            #print certfile
            #print keyfile
            opener=urllib2.build_opener(HTTPSClientAuthHandler)
            #print opener.handle_open.items()
            request = urllib2.Request(url)
            output=opener.open(request)
        else:
            #print "attempting to send http query"
            output=urllib2.urlopen(url)
    except urllib2.HTTPError,e:
        #print e.read()
        print "Error accesing url: %s" % url
        print e.code
        #print e.reason
        print url
        print "May be handled cleanly by calling instance: raising error:"
        raise
    except urllib2.URLError,e:
        #print e.read()
        print "Error accesing url: %s" % url
        print e.reason
        try:
            type, value, traceback = sys.exc_info()
            print "Trying custom URLError."
            print url
            raise urllib2.URLError, ("Unable to get data",type,value),traceback
        except:
            print url
            raise
    if logger:
        logger.debug("Completed url call: %s" % url)
    return output.read()

def constructSegmentQueryURLTimeWindow(protocol,server,ifo,name,version,include_list_string,startTime,endTime):
    """
    Simple url construction method for dqsegdb server flag:version queries 
    including restrictions on time ranges.
    """
    url1=protocol+"://"+server+"/dq"
    url2='/'.join([url1,ifo,name,str(version)])
    # include_list_string should be a comma seperated list expressed as a string for the URL
    # Let's pass it as a python string for now?  Fix!!!
    start='s=%i' % startTime
    end='e=%i' % endTime
    url3=url2+'?'+start+'&'+end+'&include='+include_list_string
    return url3

def constructSegmentQueryURL(protocol,server,ifo,name,version,include_list_string):
    """
    Simple url construction method for dqsegdb server flag:version queries 
    not including restrictions on time ranges.
    """
    url1=protocol+"://"+server+"/dq"
    url2='/'.join([url1,ifo,name,version])
    url3=url2+'?'+'include='+include_list_string
    return url3

def constructVersionQueryURL(protocol,server,ifo,name):
    """
    Simple url construction method for dqsegdb server version queries. 
    """
    ## Simple url construction method:
    url1=protocol+"://"+server+"/dq"
    url2='/'.join([url1,ifo,name])
    return url2

def constructFlagQueryURL(protocol,server,ifo):
    """
    Simple url construction method for dqsegdb server flag queries. 
    """
    ## Simple url construction method:
    url1=protocol+"://"+server+"/dq"
    url2='/'.join([url1,ifo])
    return url2

def putDataUrllib2(url,payload,timeout=900,logger=None):
    """
    Wrapper method for urllib2 that supports PUTs to a url.
    """
    socket.setdefaulttimeout(timeout)
    #BEFORE HTTPS: opener = urllib2.build_opener(urllib2.HTTPHandler)
    opener=urllib2.build_opener(HTTPSClientAuthHandler)
    request = urllib2.Request(url, data=payload)
    request.add_header('Content-Type', 'JSON')
    request.get_method = lambda: 'PUT'
    if logger:
        logger.debug("Beginning url call: %s" % url)
    try:
        urlreturned = opener.open(request)
    except urllib2.HTTPError,e:
        #print e.read()
        print e.code
        #print e.reason
        #print urlreturned
        print url
        raise
    except urllib2.URLError,e:
        #print e.read()
        print e.reason
        #print urlreturned
        print url
        raise
    if logger:
        logger.debug("Completed url call: %s" % url)
    return url

def patchDataUrllib2(url,payload,timeout=900,logger=None):
    """
    Wrapper method for urllib2 that supports PATCHs to a url.
    """
    socket.setdefaulttimeout(timeout)
    #BEFORE HTTPS: opener = urllib2.build_opener(urllib2.HTTPHandler)
    opener=urllib2.build_opener(HTTPSClientAuthHandler)
    #print opener.handle_open.items()            
    request = urllib2.Request(url, data=payload)
    request.add_header('Content-Type', 'JSON')
    request.get_method = lambda: 'PATCH'
    if logger:
        logger.debug("Beginning url call: %s" % url)
    try:
        urlreturned = opener.open(request)
    except urllib2.HTTPError,e:
        #print e.read()
        print e.code
        #print e.reason
        print url
        raise
    except urllib2.URLError,e:
        #print e.read()
        print e.reason
        print url
        raise
    if logger:
        logger.debug("Completed url call: %s" % url)
    return url

