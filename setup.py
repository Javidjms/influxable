from setuptools import find_packages, setup

setup(
    name='influxable',
    packages=find_packages(),
    version='0.0.1-alpha.1',
    license='MIT',
    description='A lightweight python ORM / ODM for InfluxDB',
    author='Javid Mougamadou',
    author_email='javidjms0@gmail.com',
    url='https://github.com/Javidjms/influxable',
    download_url='https://github.com/Javidjms/influxable/archive/0.0.1-alpha.tar.gz',
    keywords=['python', 'influxdb', 'odm', 'orm', 'driver', 'client'],
    install_requires=[
      'requests==2.22.0',
      'wheel==0.33.4',
    ],
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
