from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='Quadbot',
      version='1.0',
      description='multiplatform chatbot',
      long_description=readme(),
      classifiers=['License :: OSI Approved :: MIT',
                   'Programming Language :: Python :: 3.5+',
                   'Topic :: Chat Bot'],
      keywords='chatbot search',
      url='http://github.com/wlgranados/quadbot',
      author='William Granados',
      author_email='me@wgma.ca',
      license='MIT',
      packages=['venv'],
      platforms=['deb', 'rpm'],
      install_requires=[
          'PyYAML',
          'websocket',
          'requests',
          'simplejson',
          'websocket-client',
          'pylatex',
          'pyimgur',
          'markdown',
          'pytest'
      ],
      include_package_data=True,
      zip_safe=False)
