from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='0imap',
    version='0.0.0',
    description='Simple IMAP data saver.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/0oio/0imap',
    author='Mindey',
    author_email='~@mindey.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'metaform',
        'metatype',
        'typer',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            '0imap=0imap.main:app'
        ],
    }
)
