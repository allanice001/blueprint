from setuptools import setup, find_packages

setup(name='blueprint',
      version='4.0.0',
      description='reverse engineer server configuration',
      author='Dr@g0nM@5t3r',
      author_email='dragonmaster@acmeaws.com',
      url='http://blueprint.acmeaws.com/',
      packages=find_packages(),
      requires=['boto'],
      scripts=['bin/blueprint',
               'bin/blueprint-apply',
               'bin/blueprint-create',
               'bin/blueprint-destroy',
               'bin/blueprint-diff',
               'bin/blueprint-git',
               'bin/blueprint-list',
               'bin/blueprint-prune',
               'bin/blueprint-pull',
               'bin/blueprint-push',
               'bin/blueprint-rules',
               'bin/blueprint-show',
               'bin/blueprint-show-files',
               'bin/blueprint-show-ignore',
               'bin/blueprint-show-packages',
               'bin/blueprint-show-services',
               'bin/blueprint-show-sources',
               'bin/blueprint-split',
               'bin/blueprint-template'],
      license='BSD',
      zip_safe=False

      )