from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'kombu'
]

setup(
    name='utilitarian-queue-consumer',
    version='0.0.1dev',
    python_requires='~=3.6',
    description="A micro framework for writing consumers of AMR-UM or other AMQP messages.",
    long_description=readme + '\n\n' + history,
    author="Henrik Palmlund Wahlgren @ Palmlund Wahlgren Innovative Technology AB",
    author_email='henrik@pwit.se',
    url='https://www.pwit.se',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,

    license='BSD 3-Clause License',
    zip_safe=False,
    keywords='',
    classifiers=[

    ],
)