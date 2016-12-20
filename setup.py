# coding: utf-8


# import pip.download

from setuptools import setup, find_packages
# from pip.req import parse_requirements
# from pip.index import PackageFinder

from boorstat import __name__ as MODULE

# pip_session = pip.download.PipSession()
# package_finder = PackageFinder([], None, session=pip_session)
# requirements = list(parse_requirements('requirements.txt', package_finder,
#                                        session=pip_session))

if __name__ == '__main__':
    setup(
        name='boorstat',
        version='0.0.1',
        description='Boor stat',
        long_description=open('README.md').read(),
        author='boorstat',
        author_email='boorstat@gmail.com',
        packages=[MODULE] + ['.'.join((MODULE, e)) for e in
                             find_packages(MODULE)],
        include_package_data=True,
        url='https://boorstat.github.io',
        install_requires=[
            'requests',
            'cached-property',
            'roman'],
        # dependency_links=['/'.join((package_finder.index_urls[0].rstrip('/'),
        #                             req.name)) for req in requirements],
    )
