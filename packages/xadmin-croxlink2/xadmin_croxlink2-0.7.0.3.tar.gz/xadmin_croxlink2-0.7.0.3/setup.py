# coding=utf-8
#!/usr/bin/env python
from io import open
from setuptools import setup
# version_tuple = __import__('xadmin').VERSION
# version = ".".join([str(v) for v in version_tuple])

setup(
    name='xadmin_croxlink2',
    version='0.7.0.3',
    description='Drop-in replacement of Django admin comes with lots of goodies, fully extensible with plugin support, pretty UI based on Twitter Bootstrap.',
#     long_description=open('README.rst', encoding='utf-8').read(),
#     long_description_content_type="text/x-rst",
    author='Croxlink',
    author_email='developer@croxlink.com',
    license=open('LICENSE', encoding='utf-8').read(),
    url='http://www.croxlink.com',
    download_url='https://github.com/CROXLINK/django-xadmin/archive/django2.zip',
    packages=['xadmin', 'xadmin.migrations', 'xadmin.plugins', 'xadmin.templatetags', 'xadmin.views'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'django>=2,<3',
        'django-crispy-forms>=1.6.0',
        'django-reversion>=2.0.0',
        'django-formtools>=1.0',
        'httplib2>=0.9.2',
        'future',
        'six'
    ],
    extras_require={
        'Excel': ['xlwt', 'xlsxwriter'],
        'Reversion': ['django-reversion>=2.0.0'],
    },
    zip_safe=False,
    keywords=['admin', 'django', 'xadmin', 'bootstrap'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Programming Language :: JavaScript",
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
