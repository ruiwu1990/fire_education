__author__ = 'jerickson'

import netCDF4
import shutil
import types
import os
import uuid
import time

### PRMS File representation
class PRMSFile:
    def __init__(self, basefile):
        self.basefile = basefile
        self.workingscenario = None

    def begin_scenario(self, scenarioname):
        '''
        Starts a new scenario based on the original file under a new name

        :param scenarioname: Name of scenario to make a new file; .nc will be appended
        :return:
        '''
        if self.workingscenario is not None:
            raise Exception("Working Scenario already open")
            return
        #uniqueID = uuid.uuid4()
        #scenariofile =  "{0}_{1}_{2}.nc".format(scenarioname,uniqueID,time.strftime("%d_%b_%Y__%H_%M_%S", time.gmtime()))

        scenariofile = ""
        if os.path.exists("{0}.nc".format(scenarioname)):
            sequence = 2
            while os.path.exists("{0}-{1}.nc".format(scenarioname, sequence)):
                sequence = sequence + 1
            scenariofile = "{0}-{1}.nc".format(scenarioname, sequence)
        else:
            scenariofile = "{0}.nc".format(scenarioname)
        print scenariofile
        shutil.copyfile(self.basefile, scenariofile)
        self.workingscenario = netCDF4.Dataset(scenariofile, 'r+')

    def end_scenario(self):
        '''
        Close the working scenario and free our references to it
        :return:
        '''
        if self.workingscenario is None:
            return
        self.workingscenario.close()
        self.workingscenario = None

    def debug_display_cov_type(self, coords):
        '''
        For debug purposes; given a list of coordinates (hrus), display the coverage type for each coordinate
        :param coords: List of coordinates
        :return:
        '''
        if self.workingscenario is None:
            raise Exception("No working scenario defined")
            return
        for coord in coords:
            if isinstance(coord, types.IntType):
                #Single Coordinate given, convert to x,y
                x_max = len(self.workingscenario.dimensions['lon'])
                x = coord / x_max
                y = coord % x_max
                print "Coordinate {0} ({1}, {2}): {3}".format(coord, x, y, self.workingscenario.variables['cov_type'][x,y])
            elif isinstance(coord, types.TupleType):
                print "Coordinate {0}, {1}: {2}".format(coord[0], coord[1], self.workingscenario.variables['cov_type'][coord[0],coord[1]])

    def update_cov_type(self, x, y, val):
        '''
        Update coverage type in a single hru using 2d coordinates
        :param x: x coordinate for hru
        :param y: y coordinate for hru
        :param val: value to set hru to
        :return:
        '''
        if self.workingscenario is None:
            raise Exception("No working scenario defined")
            return
        #print "{0}, {1} Cov Type Before: {2}".format(x, y, self.workingscenario.variables['cov_type'][x,y])
        self.workingscenario.variables['cov_type'][x,y] = val
        #print "{0}, {1} Cov Type After: {2}".format(x, y, self.workingscenario.variables['cov_type'][x,y])

    def block_update_cov_type(self, coords, val):
        '''
        Given a list of coordinates (hrus), update coverage type for each hru to given value
        :param coords: List of coordinates
        :param val: value to set hrus to
        :return:
        '''
        if self.workingscenario is None:
            raise Exception("No working scenario defined")
            return
        for coord in coords:
            #print "Coordinate {0}, {1}: ".format(coord[0], coord[1])
            if isinstance(coord, types.IntType):
                #Single Coordinate given, convert to x,y
                x_max = len(self.workingscenario.dimensions['lon'])
                x = coord / x_max
                y = coord % x_max
                #print "x, y: {0}, {1}".format(x,y)
                self.update_cov_type(x, y, val)
            elif isinstance(coord, types.TupleType):
                #x,y tuple given
                self.update_cov_type(coord[0], coord[1], val)

if __name__=="__main__":
    prmsfile = PRMSFile("parameter.nc")

    coord_list_old = [(0, 0), (0, 1), (0, 2),
                  (1, 0), (1, 1), (1, 2),
                  (2, 0), (2, 1), (2, 2)]

    coord_list = [0,   1,   2,
                  96,  97,  98,
                  192, 193, 194]

    try:
        prmsfile.begin_scenario("test")
        prmsfile.debug_display_cov_type(coord_list)
        prmsfile.debug_display_cov_type(coord_list_old)
        prmsfile.block_update_cov_type(coord_list, 2)
        prmsfile.debug_display_cov_type(coord_list)
        prmsfile.debug_display_cov_type(coord_list_old)
        prmsfile.end_scenario()
    except Exception as ex:
        print "Test run failed: " + ex.message

    print "Testing exceptions..."
    try:
        prmsfile.debug_display_cov_type(coord_list)
    except Exception as ex:
        print "DebugDisplayCovType properly failed"
    try:
        prmsfile.block_update_cov_type(coord_list)
    except Exception as ex:
        print "BlockUpdateCovType properly failed"
    try:
        prmsfile.update_cov_type(0, 0, 0)
    except Exception as ex:
        print "UpdateCovType properly failed"