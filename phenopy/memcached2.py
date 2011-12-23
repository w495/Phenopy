from decorators import generic_decorator
from misc import any_class
import memcache
import cPickle, sys, os, random
import md5

class settings(object):
    url = '127.0.0.1:11211'
    enable_cache = True
    profile = ""
    tagrefs_ttl = 3600

#FIXME: remove hardcode
keys_client = memcache.Client([settings.url], debug=0)
data_client = memcache.Client([settings.url], debug=0)

class memcached(generic_decorator):
    def __call__(self, cache_key, expire=0):
        res = _cache.get(cache_key)
        
        if not res:
            res = self.orig_func(**self.func_kwargs) or {}
            _cache.set(cache_key, res, expire)
        
        return res

class argcached(generic_decorator):
    def __call__(self, cache_keys=[], expire=0):
	saved_params = self.func_kwargs
	if not settings.enable_cache:
	    return self.orig_func(**saved_params) or {}

	#print "ARGCACHED %s\n"%str(self.orig_func.__name__)
	key = ""
	if len(cache_keys):
	    keynames = cache_keys
	else:
	    keynames = saved_params.keys()
	keynames.sort()
        for p in keynames:
		if (p in saved_params) and (p != 'self'):
    		    val = saved_params[p]
		    try:
    	    	        val.__iter__
	    		val.sort()
		        for o in val:
		    	    key = key + str(get_tagref(p, o))
    		    except:
		        key = key + str(get_tagref(p, val))

        #print "ARGCACHED UNHASHED KEY = %s\n"%key
	key = self.orig_func.__name__ + "_" + md5.md5(key).hexdigest()
        #key = key + "__" + settings.profile
        res = data_client.get(key)
        #print "ARGCACHED HASHED KEY_TO_READ = %s\n"%key
        #print "ARGCACHED GOT VALUE = %s\n"%str(res)


        if not res:
            res = self.orig_func(**saved_params) or {}
            #print "ARGCACHED HASHED KEY_TO_WRITE = %s\n"%key
            data_client.set(key, res, expire)
            #print "ARGCACHED SET VALUE = %s\n"%str(res)
	    res2 = data_client.get(key)
            #print "GOT VALUE BACK = %s\n"%str(res2)

        return res

def get_tagref(subkey_name, subkey_value):
    tagref_key = "tr_%s_%s_%s"%(md5.md5(str(subkey_name)).hexdigest(), md5.md5(str(subkey_value)).hexdigest(), md5.md5(str(settings.profile)).hexdigest())
    #print "ARGCACHED FOR KEY: %s\n"%tagref_key
    tagref = keys_client.get(tagref_key)
    #print "ARGCACHED GOT STORED TAGREF = %s\n"%str(tagref)
    if not tagref:
	tagref = (str(subkey_name), str(subkey_value), str(int(random.random()*999999)))
	keys_client.set(tagref_key, tagref, settings.tagrefs_ttl)
    #print "ARGCACHED RETURED TAGREF = %s\n"%str(tagref)
    return tagref

def touch_tagref(subkey_name, subkey_value):
    if not settings.enable_cache:
	return False
    try:
	subkey_value.__iter__
	for v in subkey_value:
	    touch_tagref_1(subkey_name, v)
    except:
	touch_tagref_1(subkey_name, subkey_value)

def touch_tagref_1(subkey_name, subkey_value):
    tagref_key = "tr_%s_%s_%s"%(md5.md5(str(subkey_name)).hexdigest(), md5.md5(str(subkey_value)).hexdigest(), md5.md5(str(settings.profile)).hexdigest())
    #print "ARGCACHED FOR KEY: %s\n"%tagref_key
    tagref = keys_client.get(tagref_key)
    #print "ARGCACHED GOT STORED TAGREF = %s\n"%str(tagref)
    if not tagref:
        tagref = (str(subkey_name), str(subkey_value), str(int(random.random()*999999)))
    else:
	(_,_,old_version)=tagref
	tagref = (str(subkey_name), str(subkey_value), str(int(old_version)+1))
    #print "ARGCACHED TOUCHED TAGREF = %s\n"%str(tagref)
    keys_client.set(tagref_key, tagref, settings.tagrefs_ttl)
    tagref = keys_client.get(tagref_key)
    #print "ARGCACHED GOT BACK TAGREF = %s\n"%str(tagref)
    return True
