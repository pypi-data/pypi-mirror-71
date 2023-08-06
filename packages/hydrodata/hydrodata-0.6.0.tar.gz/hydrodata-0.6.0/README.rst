.. image:: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/hydrodata_logo_text.png
    :target: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/hydrodata_logo_text.png
    :align: center

|

.. image:: https://img.shields.io/pypi/v/hydrodata.svg
    :target: https://pypi.python.org/pypi/hydrodata
    :alt: PyPi

.. image:: https://codecov.io/gh/cheginit/hydrodata/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/cheginit/hydrodata
    :alt: CodeCov

.. image:: https://github.com/cheginit/hydrodata/workflows/build/badge.svg
    :target: https://github.com/cheginit/hydrodata/actions?query=workflow%3Abuild
    :alt: Github Actions

.. image:: https://readthedocs.org/projects/hydrodata/badge/?version=latest
    :target: https://hydrodata.readthedocs.io/en/latest/?badge=latest
    :alt: ReadTheDocs

|

.. image:: https://www.codefactor.io/repository/github/cheginit/hydrodata/badge/develop
   :target: https://www.codefactor.io/repository/github/cheginit/hydrodata/overview/develop
   :alt: CodeFactor

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://zenodo.org/badge/237573928.svg
    :target: https://zenodo.org/badge/latestdoi/237573928
    :alt: Zenodo


-----------------

Features
--------

Hydrodata is a python library designed to aid in watershed analysis. It provides easy and consistent access to a handful of hydrology and climatology databases with some helper functions for visualization. Currently, the following data retrieval services are supported:

* `NLDI <https://labs.waterdata.usgs.gov/about-nldi/>`_ and `NHDPlus V2 <https://www.usgs.gov/core-science-systems/ngp/national-hydrography/national-hydrography-dataset?qt-science_support_page_related_con=0#qt-science_support_page_related_con>`_ for vector river network, catchments, and other NHDPlus data.
* `Daymet <https://daymet.ornl.gov/>`__ for climatology data, both single pixel and gridded
* `SSEBop <https://earlywarning.usgs.gov/ssebop/modis/daily>`_ for daily actual evapotranspiration, both single pixel and gridded
* `NLCD 2016 <https://www.mrlc.gov/>`__ for land cover, land use (some utilities are available for analysing and plotting the cover data)
* `NWIS <https://nwis.waterdata.usgs.gov/nwis>`__ for daily streamflow observations
* `HCDN 2009 <https://www2.usgs.gov/science/cite-view.php?cite=2932>`_ for identifying sites where human activity affects the natural flow of the watercourse
* `3DEP <https://www.usgs.gov/core-science-systems/ngp/3dep>`_ from National Map service for getting data such as Digital Elevation Model, slope, and aspect.

Additionally, the following functionalities are offered:

* **Interactive map** for exploring USGS stations within a bounding box,
* Efficient vector-based **flow accumulation** in a stream network,
* Computing **Potential Evapotranspiration** (PET) using Daymet data based on `FAO-56 <http://www.fao.org/3/X0490E/X0490E00.htm>`_,
* High level APIs for easy access to all ArcGIS `RESTful <https://en.wikipedia.org/wiki/Representational_state_transfer>`_-based services as well as `WMS <https://en.wikipedia.org/wiki/Web_Map_Service>`_- and `WFS <https://en.wikipedia.org/wiki/Web_Feature_Service>`_-based services,
* Helpers for plotting land cover data based on **official NLCD cover legends**,
* A **roughness coefficients** lookup table for each land cover type which is useful for overland flow routing.

Requests for additional databases or functionalities can be submitted via `issue tracker <https://github.com/cheginit/hydrodata/issues>`_.

Documentation
-------------

Learn more about Hydrodata in its official documentation at https://hydrodata.readthedocs.io.


Installation
------------

You can install Hydrodata using ``pip`` after installing ``libgdal`` (for example ``libgdal`` in ``Conda`` environment or ``libgdal-dev`` in Ubuntu) on your system or environment:

.. code-block:: console

    $ pip install hydrodata

Quickstart
----------

With just a few lines of code, Hydrodata provides easy access to a handful of databases. We can start by exploring the available USGS stations within a bounding box:

.. code-block:: python

    import hydrodata.datasets as hds

    hds.interactive_map([-70, 44, -69, 46])

.. image:: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/interactive_map.png
    :target: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/interactive_map.png
    :align: center


Then, we can either specify a station ID or coordinates to the ``Station`` function and gathers the USGS site information such as name, contributing drainage area, and watershed geometry.

.. code-block:: python

    from hydrodata import Station

    wshed = Station(coords=(-69.32, 45.17), dates=('2000-01-01', '2010-01-21'))

The generated ``wshed`` object has a property that shows whether the station is in HCDN database i.e., whether it's a natural watershed or is affected by human activity. For this watershed ``wshed.hcdn`` is ``True``, therefore, this is a natural watershed. Moreover, using the retrieved information, ``datasets`` module provides access to other databases. For example, we can get the main river channel and the tributaries of the watershed, the USGS stations upstream (or downstream) of the main river channel (or tributatires) up to a certain distance, say 150 km or all the stations:

.. code-block:: python

    from hydrodata import NLDI

    tributaries = NLDI.tributaries(wshed.station_id)
    main = NLDI.main(wshed.station_id)
    stations = NLDI.stations(wshed.station_id)
    stations_m150 = NLDI.stations(wshed.station_id, navigation="upstreamMain", distance=150)

For demonstrating the flow accumulation function, lets assume the flow in each river segment is equal to the length of the river segment. Therefore, it should produce the same results as the ``arbolatesu`` variable in the NHDPlus database.

.. code-block:: python

    from hydrodata import utils

    flw = utils.prepare_nhdplus(NLDI.flowlines('11092450'), 0, 0, purge_non_dendritic=False)

    def routing(qin, q):
        return qin + q

    qsim = utils.vector_accumulation(
        flw[["comid", "tocomid", "lengthkm"]],
        routing,
        "lengthkm",
        ["lengthkm"], threading=False
    )
    flw = flw.merge(qsim, on="comid")
    diff = flw.arbolatesu - flw.acc

We can check the validity of the results using ``diff.abs().sum() = 5e-14``. Furthermore, DEM, slope, and aspect can be retrieved for the station's contributing watershed at 30 arc-second (~1 km) resolution as follows:

.. code-block:: python

    from hydrodata import NationalMap

    nm = NationalMap(wshed.geometry, resolution=30)
    dem, slope, aspect = nm.get_dem(), nm.get_slope(), nm.get_aspect()

The climate data and streamflow observations for a location of interest can be retrieved as well. Note the use of ``pet`` flag for computing PET:

.. code-block:: python

    variables = ["tmin", "tmax", "prcp"]
    clm_p = hds.daymet_byloc(wshed.lon, wshed.lat,
                             start=wshed.start, end=wshed.end,
                             variables=variables, pet=True)
    clm_p['Q (cms)'] = hds.nwis_streamflow(wshed.station_id, wshed.start, wshed.end)

Other than point-based data, we can get data from gridded databases. The retrieved data are masked with the watershed geometry:

.. code-block:: python

    clm_g = hds.daymet_bygeom(wshed.geometry,
                              start='2005-01-01', end='2005-01-31',
                              variables=variables, pet=True)
    eta_g = hds.ssebopeta_bygeom(wshed.geometry, start='2005-01-01', end='2005-01-31')

All the gridded data are returned as `xarray <https://xarray.pydata.org/en/stable/>`_ datasets that has efficient data processing tools. Additionally, Hydrodata has a ``plot`` module that plots five hydrologic signatures graphs in one plot:

.. code-block:: python

    from hydrodata import plot

    plot.signatures(clm_loc['Q (cms)'], wshed.drainage_area, prcp=clm_loc['prcp (mm/day)'], title=wshed.name)

Some example plots are shown below:

.. image:: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/example_plots.png
        :target: https://raw.githubusercontent.com/cheginit/hydrodata/develop/docs/_static/example_plots.png

The ``services`` module can be used to access some other web services as well. For example, we can access `Los Angeles GeoHub <http://geohub.lacity.org/>`_ RESTful service, NationalMap's `3D Eleveation Program <https://www.usgs.gov/core-science-systems/ngp/3dep>`_ via WMS and `FEMA National Flood Hazard Layer <https://www.fema.gov/national-flood-hazard-layer-nfhl>`_ via WFS as follows:

.. code-block:: python

    from hydrodata import ArcGISREST, WFS, services
    import geopandas as gpd

    la_wshed = Station('2005-01-01', '2005-01-31', '11092450')

    url_rest = "https://maps.lacity.org/lahub/rest/services/Stormwater_Information/MapServer/10"
    s = ArcGISREST(url_rest, outFormat="json")
    s.get_featureids(la_wshed.geometry)
    storm_pipes = s.get_features()

    url_wms = "https://elevation.nationalmap.gov/arcgis/services/3DEPElevation/ImageServer/WMSServer"
    hillshade = services.wms_bygeom(
        url_wms,
        geometry=wshed.geometry,
        version="1.3.0",
        layers={"hillshade": "3DEPElevation:GreyHillshade_elevationFill"},
        outFormat="image/tiff",
        resolution=1
    )

    url_wfs = "https://hazards.fema.gov/gis/nfhl/services/public/NFHL/MapServer/WFSServer"
    wfs = WFS(
        url_wfs,
        layer="public_NFHL:Base_Flood_Elevations",
        outFormat="esrigeojson",
        crs="epsg:4269",
    )
    r = wfs.getfeature_bybox(wshed.geometry.bounds, in_crs="epsg:4326")
    flood = utils.json_togeodf(r.json(), "epsg:4269", "epsg:4326")

Contributing
------------

Hydrodata offers some limited statistical analysis. It could be more useful to the watershed modeling community to integrate more data exploratory capabilities to the package. Additionally, adding support for more databases such as water quality, phenology, and water level, are very welcome. If you are interested please get in touch. You can find information about contributing to hydrodata at our `Contributing page <https://hydrodata.readthedocs.io/en/latest/contributing.html>`_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
