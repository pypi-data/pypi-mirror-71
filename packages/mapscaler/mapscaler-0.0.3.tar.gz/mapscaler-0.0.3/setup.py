from setuptools import setup
setup(
    name = 'mapscaler',
    packages = ['mapscaler'],
    package_data = {'mapscaler': ['geojson/us_counties.json', 'geojson/us_states.json'] },
    version = '0.0.3',
    license='gpl-3.0',
    description = 'Scale areas of a geopandas map by any property to create more intuitive and beautiful choropleth visualizations.',
    author = 'Greg Condit',
    author_email = 'conditg@gmail.com',
    url = 'https://github.com/user/conditg/mapscaler',
    download_url = 'https://github.com/conditg/mapscaler/archive/v0.0.3.tar.gz',
    keywords = ['DATA VISUALIZATION', 'MAP', 'CHOROPLETH', 'CARTOGRAM','MAP SCALER', 'GEOJSON'],
    install_requires=[
        'numpy',
        'geopandas',
        'shapely',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)


