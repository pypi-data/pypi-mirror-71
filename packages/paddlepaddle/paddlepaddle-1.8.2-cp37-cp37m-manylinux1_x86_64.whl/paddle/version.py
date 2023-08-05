# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.8.2'
major           = '1'
minor           = '8'
patch           = '2'
rc              = '0'
istaged         = True
commit          = '0b3f6265819d9ee0c0e08f76ed568e2057a7aa0e'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
