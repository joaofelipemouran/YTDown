from setuptools import setup

APP=['main.py']

OPITIONS = {
    'argv_emulation':True
}

setup( 
    app=APP,
    opitions={'py2app':OPITIONS },
    set_requires=['py2app']
    )
