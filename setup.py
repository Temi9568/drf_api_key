from setuptools import setup, find_packages

setup(
    name='drf_api_key',
    version='0.1.0', 
    description='Django rest library for creating, managing and securing API keys',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/temi9568/drf_api_key',  
    author='Temi Olatunji',
    author_email='temiolatunji95@gmail.com',
    license='MIT',  
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
    include_package_data=True,
    zip_safe=False
)