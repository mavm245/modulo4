#!/usr/bin/env python
"Recovers your Firefox or Thunderbird passwords"

import base64
from collections import namedtuple
from ConfigParser import RawConfigParser, NoOptionError
from ctypes import (Structure, CDLL, byref, cast, string_at, c_void_p, 
    c_uint, c_ubyte, c_char_p)
from getpass import getpass
import logging
from optparse import OptionParser
import os
try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite
from subprocess import Popen, CalledProcessError, PIPE
import sys


LOGLEVEL_DEFAULT = 'warn'

log = logging.getLogger()
PWDECRYPT = 'pwdecrypt'

SITEFIELDS = ['id', 'hostname', 'httpRealm', 'formSubmitURL', 'usernameField', 'passwordField', 'encryptedUsername', 'encryptedPassword', 'guid', 'encType', 'plain_username', 'plain_password' ]
Site = namedtuple('FirefoxSite', SITEFIELDS)
'''The format of the SQLite database is:
(id                 INTEGER PRIMARY KEY,hostname           TEXT NOT NULL,httpRealm          TEXT,formSubmitURL      TEXT,usernameField      TEXT NOT NULL,passwordField      TEXT NOT NULL,encryptedUsername  TEXT NOT NULL,encryptedPassword  TEXT NOT NULL,guid               TEXT,encType            INTEGER);
'''



#### These are libnss definitions ####
class SECItem(Structure):
	_fields_ = [('type',c_uint),('data',c_void_p),('len',c_uint)]
	
class secuPWData(Structure):
	_fields_ = [('source',c_ubyte),('data',c_char_p)]

(PW_NONE, PW_FROMFILE, PW_PLAINTEXT, PW_EXTERNAL) = (0, 1, 2, 3)
# SECStatus
(SECWouldBlock, SECFailure, SECSuccess) = (-2, -1, 0)
#### End of libnss definitions ####


def get_default_firefox_profile_directory(dir='~/.mozilla/firefox'):
    '''Returns the directory name of the default profile
    
    If you changed the default dir to something like ~/.thunderbird,
    you would get the Thunderbird default profile directory.'''

    profiles_dir = os.path.expanduser(dir)
    profile_path = None

    cp = RawConfigParser()
    cp.read(os.path.join(profiles_dir, "profiles.ini"))
    for section in cp.sections():
        if not cp.has_option(section, "Path"):
            continue

        if (not profile_path or
            (cp.has_option(section, "Default") and cp.get(section, "Default").strip() == "1")):
            profile_path = os.path.join(profiles_dir, cp.get(section, "Path").strip())

    if not profile_path:
        raise RuntimeError("Cannot find default Firefox profile")

    return profile_path
    

def get_encrypted_sites(firefox_profile_dir=None):
    'Opens signons.sqlite and yields encryped password data'
    
    if firefox_profile_dir is None:
        firefox_profile_dir = get_default_firefox_profile_directory()
    password_sqlite = os.path.join(firefox_profile_dir, "signons.sqlite")
    query = '''SELECT id, hostname, httpRealm, formSubmitURL,
                      usernameField, passwordField, encryptedUsername,
                      encryptedPassword, guid, encType, 'noplainuser', 'noplainpasswd' FROM moz_logins;'''

    # We don't want to type out all the column from the DB as we have 
    ## stored them in the SITEFIELDS already. However, we have two 
    ## components extra, the plain usename and password. So we remove 
    ## that from the list, because the table doesn't have that column. 
    ## And we add two literal SQL strings to make our "Site" data 
    ## structure happy
    #queryfields = SITEFIELDS[:-2] + ["'noplainuser'", "'noplainpassword'"]
    #query = '''SELECT %s 
    #           FROM moz_logins;''' % ', '.join(queryfields)

    connection = sqlite.connect(password_sqlite)
    try:
        cursor = connection.cursor()
        cursor.execute(query)

        for site in map(Site._make, cursor.fetchall()):
          yield site
    finally:
        connection.close()

def decrypt(encrypted_string, firefox_profile_directory, password = None):
    '''Opens an external tool to decrypt strings
    
    This is mostly for historical reasons or if the API changes. It is 
    very slow because it needs to call out a lot. It uses the 
    "pwdecrypt" tool which you might have packaged. Otherwise, you 
    need to build it yourself.'''
    
    log = logging.getLogger('firefoxpasswd.decrypt')
    execute = [PWDECRYPT, '-d', firefox_profile_directory]
    if password:
        execute.extend(['-p', password])
    process = Popen(execute,
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate(encrypted_string)
    
    log.debug('Sent: %s', encrypted_string)
    log.debug('Got: %s', output)
    
    NEEDLE = 'Decrypted: "' # This string is prepended to the decrypted password if found
    output = output.strip()
    if output == encrypted_string:
        log.error('Password was not correct. Please try again without a '
                   'password or with the correct one')
    
    index = output.index(NEEDLE) + len(NEEDLE)
    password = output[index:-1] # And we strip the final quotation mark

    return password


class NativeDecryptor(object):
    'Calls the NSS API to decrypt strings'

    def __init__(self, directory, password = ''):
        '''You need to give the profile directory and optionally a 
        password. If you don't give a password but one is needed, you 
        will be prompted by getpass to provide one.'''
        self.directory = directory
        self.log = logging.getLogger('NativeDecryptor')
        self.log.debug('Trying to work on %s', directory)
        
        self.libnss = CDLL('libnss3.so')
        if self.libnss.NSS_Init(directory) != 0:
            self.log.error('Could not initialize NSS')

        # Initialize to the empty string, not None, because the password
        # function expects rather an empty string
        self.password = password = password or ''
        

        slot = self.libnss.PK11_GetInternalKeySlot()
        
        pw_good = self.libnss.PK11_CheckUserPassword(slot, c_char_p(password))
        while pw_good != SECSuccess:
            msg = 'Password is not good (%d)!' % pw_good
            print >>sys.stderr, msg
            password = getpass('Please enter password: ')
            pw_good = self.libnss.PK11_CheckUserPassword(slot, c_char_p(password))
            #raise RuntimeError(msg)

        # That's it, we're done with passwords, but we leave the old 
        # code below in, for nostalgic reasons.

        if password is None:
            pwdata = secuPWData()
            pwdata.source = PW_NONE
            pwdata.data = 0
        else:
            # It's not clear whether this actually works
            pwdata = secuPWData()
            pwdata.source = PW_PLAINTEXT
            pwdata.data = c_char_p (password) 
            # It doesn't actually work :-(

            
            # Now follow some attempts that were not succesful!
            def setpwfunc():
                # One attempt was to use PK11PassworFunc. Didn't work.
                def password_cb(slot, retry, arg):
                    #s = self.libnss.PL_strdup(password)
                    s = self.libnss.PL_strdup("foo")
                    return s
        
                PK11PasswordFunc = CFUNCTYPE(c_void_p, PRBool, c_void_p)
                c_password_cb = PK11PasswordFunc(password_cb)
                #self.libnss.PK11_SetPasswordFunc(c_password_cb)
                

            # To be ignored
            def changepw():                
                # Another attempt was to use ChangePW. Again, no effect.
                #ret = self.libnss.PK11_ChangePW(slot, pwdata.data, 0);
                ret = self.libnss.PK11_ChangePW(slot, password, 0)
                if ret == SECFailure:
                    raise RuntimeError('Setting password failed! %s' % ret)
        
        #self.pwdata = pwdata
    

    def __del__(self):
        self.libnss.NSS_Shutdown()
    

    def decrypt(self, string, *args):
        'Decrypts a given string'

        libnss =  self.libnss

        uname = SECItem()
        dectext = SECItem()        
        #pwdata = self.pwdata
        
        cstring = SECItem()
        cstring.data  = cast( c_char_p( base64.b64decode(string)), c_void_p)
        cstring.len = len(base64.b64decode(string))
        #if libnss.PK11SDR_Decrypt (byref (cstring), byref (dectext), byref (pwdata)) == -1:
        self.log.debug('Trying to decrypt %s (error: %s)', string, libnss.PORT_GetError())
        if libnss.PK11SDR_Decrypt (byref (cstring), byref (dectext)) == -1:
            error = libnss.PORT_GetError()
            libnss.PR_ErrorToString.restype = c_char_p
            error_str = libnss.PR_ErrorToString(error)
            raise Exception ("%d: %s" % (error, error_str))
	        
        decrypted_data = string_at(dectext.data, dectext.len)
	    
    	return decrypted_data
	
	
    def encrypted_sites(self):
        'Yields the encryped passwords from the profile'
        sites = get_encrypted_sites(self.directory)

        return sites


    def decrypted_sites(self):
        'Decrypts the encrypted_sites and yields the results'

        sites = self.encrypted_sites()
        
        for site in sites:
            plain_user = self.decrypt(site.encryptedUsername)
            plain_password = self.decrypt(site.encryptedPassword)
            site = site._replace(plain_username=plain_user,
                plain_password=plain_password)
            
            yield site


def get_firefox_sites_with_decrypted_passwords(firefox_profile_directory = None, password = None):
    'Old school decryption of passwords using the external tool'
    if not firefox_profile_directory:
        firefox_profile_directory = get_default_firefox_profile_directory()
    #decrypt = NativeDecryptor(firefox_profile_directory).decrypt
    for site in get_encrypted_sites(firefox_profile_directory):
        plain_user = decrypt(site.encryptedUsername, firefox_profile_directory, password)
        plain_password = decrypt(site.encryptedPassword, firefox_profile_directory, password)
        site = site._replace(plain_username=plain_user, plain_password=plain_password)
        log.debug("Dealing with Site: %r", site)
        log.info("user: %s, passwd: %s", plain_user, plain_password)
        yield site

def main_decryptor(firefox_profile_directory, password, thunderbird=False):
    'Main function to get Firefox and Thunderbird passwords'
    if not firefox_profile_directory:
        if thunderbird:
            dir = '~/.thunderbird/'
        else:
            dir = '~/.mozilla/firefox'
        firefox_profile_directory = get_default_firefox_profile_directory(dir)

    decryptor = NativeDecryptor(firefox_profile_directory, password)
    
    for site in decryptor.decrypted_sites():
        print site
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--directory", default=None,
                  help="the Firefox profile directory to use")
    parser.add_option("-p", "--password", default=None,
                  help="the master password for the Firefox profile")
    parser.add_option("-l", "--loglevel", default=LOGLEVEL_DEFAULT,
                  help="the level of logging detail [debug, info, warn, critical, error]")
    parser.add_option("-t", "--thunderbird", default=False, action='store_true',
                  help="by default we try to find the Firefox default profile."
                  " But you can as well ask for Thunderbird's default profile."
                  " For a more reliable way, give the directory with -d.")
    parser.add_option("-n", "--native", default=True, action='store_true',
                  help="use the native decryptor, i.e. make Python use "
                  "libnss directly instead of invoking the helper program"
                  "DEFUNCT! this option will not be checked.")
    parser.add_option("-e", "--external", default=False, action='store_true',
                  help="use an external program `pwdecrypt' to actually "
                    "decrypt the passwords. This calls out a lot and is dead "
                    "slow. "
                    "You need to use this method if you have a password "
                    "protected database though.")
    options, args = parser.parse_args()
    
    loglevel = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warn': logging.WARN, 'critical':logging.CRITICAL,
                'error': logging.ERROR}.get(options.loglevel, LOGLEVEL_DEFAULT)
    logging.basicConfig(level=loglevel)
    log = logging.getLogger()
    
    password = options.password

    if not options.external:
        sys.exit (main_decryptor(options.directory, password, thunderbird=options.thunderbird))
    else:
        for site in get_firefox_sites_with_decrypted_passwords(options.directory, password):
            print site
