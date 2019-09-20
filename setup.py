from setuptools import find_packages, setup

VERSION = '1.0.0'

with open('requirements.txt', 'r') as f:
    requirements = [x.strip() for x in f if x.strip()]

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='influxable',
    packages=find_packages(),
    version=VERSION,
    license='MIT',
    description='A lightweight python ORM / ODM for InfluxDB',
    long_description=readme,
    author='Javid Mougamadou',
    author_email='javidjms0@gmail.com',
    url='https://github.com/Javidjms/influxable',
    download_url='https://github.com/Javidjms/influxable/archive/1.0.0.zip',
    keywords=['python', 'influxdb', 'odm', 'orm', 'driver', 'client'],
    install_requires=requirements,
    python_requires='>=3.0.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Source': 'https://github.com/Javidjms/influxable',
    },
)
