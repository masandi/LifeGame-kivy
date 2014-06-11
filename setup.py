
from setuptools import setup, find_packages

setup(
        name='pylife',
        version='0.1.0',
        description='Conway\'s Game of Life with kivy',
        author='yukirin',
        author_email='standupdown@gmail.com',
        url='https://github.com/yukirin/LifeGame-kivy',
        license='MIT',
        keywords=['python', 'game', 'life game', 'kivy'],
        zip_safe=False,
        platforms=['Linux'],
        packages=find_packages(),
        package_data={'pylife': ['lifegame*.*']},
        classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Development Status :: 4 - Beta',
          'Operating System :: POSIX :: Linux',
          'Natural Language :: Japanese',
          'License :: OSI Approved :: MIT License',
          'Topic :: Games/Entertainment'
            ],
        install_requires = ['kivy'],
        entry_points={
            'gui_scripts': ['pylife = pylife.main:run']
            },
        )


