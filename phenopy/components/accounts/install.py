import sys, os
import distutils.dir_util as dir_util

from account_generator import Account_Postgres_MD5_Salt_Generator

def install(**kw):
    sys.stdout.write('Installing Account component...\n')
    sys.stdout.write('Enter parent directory [%s]:'%(os.getcwd()))
    pdir = sys.stdin.readline().strip()
    pdir = (pdir == '' and os.getcwd() or pdir)
    sys.stdout.write('Enter account entity name [Account]:')
    acc_entity = sys.stdin.readline().strip()
    acc_entity = ( acc_entity == '' and 'Account' or acc_entity)
    
    print 'Creating directory...'
    path = os.path.join(pdir, acc_entity.lower())
    dir_util.mkpath( path  )
    gen = Account_Postgres_MD5_Salt_Generator(path=path, entity_name=acc_entity)
    print 'Generating files...'
    gen.generate_files()
    print path
    print '\n'.join( ('  '+ x for x in os.listdir(path)) )
    print 'Done.'

    
