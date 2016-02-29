---
title: PRMS Vegetation Map Scenario Tool
author:
    - Matthew A. Turner
    - Chao Chen
    - Chase Carthen
    - Moinul Hossain
    - Lisa Palathingal
    - John Erickson
    - Lucas J. Sheneman
    - Karl Benedict
    - Fred Harris
    - Sajjad Ahmad
date: \today{}
geometry: margin=1in
header-includes:
    - \usepackage{setspace}
    - \doublespacing
    - \usepackage{lineno}
    - \linenumbers
---

\maketitle

\begin{abstract}
Climate Change brings with it increased chances of vegetation succession,
be it due to fire, drought, temperature and precipitation change, or flooding.
PRMS is a popular tool for hydrological modeling. Combining the two,
we present an online tool that allows a user
to model vegetation succession in a variety of scenarios and analyze the PRMS
output. To do this, a user draws GeoJSON MultiPolygons on a map either in the
browser or in a Unity visualization client, then re-run PRMS for all
of the scenarios they have created. The user then can download the
outputs in convenient netCDF format for local processing. Although
the app that is
\href{https://virtualwatershed.org/modeling/prms-burn-scenarios}{available online now} is
built exclusively for the Lehman Creek watershed located in Great
Basin National Park in Nevada, it is suitable for any watershed for
which there exists PRMS data and parameterization. The configuration
is simple: there is but one file to update and the entire app can be
quickly customized for your watershed. What's more, the REST API can
be used with any HTTP client, with documentation and examples online.
So if your hydrologists are using MATLAB you could build a MATLAB
client, or if you want to build a mobile app, you can do that, too.
\end{abstract}

\tableofcontents


\newpage



# Introduction

First it's important to note that this PRMS Burn Scenario Tool (PBST)
is a product of the [Virtual Watershed
project](https://github.com/VirtualWatershed), which is the
over-arching product of the Western Consortium for Wateshed Analysis,
Visualization, and Exploration (WC-WAVE). This collaboration between three
intermountain west states, Nevada, New Mexico, and Idaho, focuses on
bringing timely and useful cyberinfrastructure tools to critical zone
hydrologists. Developers and hydrologists are partners developing
tools that serve immediate needs while at the same time building a
common core of cyberinfrastructure that will serve hydrologists beyond
our project. So for this project, it's important to emphasize again
that the version available online is specific to the watershed where
PRMS is being used within WC-WAVE, by changing a configuration file,
we can adapt the framework for any watershed and PRMS data and
parameters.

As a quick overview of the technology used, the core is a REST API
built with Python's Flask "microframework". This core API makes heavy
use of the Virtual Watershed's [PRMS
adaptors](https://github.com/VirtualWatershed/vw-py/prms), [Python
API](https://github.com/VirtualWatershed/vw-py), and [RESTful modeling
services](https://github.com/VirtualWatershed/vwadaptor). Our web
client uses React for its user interface and controller, and jQuery
AJAX calls for running and retrieving scenarios and their associated
data. The visualization client lets the user explore the terrain in
3D to better select the burn regions according to landscape features
using the Unity gaming engine. The Unity engine allows us to connect
this to other technologies like CAVEs and immersive technologies.


# Hydrologist Workflow

`(from Chao)`

As one of the most important inputs to a hydrologic model, the land cover
(cov_type) determines the hydrological processes of canopy interception,
evapotranspiration and snow pack accumulation/melt, and through the changes of
these processes, the water formation and distribution as to streamflow rate and
timing on entire watershed will be affected or changed entirely. By
simulating the changes of vegetation type, the impact of vegetation
distribution on hydrologic processes can be assessed. Making the functionality
of vegetation change available in Vis tool/VW platform will help researchers to
perform theoretical studies with a change of vegetation distribution and
evaluate the hydrological changes.

## More on the science with references to previous work (Chao)

As one of the most important inputs to a hydrologic model, the land cover
(cov_type) determines the hydrological processes of canopy interception,
evapotranspiration and snow pack accumulation/melt, and through the changes
of these processes, the water formation and distribution as to streamflow
rate and timing on entire watershed will be affected or changed entirely.
By simulating the changes of vegetation type, the impact of vegetation
distribution on hydrologic processes can be assessed. Making the
functionality of vegetation change available in Vis tool/VW platform
can help researchers to perform theoretical study with a change of vegetation
distribution and evaluate the hydrological changes.

The seven parameters to be updated when vegetation type (cov_type) is updated:

1. snow interception storage capacity for the major vegetation type in each HRU (snow_intcp)
1. summer rain interception storage capacity for the major vegetation type in each HRU (srain_intcp)
1. winter rain interception storage for the major vegetation type in each HRU (wrain_intcp)
1. summer vegetation cover density for the major vegetation type in each HRU(covden_sum)
1. winter vegetation cover density for the major vegetation type in each HRU(covden_win), from the Canopy Interception process
1. Air temperature coefficient (jh_coef_hru) used in Jensen-Haise potential evapotranspiration equation for each HRU (jh_coef_hru), from the Potential Evapotranspiration process
1. Transmission coefficient for short-wave radiation through winter plant canopy (rad_trncf), from the Snow Computation process

When vegetation change occurs to a certain region in Lehman Creek, we will
replace these 7 parameter values with the corresponding values of the
certain vegetation type that the region changes into. For example, if we
make the vegetation type change from 3 (forest) to 0 (barren), we will use
the 7 parameter values from other barren area within the watershed, to
replace those 7 parameter values in this vegetation changed region.
Certainly, there are limitations and assumptions we have to make for this
method employment and for the vegetation change study too.


## REST API for running scenarios

REST is a ubiquitous and powerful scheme for programming language-agnostic
functionality. In our case, our server has been
designed to present the user with an interface for running new scenarios and
a list of previously run scenarios.

A new scenario consists of a list of polygons and the vegetation code associated
with each polygon. For example, leaving out any user or session information,
we might update two areas of our watershed with vegetation codes of 1 and 3
over two separate polygons like so

```json
{
	'vegetation_updates': [
		{
			'cov_type_code': 1,
			'region': {
				'type': 'Polygon',
				'coordinates': [ [100.0, 0.0],
								 [101.0, 0.0],
								 [101.0, 1.0],
								 [100.0, 1.0],
								 [100.0, 0.0] ]
			}
		},
		{
			'cov_type_code': 3,
			'region': { 'type': 'Polygon', 'coordinates': ... }
		}, ...
	],
    ...
}
```

If two polygons overlap, the later one in the list will overwrite previous
polygons.


## Translated to a Unity client (Chase)

## Translated to a Web Browser (Matt)

In the browser we translate the requirements of the ability to change the
vegetation type to one of the five types for an arbitrary polygon and re-run
the PRMS model to a set of five selector buttons and a map with a polygon
drawing ability. The user creates one polygon at a time with the ability to
edit existing polygons. When the user has created all the polygons necessary,
the user presses "Run Scenario." This sends an HTTP POST request to the
server's `/api/scenarios` route, which is explained above.



# Design and Software

This section introduces our software stack, with Python providing a REST API
that serves and accepts JSON on the backend and a ReactJS, Bootstrap, and

This is a fully open source solution with familiar, ubiquitous tools that all
students will find valuable to know as they enter the workforce. By using
common and cutting-edge tools we make our developers lives easier since more
resources are available online for learning the tools, and the power and wide
applicability of these tools makes development fun.


## Server Architecture: REST, JSON, Python

The REST architecture is the natural choice for Service Oriented
Architectures (SOA) where providers and consumers are loosely coupled to
allow for services to be improved or new services to be added without
affecting other services. By using the REST-compliant SOA, clients can
expect the only verbs to be the HTTP verbs, and URLs will be
descriptive, intuitive nouns, best explained in Fielding's PhD thesis
where he introduces his invention [@fielding2000].

JSON is in and XML is out [@vitolo2015web], arguably because web technologies
are rarely, if ever, designed with XML in mind, and we want to support
GeoJSON queries natively, we use MongoDB as our datastore. Part of the Virtual
Watershed effort is not just to establish better cyberinfrastructure for
hydrologists, but also to use and establish best practices for future
cyberinfrastructure developers.

To this end, we are using standards where appropriate. Appropriate means
not only having a history of adoption within the hydrology community, but also
having modern tools to support development. To this end, we have chosen
netCDF as our common data format. In the case of PRMS this enables us to
use existing tools, namely the
[netcdf-python](https://github.com/Unidata/netcdf4-python) library, to
modify PRMS parameter files. `netcdf4-python` uses numpy arrays, which are widely
used across a multitude (if not all!) scientific disciplines.
The netCDF format is self-describing, meaning it contains its own metadata in
a standardized format. This allows us to include all the metadata of a PRMS
file, as well as its data, in a format that any developer at any point in their
career can find a plethora of help for using.

## Unity Visualization Engine (Chase)



## Web Front-end Architecture: ReactJS, D3, jQuery


# Discussion & Future Work


# Conclusion

\newpage

# Works Cited
