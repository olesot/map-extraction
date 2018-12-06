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

def dissolve(input, output, multipoly=False, overwrite=False):
    ds = ogr.Open(input)
    lyr = ds.GetLayer()
    out_ds, out_lyr = createDS(output, ds.GetDriver().GetName(), lyr.GetGeomType(), lyr.GetSpatialRef(), overwrite)
    defn = out_lyr.GetLayerDefn()
    multi = ogr.Geometry(ogr.wkbMultiPolygon)
    for feat in lyr:
        if feat.geometry():
            feat.geometry().CloseRings() # this copies the first point to the end
            wkt = feat.geometry().ExportToWkt()
            multi.AddGeometryDirectly(ogr.CreateGeometryFromWkt(wkt))
    union = multi.UnionCascaded()
    if multipoly is False:
        for geom in union:
            poly = ogr.CreateGeometryFromWkb(geom.ExportToWkb())
            feat = ogr.Feature(defn)
            feat.SetGeometry(poly)
            out_lyr.CreateFeature(feat)
    else:
        out_feat = ogr.Feature(defn)
        out_feat.SetGeometry(union)
        out_lyr.CreateFeature(out_feat)
        out_ds.Destroy()
    ds.Destroy()
    return True


if __name__ == "__main__":
    dissolve("polyHazards", "polyHazardsDissolved", overwrite=True)
    print("Geometries is dissolved.")
