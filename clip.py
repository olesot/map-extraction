#!/usr/bin/python


import os
from osgeo import ogr

def createDS(ds_name, ds_format, geom_type, srs, overwrite=False):
    drv = ogr.GetDriverByName(ds_format)
    if os.path.exists(ds_name) and overwrite is True:
        drv.DeleteDataSource(ds_name)
    ds = drv.CreateDataSource(ds_name)
    lyr_name = os.path.splitext(os.path.basename(ds_name))[0]
    lyr = ds.CreateLayer(lyr_name, srs, geom_type)
    return ds, lyr

'''
def createClipLayer():
    

def clip(input, output, overwrite=False):
    
    '''

def assignClipSections(layer):
    center = ogr.Geometry(ogr.wkbPoint)
    center.AddPoint(5.85, 58.47)

    safe  = center.Buffer(0.001,4)
    close = center.Buffer(0.002,4)
    ahead = center.Buffer(0.01,4)

    featDefn = layer.GetLayerDefn()

    geom_safe = center.Buffer(0.001,4)
    geom_close = center.Buffer(0.002,4)
    geom_ahead = center.Buffer(0.01,4).Difference(geom_close)
    geom_close = geom_close.Difference(geom_safe)

    feat_safe = ogr.Feature(featDefn)
    feat_safe.SetGeometry(geom_safe)
    feat_safe.SetFID(0)
    feat_close = ogr.Feature(featDefn)
    feat_close.SetGeometry(geom_close)
    feat_close.SetFID(1)
    feat_ahead = ogr.Feature(featDefn)
    feat_ahead.SetGeometry(geom_ahead)
    feat_ahead.SetFID(2)

    layer.CreateFeature(feat_ahead)
    layer.CreateFeature(feat_close)
    layer.CreateFeature(feat_safe)




if __name__ == "__main__":
    ds = ogr.Open("polyHazardsDissolved")
    lyr = ds.GetLayer()

    ds_section, lyr_section = createDS("clipSection", ds.GetDriver().GetName(),
                                       lyr.GetGeomType(), lyr.GetSpatialRef(),
                                       overwrite=True)

    ds_out, lyr_out = createDS("clip", ds.GetDriver().GetName(),
                               lyr.GetGeomType(), lyr.GetSpatialRef(),
                               overwrite=True)


    assignClipSections(lyr_section)
    lyr.Intersection(lyr_section, lyr_out)

    print("Featcount: ", lyr_section.GetFeatureCount())


