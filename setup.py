from setuptools import setup, find_packages

# requirements.txt ���� �б�
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cad_generator',
    version='0.1.0',
    author='mschongchulshin',  # GitHub ����� �̸����� ����
    author_email='saekomi5@korea.ac.kr',  # �������ֽ� �̸���
    description='A fine-tuned LLM for generating CAD data from natural language.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mschongchulshin/finetuningcadtest20250909',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)