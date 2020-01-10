import arcpy
checkboxRaft = arcpy.GetParameterAsText(0)
LineRaft = arcpy.GetParameterAsText(1)
pointRaft = arcpy.GetParameterAsText(2)
checkboxBargasht = arcpy.GetParameterAsText(3)
output = arcpy.GetParameterAsText(6)
arcpy.env.workspace = output
arcpy.env.overwriteOutput = True

interval = 15
sr = arcpy.SpatialReference(32639)


if str(checkboxRaft) == "true":

    def raft():

        arcpy.CreateFeatureclass_management(output,pointRaft,"POINT",spatial_reference=sr)
        memorypointRaft=arcpy.CopyFeatures_management(pointRaft,"in_memory/pointRaft")
        memorylineRaft=arcpy.CopyFeatures_management(LineRaft,"in_memory/lineRaft")
        X= arcpy.AddField_management(memorypointRaft,"X","DOUBLE")
        Y= arcpy.AddField_management(memorypointRaft,"Y","DOUBLE")
        arcpy.AddField_management(memorypointRaft,"Point_Row","SHORT")
        arcpy.AddField_management(memorypointRaft,"KM","DOUBLE")
        insertCursor = arcpy.da.InsertCursor(memorypointRaft, ["SHAPE@XY"]) # this is the pre-existing pt feature class
        with arcpy.da.SearchCursor(memorylineRaft, ['OID@','SHAPE@']) as searchCursor: # this is the line feature on which the pointRafts will be based
            for row in searchCursor:
                lengthLine = row[1].length # grab the length of the line feature, i'm using round() here to avoid weird rounding errors that prevent the numberOfPositions from being determined
                if lengthLine % interval == 0:
                    numberOfPositions = int(lengthLine // interval) - 1
                else:
                    numberOfPositions = int(lengthLine // interval)
                    if numberOfPositions >= 0:
                        distancezero = 0
                        xPoint = row[1].positionAlongLine(distancezero).firstPoint.X
                        yPoint = row[1].positionAlongLine(distancezero).firstPoint.Y
                        xy = (xPoint, yPoint)
                        insertCursor.insertRow([xy])
                        for i in range(numberOfPositions):
                            distance = (i + 1) * interval
                            xPoint = row[1].positionAlongLine(distance).firstPoint.X
                            yPoint = row[1].positionAlongLine(distance).firstPoint.Y
                            xy = (xPoint, yPoint)
                            insertCursor.insertRow([xy])
                        distanceend = lengthLine
                        xPoint = row[1].positionAlongLine(lengthLine).firstPoint.X
                        yPoint = row[1].positionAlongLine(lengthLine).firstPoint.Y
                        xy = (xPoint, yPoint)
                        insertCursor.insertRow([xy])
                    del insertCursor
        count = arcpy.GetCount_management(memorypointRaft).getOutput(0)

        lastRow = int(count)
        onelastRow = int(count)-1
        print lastRow
        with arcpy.da.UpdateCursor(memorypointRaft,["OBJECTID","KM"]) as ptcursor:
            number = 0
            for rowpt in ptcursor:
                rowpt[1] = number
                number = number + 15
                if rowpt[0] == lastRow:
                        remainder = (lengthLine - ( onelastRow * 15 -15))
                        rowpt[1] = round(float((onelastRow * 15 -15)+remainder))
                ptcursor.updateRow(rowpt)


        arcpy.CalculateField_management(memorypointRaft, "Point_Row","!OBJECTID!", "PYTHON_9.3")
        wgs = arcpy.SpatialReference(4326)
        with arcpy.da.UpdateCursor(memorypointRaft, ['SHAPE@', 'Y', 'X']) as rows:
            for row in rows:
                pnt_wgs = row[0].projectAs(wgs)
                row[1:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X] #will be in decimal degrees
                rows.updateRow(row)
            del row
            del rows
        arcpy.CopyFeatures_management(memorypointRaft,pointRaft)
    raft()

if str(checkboxBargasht) == "true":
# Bargasht
    def bargasht():
        LineBargasht = arcpy.GetParameterAsText(4)
        pointBargasht = arcpy.GetParameterAsText(5)
        arcpy.CreateFeatureclass_management(output,pointBargasht,"POINT",spatial_reference=sr)
        memorypointBargasht = arcpy.CopyFeatures_management(pointBargasht,"in_memory/pointbargasht")
        X= arcpy.AddField_management(memorypointBargasht,"X","DOUBLE")
        Y= arcpy.AddField_management(memorypointBargasht,"Y","DOUBLE")
        arcpy.AddField_management(memorypointBargasht,"Point_Row","SHORT")
        arcpy.AddField_management(memorypointBargasht,"KM","DOUBLE")
        insertCursor = arcpy.da.InsertCursor(memorypointBargasht, ["SHAPE@XY"]) # this is the pre-existing pt feature class
        memoryLineBargasht=arcpy.CopyFeatures_management(LineBargasht,"in_memory/linebargasht")
        with arcpy.da.SearchCursor(memoryLineBargasht, ['OID@','SHAPE@']) as searchCursor: # this is the line feature on which the memorypointBargashts will be based
            for row in searchCursor:
                lengthLine = row[1].length # grab the length of the line feature, i'm using round() here to avoid weird rounding errors that prevent the numberOfPositions from being determined
                if lengthLine % interval == 0:
                    numberOfPositions = int(lengthLine // interval) - 1
                else:
                    numberOfPositions = int(lengthLine // interval)
                    if numberOfPositions >= 0:
                        distancezero = 0
                        xPoint = row[1].positionAlongLine(distancezero).firstPoint.X
                        yPoint = row[1].positionAlongLine(distancezero).firstPoint.Y
                        xy = (xPoint, yPoint)
                        insertCursor.insertRow([xy])
                        for i in range(numberOfPositions):
                            distance = (i + 1) * interval
                            xPoint = row[1].positionAlongLine(distance).firstPoint.X
                            yPoint = row[1].positionAlongLine(distance).firstPoint.Y
                            xy = (xPoint, yPoint)
                            insertCursor.insertRow([xy])
                        distanceend = lengthLine
                        xPoint = row[1].positionAlongLine(lengthLine).firstPoint.X
                        yPoint = row[1].positionAlongLine(lengthLine).firstPoint.Y
                        xy = (xPoint, yPoint)
                        insertCursor.insertRow([xy])
                    del insertCursor
        count = arcpy.GetCount_management(memorypointBargasht).getOutput(0)

        lastRow = int(count)
        onelastRow = int(count)-1
        print lastRow
        with arcpy.da.UpdateCursor(memorypointBargasht,["OBJECTID","KM"]) as ptcursor:
            number = 0
            for rowpt in ptcursor:
                rowpt[1] = number
                number = number + 15
                if rowpt[0] == lastRow:
                        remainder = (lengthLine - ( onelastRow * 15 -15))
                        rowpt[1] = round(float((onelastRow * 15 -15)+remainder))
                ptcursor.updateRow(rowpt)


        arcpy.CalculateField_management(memorypointBargasht, "Point_Row","!OBJECTID!", "PYTHON_9.3")
        wgs = arcpy.SpatialReference(4326)
        with arcpy.da.UpdateCursor(memorypointBargasht, ['SHAPE@', 'Y', 'X']) as rows:
            for row in rows:
                pnt_wgs = row[0].projectAs(wgs)
                row[1:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X] #will be in decimal degrees
                rows.updateRow(row)
            del row
            del rows
        arcpy.CopyFeatures_management(memorypointBargasht,pointBargasht)
    bargasht()

arcpy.AddMessage(u'\u067e\u0631\u062f\u0627\u0632\u0634 \u062f\u0627\u062f\u0647 \u0647\u0627 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u0627\u0646\u062c\u0627\u0645 \u0634\u062f')