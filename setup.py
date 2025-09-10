from setuptools import setup, find_packages

setup(
    name='cad_generator',
    version='0.1.1',
    author='mschongchulshin',
    author_email='saekomi5@korea.ac.kr',
    description='A fine-tuned LLM for generating CAD data from natural language.',
    long_description="See the GitHub repository for full details: https://github.com/mschongchulshin/finetuningcadtest20250909",
    long_description_content_type='text/markdown',
    url='https://github.com/mschongchulshin/finetuningcadtest20250909',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'torch',
        'accelerate',
        'huggingface_hub'
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
