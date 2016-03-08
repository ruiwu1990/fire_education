from . import db


class Hydrograph(db.EmbeddedDocument):
    """
    Hydrograph output data
    """
    time_array = db.ListField(db.DateTimeField())
    streamflow_array = db.ListField(db.DateTimeField())


class VegetationMapByHRU(db.EmbeddedDocument):
    """
    Vegetation map by HRU, modified as requested by the user
    """
    bare_ground = db.ListField(db.IntField())
    grasses = db.ListField(db.IntField())
    shrubs = db.ListField(db.IntField())
    trees = db.ListField(db.IntField())
    conifers = db.ListField(db.IntField())


class Inputs(db.EmbeddedDocument):
    """
    download links to control, data, and parameter files for a given scenario
    """
    control = db.URLField(default='example.com/control.dat')
    parameter = db.URLField(default='example.com/parameter.nc')
    data = db.URLField(default='example.com/data.nc')


class Outputs(db.EmbeddedDocument):
    """
    download links to PRMS outputs from scenario
    """
    statvar = db.URLField(default='example.com/statvar.nc')


class Scenario(db.Document):
    """
    Scenario data and metadata
    """
    name = db.StringField(required=True)
    user = db.StringField(default='anonymous')
    time_received = db.DateTimeField(required=True)
    time_finished = db.DateTimeField(required=True)

    veg_map_by_hru = db.EmbeddedDocumentField('VegetationMapByHRU')

    inputs = db.EmbeddedDocumentField('Inputs')
    outputs = db.EmbeddedDocumentField('Outputs')

    hydrograph = db.EmbeddedDocumentListField('Hydrograph')

    def __str__(self):

        return \
            '\n'.join(["{}: {}".format(k, self[k])
                       for k in self._fields_ordered])
