## prms-fire-scenarios

In keeping with our aim of serving specific hydrologists' needs while building or demonstrating core
cyberinfrastructure (CI), this tool uses Virtual Watershed technology to provide a tool for
hydrologists wanting to investigate the effects of fire on the outputs of PRMS models.

## Prototype Goals and Milestones (as of 2/25)

There are [two current milestones](https://github.com/VirtualWatershed/prms-fire-scenarios/milestones):

1. [Minimum Viable Product due March 25](https://github.com/VirtualWatershed/prms-fire-scenarios/milestones/Minimum%20Viable%20Product%20--%20MVP)
1. [v1.0 Release due May 13](https://github.com/VirtualWatershed/prms-fire-scenarios/milestones/v1.0%20Release)

The [issues](https://github.com/VirtualWatershed/prms-fire-scenarios/issues) show what needs to be done. There 
are currently only issues for the first milestone, which will be the case for a while. These issues reference 
how to build out the wireframe demo (forthcoming).

# Info and Getting Started

Currently there are some demo routes in [app/api/views.py](https://github.com/VirtualWatershed/prms-fire-scenarios/blob/master/app/api/views.py)
and the Swagger API spec is in [api-spec.yaml](https://github.com/VirtualWatershed/prms-fire-scenarios/blob/master/api-spec.yaml).


#### Dependencies

There are a couple of things to do first. One, run 

```
bower install
```

to install Swagger-UI, currently the only [bower](http://bower.io) dependency.

Next install the Python dependencies using

```
pip install -r requirements.txt
```

You probably want to be using [virtual environments]().

At this point bower has overwritten something in the repository. To put it back,

```
git checkout -- app/static/bower_components/swagger-ui/dist/index.html
```

#### Run Swagger-UI to see spec

Now, finally, we can run our Swagger-UI and look at the spec by running

```
./serve-swag.sh
```

and visiting [http://localhost:8000/swagger-ui/dist/?url=/../../api-spec.yaml](http://localhost:8000/swagger-ui/dist/?url=/../../api-spec.yaml).

We need to make this spec actually happen. This is the API the frontend and Chase's Unity vis will use to run and access scenarios.


#### Flask RESTful API

To see the API in action in its current state, start up the Flask development server

```
python manage.py runserver
```

and visit [localhost:5000/api/scenarios](http://localhost:5000/api/scenarios).

Again, find example routes in [app/api/views.py](https://github.com/VirtualWatershed/prms-fire-scenarios/blob/master/app/api/views.py).
These need to be filled in. Most immediately, `POST`ing to the `/api/scenarios` route is required for our demo.
