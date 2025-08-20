from setuptools import setup, find_packages

setup(
    name='job-market-analyzer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A project to analyze job market trends using AI and data analysis techniques.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/job-market-analyzer',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk',
        'spacy',
        'matplotlib',
        'seaborn',
        'jupyter',
        'notebook',
        'openai',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)