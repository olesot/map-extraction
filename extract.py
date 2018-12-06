#!/usr/bin/python


from osgeo import ogr, osr, gdal
import sys, getopt, os


def main(argv):
    src = ''
    outPoint = "pointHazards"
    outPoly = "polyHazards"
    relevantLayers= ['DEPARE', 'BCNSPP', 'BCNISD', 'BCNLAT', 'BOYSPP']
    safeDepth = 5

    try:
        opts, args = getopt.getopt(argv, "hi::", ["ifile="])
    except getopt.GetoptError:
        print "extract2.py -i <inputfile>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "extract2.py -i <inputfile>"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            src = arg
    print("Inputfile is ", src)

    # Open source file
    ds = gdal.OpenEx(src)
    if(ds == None):
        print("Error open source file %s. Exiting." % src)
        sys.exit(1)
    # Create Shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # Create Point Shapefile
    if os.path.exists(outPoint):
        driver.DeleteDataSource(outPoint)
    if os.path.exists(outPoly):
        driver.DeleteDataSource(outPoly)
    outDSPoint = driver.CreateDataSource(outPoint)
    outDSPoly = driver.CreateDataSource(outPoly)
    wgs_reference = osr.SpatialReference()
    wgs_reference.ImportFromEPSG(4326)
    utm_32v_reference = osr.SpatialReference()
    utm_32v_reference.SetProjCS("UTM 32 / WGS84")
    utm_32v_reference.SetWellKnownGeogCS("WGS84")
    utm_32v_reference.SetUTM(32)
    outLayerPoint = outDSPoint.CreateLayer(outPoint.split(".")[0], wgs_reference, ogr.wkbPoint)
    outLayerPoly = outDSPoly.CreateLayer(outPoly.split(".")[0], wgs_reference, ogr.wkbPolygon)

    for layername in relevantLayers:
        layer = ds.GetLayerByName(layername)

        # Keep only Geometry areas less than "safeDepth" meter
        if (layername == "DEPARE"):
            layer.SetAttributeFilter("DRVAL1 < %d" % safeDepth)

        for feat in layer:
            geom = feat.GetGeometryRef()
            if (geom.GetGeometryName() == "POINT"):
                outFeatDefn = outLayerPoint.GetLayerDefn()
                outFeat = ogr.Feature(outFeatDefn)
                outFeat.SetGeometry(geom)
                outLayerPoint.CreateFeature(outFeat)
            elif (geom.GetGeometryName() == "POLYGON"):
                outFeatDefn = outLayerPoly.GetLayerDefn()
                outFeat = ogr.Feature(outFeatDefn)
                outFeat.SetGeometry(geom)
                outLayerPoly.CreateFeature(outFeat)

if __name__ == "__main__":
    main(sys.argv[1:])
