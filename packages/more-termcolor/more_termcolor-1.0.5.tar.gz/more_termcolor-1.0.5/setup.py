"""Optional args (all False by default):
-n, --dry-run       doesn't actually call setup()
-ok                 before calling setup(), pretty-prints args and prompts user to confirm"""
from setuptools import find_packages, setup
import sys
import re

if sys.version_info < (3, 7):
    print(f"Python 3.7 and above required. current version: ", sys.version_info)
    exit(1)
from more_termcolor import util

packages = find_packages(exclude=["tests?", "*.tests*", "*.tests*.*", "tests*.*", ])
setup_args = dict(name='more_termcolor',
                  # https://packaging.python.org/tutorials/packaging-projects/
                  version='1.0.5',
                  description='Literally all colors, supporting multiple substring colors, convenience methods and full original termcolor compatability',
                  license='MIT',
                  author='Gilad Barnea',
                  author_email='giladbrn@gmail.com',
                  url='https://github.com/giladbarnea/more_termcolor',
                  packages=packages,

                  keywords=["termcolor", "color", "colors", "terminal", "ansi", "formatting"],

                  extras_require=dict(test=['pytest', 'ipdb']),
                  classifiers=[
                      # https://pypi.org/classifiers/
                      'Development Status :: 4 - Beta',
                      'Environment :: Console',
                      'Intended Audience :: Developers',
                      "License :: OSI Approved :: MIT License",
                      'Operating System :: OS Independent',
                      "Programming Language :: Python :: 3 :: Only",
                      'Topic :: Terminals',
    
                      ],
                  python_requires='>=3.7',
                  )

dry_run = False  # -n, [-]+dry[-_]?run
confirm = False  # [-]+ok
for arg in sys.argv[1:]:
    if arg == '-n' or re.fullmatch('^[-]+dry[-_]?run$', arg):
        dry_run = True
        sys.argv.remove(arg)
        continue
    if re.fullmatch('^[-]+ok$', arg):
        confirm = True
        sys.argv.remove(arg)
        continue
print(f'sys.argv[1:]: ', sys.argv[1:])
print(f'dry_run: ', dry_run, '\nconfirm: ', confirm)
if confirm:
    from pprint import pprint
    
    print('setup args:')
    pprint(setup_args)
    if not util.confirm():
        print('aborting')
        sys.exit()

if not dry_run:
    setup(**setup_args)
