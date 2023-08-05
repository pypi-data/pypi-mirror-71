from setuptools import setup, find_packages

setup(
    name='apievaluator',
    author='Filip Majetić',
    author_email='filip.majetic@fer.hr',
    version='0.0.1',
    description='Validate an API specification and run tests',
    keywords=['rest', 'api', 'testing', 'automated'],
    url='https://gitlab.com/fmajestic/api-evaluator',
    download_url='https://gitlab.com/fmajestic/api-evaluator/-/archive/v0.1.1/api-evaluator-v0.1.1.tar.gz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click',
                      'prance',
                      'pyyaml',
                      'requests',
                      ],
    entry_points={
        'console_scripts': ['apieval=apievaluator.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
