__author__ = 'jerickson'

import netCDF4
import shutil
import os

### PRMS File representation
class PRMSFile:
    def __init__(self, basefile):
        self.basefile = basefile
        self.workingscenario = None

    def BeginScenario(self, scenarioname):
        '''
        Starts a new scenario based on the original file under a new name

        :param scenarioname: Name of scenario to make a new file; .nc will be appended
        :return:
        '''
        if self.workingscenario is not None:
            raise Exception("Working Scenario already open")
            return
        scenariofile = scenarioname + ".nc"
        shutil.copyfile(self.basefile, scenariofile)
        self.workingscenario = netCDF4.Dataset(scenariofile, 'r+')

    def EndScenario(self):
        '''
        Close the working scenario and free our references to it
        :return:
        '''
        if self.workingscenario is None:
            return
        self.workingscenario.close()
        self.workingscenario = None

    def DebugDisplayCovType(self, coords):
        '''
        For debug purposes; given a list of coordinates (hrus), display the coverage type for each coordinate
        :param coords: List of coordinates
        :return:
        '''
        if self.workingscenario is None:
            raise Exception("No working scenario defined")
            return
        for coord in coords:
            print "Coordinate {0}, {1}: {2}".format(coord[0], coord[1], self.workingscenario.variables['cov_type'][coord[0],coord[1]])

    def UpdateCovType(self, x, y, val):
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

    def BlockUpdateCovType(self, coords, val):
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
            self.UpdateCovType(coord[0], coord[1], val)

if __name__=="__main__":
    prmsfile = PRMSFile("parameter.nc")

    coord_list = [(0, 0), (0, 1), (0, 2),
                  (1, 0), (1, 1), (1, 2),
                  (2, 0), (2, 1), (2, 2)]

    try:
        prmsfile.BeginScenario("test")
        prmsfile.DebugDisplayCovType(coord_list)
        prmsfile.BlockUpdateCovType(coord_list, 2)
        prmsfile.DebugDisplayCovType(coord_list)
        prmsfile.EndScenario()
    except Exception as ex:
        print "Test run failed: " + ex.message

    print "Testing exceptions..."
    try:
        prmsfile.DebugDisplayCovType(coord_list)
    except Exception as ex:
        print "DebugDisplayCovType properly failed"
    try:
        prmsfile.BlockUpdateCovType(coord_list)
    except Exception as ex:
        print "BlockUpdateCovType properly failed"
    try:
        prmsfile.UpdateCovType(0, 0, 0)
    except Exception as ex:
        print "UpdateCovType properly failed"