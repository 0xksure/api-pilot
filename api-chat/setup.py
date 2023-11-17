from setuptools import setup,find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.md")
requirements = read_requirements("requirement.txt")


setup(
    name='api_assistant',
    version='0.3.0',
    packages=find_packages(
        where=".",
        include=["api_assistant","common","openai"]
    ),
    description='An OpenAI assistant that can be used on top of a OpenAI functions IDL.',
    long_description_content_type="text/markdown",
    license = "MIT license",
    long_description=long_description,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'api-chat = api_assistant.main:main',
        ],
    },
)