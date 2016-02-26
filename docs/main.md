PRMS Burn Scenario Tool
=======================


\begin{abstract}
Since burn extent has an impact on the hydrodynamics of a watershed,
it's important to be able to readily modify the vegetation type in the
burn to indicate it has burned as well as quickly run PRMS after we
have updated the area of burn. In order to plan for multiple scenarios
in high burn-risk areas, we present an online tool that allows a user
to create burn area GeoJSON MultiPolygons on a map either in the
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



Introduction
------------

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



Design and Software
-------------------

The REST architecture is the natural choice for Service Oriented
Architectures (SOA) where providers and consumers are loosely coupled to
allow for services to be improved or new services to be added without
affecting other services. By using the REST-compliant SOA, clients can
expect the only verbs to be the HTTP verbs, and URLs will be
descriptive, intuitive nouns, best explained in Fielding's PhD thesis
where he introduces his invention @fielding2000.

JSON is in and XML is out @vitolo2015web, arguably because web technologies
are rarely, if ever, designed with XML in mind, and we want to support
GeoJSON queries natively, we use MongoDB as our datastore.

NetCDF, Flask, Unity, D3, React
