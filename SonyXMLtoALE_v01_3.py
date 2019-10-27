#!/usr/bin/python

#LTC Change = Samples since midnight (FFSSMMHH) 00351210 = 10:12:35:00

#Script is written by Rainer Fritz, April 2019

import sys
import os
import fnmatch

from Tkinter import *
import Tkinter, tkFileDialog, Tkconstants

import xml.etree.ElementTree as ET

#from timecode import Timecode

runcounter = 0


def searchdir():
    print ('Please select Directory to search for XMLs!')
    root = Tk()
    root.withdraw()
    root.directory = tkFileDialog.askdirectory()
    return root.directory


def searchfiles(path, pattern):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def parse_mproxml(mproxmlpath):
    global fpsheader
    global runcounter

    mpro_dict_header = {'systemid':'', 'systemkind':'', 'mediaid':'', 'mediakind':'', 'medianame':''}
    tree = ET.parse(mproxmlpath)
    root = tree.getroot()
    cliplist = []
    mediadir = mproxmlpath.split('/')
    del mediadir[-1]
    mediadir = '/'.join(mediadir) + '/'
    print "--Media Directory: ", mediadir

    for elem in root:
        for childs in elem:
            if childs.tag == '{http://xmlns.sony.net/pro/metadata/mediaprofile}Material':
                uri = childs.get('uri')
                cliplist.append(uri)
    #print cliplist
    clipcount = len(cliplist)
    print ("--Found %d Clips in XML\n") %clipcount

    for elem in root:
        for childs in elem:
            if childs.tag == '{http://xmlns.sony.net/pro/metadata/mediaprofile}System':
                systemid = childs.get('systemId')
                systemkind = childs.get('systemKind')
                mpro_dict_header['systemid'] = systemid
                mpro_dict_header['systemkind'] = systemkind
            if childs.tag == '{http://xmlns.sony.net/pro/metadata/mediaprofile}Attached':
                mediaid = childs.get('mediaId')
                mediakind = childs.get('mediaKind')
                medianame = childs.get('mediaName')
                mpro_dict_header['mediaid'] = mediaid
                mpro_dict_header['mediakind'] = mediakind
                mpro_dict_header['medianame'] = medianame

    for clips in cliplist:
        for elem in root:
            for childs in elem:
                if childs.tag == '{http://xmlns.sony.net/pro/metadata/mediaprofile}Material':
                    uri = ''
                    uri = childs.get('uri')
                    clipinfo = {'clipid': '', 'uri': '', 'videotype': '', 'achannels': '', 'fps': '', 'aspect': '',
                                'dur': '', 'umid': '', 'tcstart':'', 'tcend':'', 'creationdate':'', 'capfps':'', 'formfps':'', 'RecModel':'', 'RecSerial':'', 'CamModel':'', 'CamSerial':'',
                                'Lensattribute':'', 'ExpIndex':'', 'NDFilter':'', 'Shutterangle':'', 'ISO':'', 'WhiteBal':'', 'CaptureGamma':'', 'CDLGamma':'',
                                'CamAttribute':'', 'Markeraspect':'', 'ActiveArea':'', 'Pixelaspect':'', 'RawBlack':'', 'RawGrey':'', 'RawWhite':'', 'MonCurve':'',
                                'LookGamma':'', 'LookColor':'', 'PreCDLTransform':'', 'PostCDLTransform': '', 'LookBakedin':'', 'MonColorPrimary':'', 'MonDescriptor':'', 'Project':'',
                                'Director':'', 'DOP':'', 'Production':'', 'Camindex':'', 'Reel':'', 'Scene':'', 'Cut':'', 'Take':'', 'Shot':'', 'Tape':'', 'Tracks':'',
                                'Name':'', 'Source':'', 'Clip':'', 'LensInfo':''}
                    if uri == clips:
                        print "--Found Clip %s in XML" %uri
                        uri = childs.get('uri').split('/')
                        uri_orig = '/'.join(uri)
                        clipid = uri[2]
                        sourceclip = uri[-1]
                        del uri[0]
                        del uri[-1]
                        temppath = '/'.join(uri)
                        sourceclip_path = mediadir + temppath + '/' + sourceclip
                        print "--Path to Source Clip is:", sourceclip_path
                        clipxml_path = mediadir + temppath + '/' + clipid + 'M01.xml'
                        print "--Path to Clip XML is: ", clipxml_path
                        videotype = childs.get('videoType')
                        soundch = childs.get('ch')
                        fps = childs.get('fps')
                        fpsval = str(childs.get('fps'))
                        fpsval = fpsval[:2]
                        fpsheader = fpsval
                        if runcounter == 0:
                            writeheader(fpsheader)
                            runcounter += 1
                        fpsval = int(fpsval)
                        duration = childs.get('dur')
                        #fcount = int(duration)
                        #fcount = fcount + 1
                        #durationtc = Timecode(fpsval, frames=fcount)
                        aspect = childs.get('aspectRatio')
                        umid = childs.get('umid')

                        clipmeta_dict = parseclipxml(clipxml_path, umid, clipid, sourceclip_path, sourceclip) #todohere: parse each clip xml and add info to dict according clips

                        clipinfo.update({'clipid':clipid, 'uri':uri_orig, 'videotype':videotype, 'achannels':soundch, 'fps':fps, 'aspect':aspect, 'dur':duration, 'umid':umid,
                                         'tcstart': '', 'tcend': '', 'creationdate': '', 'capfps': '', 'formfps': '',
                                         'RecModel': '', 'RecSerial': '', 'CamModel': '', 'CamSerial': '',
                                         'Lensattribute': '', 'ExpIndex': '', 'NDFilter': '', 'Shutterangle': '',
                                         'ISO': '', 'WhiteBal': '', 'CaptureGamma': '', 'CDLGamma': '',
                                         'CamAttribute': '', 'Markeraspect': '', 'ActiveArea': '', 'Pixelaspect': '',
                                         'RawBlack': '', 'RawGrey': '', 'RawWhite': '', 'MonCurve': '',
                                         'LookGamma': '', 'LookColor': '', 'PreCDLTransform': '', 'PostCDLTransform': '', 'LookBakedin': '',
                                         'MonColorPrimary': '', 'MonDescriptor': '', 'Project': '',
                                         'Director': '', 'DOP': '', 'Production': '', 'Camindex': '', 'Reel': '',
                                         'Scene': '', 'Cut': '', 'Take': '', 'Shot': '', 'Tape': '', 'Tracks':'', 'Name':'', 'Source':'', 'Clip':'', 'LensInfo':''
                                         })
                        clipnamecount = "CLIP_" + str(clipid)

                        for k, v in iter(clipmeta_dict.items()):
                            clipinfo[k] = v
                            #print "clipmeta"
                            #print(k, v)

                        mpro_dict_header[clipnamecount] = clipinfo

                        #print childs.tag, childs.attrib

    return mpro_dict_header


def parseclipxml(clipxmlpath, umid, clipid, sourceclip_path, sourceclip):
    exists = os.path.isfile(clipxmlpath)
    source_exists = os.path.isfile(sourceclip_path)

    if source_exists is True:
        print "--Found Source File: ", sourceclip_path
    else:
        print "--Source File not found!--> ", sourceclip_path

    if exists is True:

        tree = ET.parse(clipxmlpath)
        root = tree.getroot()
        clipxmldict = {'tcstart':'', 'tcend':'', 'creationdate':'', 'capfps':'', 'formfps':'', 'RecModel':'', 'RecSerial':'', 'CamModel':'', 'CamSerial':'',
                       'Lensattribute':'', 'ExpIndex':'', 'NDFilter':'', 'Shutterangle':'', 'ISO':'', 'WhiteBal':'', 'CaptureGamma':'', 'CDLGamma':'',
                       'CamAttribute':'', 'Markeraspect':'', 'ActiveArea':'', 'Pixelaspect':'', 'RawBlack':'', 'RawGrey':'', 'RawWhite':'', 'MonCurve':'',
                       'LookGamma':'', 'LookColor':'', 'PreCDLTransform':'', 'PostCDLTransform': '', 'LookBakedin':'', 'MonColorPrimary':'', 'MonDescriptor':'', 'Project':'',
                       'Director':'', 'DOP':'', 'Production':'', 'Camindex':'', 'Reel':'', 'Scene':'', 'Cut':'', 'Take':'', 'Shot':'', 'Tape':'', 'Tracks':'',
                       'Name':'', 'Source':'', 'Clip':'', 'LensInfo':''}

        for elem in root:
            if elem.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}TargetMaterial':
                umidref = elem.get('umidRef')
                if umidref == umid:
                    clipxmldict = {'tcstart': '', 'tcend': '', 'creationdate': '', 'capfps': '', 'formfps': '',
                                   'RecModel': '', 'RecSerial': '', 'CamModel': '', 'CamSerial': '', 'Manufacturer':'',
                                   'Lensattribute': '', 'ExpIndex': '', 'NDFilter': '', 'Shutterangle': '', 'ISO': '',
                                   'WhiteBal': '', 'CaptureGamma': '', 'CDLGamma': '',
                                   'CamAttribute': '', 'Markeraspect': '', 'ActiveArea': '', 'Pixelaspect': '',
                                   'RawBlack': '', 'RawGrey': '', 'RawWhite': '', 'MonCurve': '',
                                   'LookGamma': '', 'LookColor': '', 'PreCDLTransform': '', 'PostCDLTransform': '', 'LookBakedin': '',
                                   'MonColorPrimary': '', 'MonDescriptor': '', 'Project': '',
                                   'Director': '', 'DOP': '', 'Production': '', 'Camindex': '', 'Reel': '', 'Scene': '',
                                   'Cut': '', 'Take': '', 'Shot': '', 'Tape': '', 'Tracks':'', 'Name':'', 'Source':'', 'Clip':'', 'LensInfo':''}
                    print "--Found matching umid-- "
                    clipxmldict['Tape'] = clipid
                    clipxmldict['Name'] = sourceclip
                    clipxmldict['Clip'] = sourceclip
                    clipxmldict['Source'] = sourceclip_path

                    for data in root:
                        #print data.tag, data.attrib
                        if data.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}CreationDate':
                            cdate = data.get('value')
                            clipxmldict['creationdate'] = cdate
                        if data.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Device':
                            recserial = data.get('serialNo')
                            clipxmldict['RecSerial'] = recserial
                            recmodel = data.get('modelName')
                            clipxmldict['RecModel'] = recmodel
                        if data.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Camera':
                            camserial = data.get('serialNo')
                            clipxmldict['CamSerial'] = camserial
                            modelname = data.get('modelName')
                            clipxmldict['CamModel'] = modelname
                            manufact = data.get('manufacturer')
                            clipxmldict['Manufacturer'] = manufact
                        if data.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}AudioFormat':
                            achnumber = data.get('numOfChannel')
                            trackslist = []
                            achnumber = int(achnumber)
                            trackslist.append('V')
                            for i in range(1, achnumber + 1):
                                trackslist.append('A' + str(i))
                            tracks = ''.join(trackslist)
                            clipxmldict['Tracks'] = str(tracks)
                        if data.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Lens':
                            lensinfo = data.get('modelName')
                            clipxmldict['LensInfo'] = lensinfo
                            #print "Lens: ", lensinfo


                        for childs in data:
                            if childs.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}LtcChange':
                                status = childs.get('status')
                                clipframecount = childs.get('frameCount')
                                #print "Framecount", clipframecount
                                if status == 'increment' and clipframecount == "0":
                                    tcraw_start = childs.get('value')
                                    tcstart = '%s:%s:%s:%s' % (tcraw_start[6:], tcraw_start[4:6], tcraw_start[2:4], tcraw_start[0:2])
                                    clipxmldict['tcstart'] = tcstart
                                if status == 'end':
                                    tcraw_end = childs.get('value')
                                    tcendframes = int(tcraw_end[0:2])
                                    tcendframes = tcendframes + 1
                                    tcendframes = str(tcendframes)
                                    if len(tcendframes) == 1:
                                        tcendframes = '0' + tcendframes
                                    tcend = '%s:%s:%s:%s' % (tcraw_end[6:], tcraw_end[4:6], tcraw_end[2:4], tcendframes)
                                    clipxmldict['tcend'] = tcend
                            if childs.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}VideoFrame':
                                capfps = childs.get('captureFps')
                                clipxmldict['capfps'] = capfps
                                formfps = childs.get('formatFps')
                                clipxmldict['formfps'] = formfps
                            if childs.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Group':
                                for childs_items in childs:
                                    if childs_items.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Item':
                                        c_attrib = childs_items.get('name')
                                        if c_attrib == 'LensAttributes':
                                            lensdata = childs_items.get('value')
                                            clipxmldict['Lensattribute'] = lensdata
                                        if c_attrib == 'ExposureIndexOfPhotoMeter':
                                            expindex = childs_items.get('value')
                                            clipxmldict['ExpIndex'] = expindex
                                        if c_attrib == 'NeutralDensityFilterWheelSetting':
                                            ndfilter= childs_items.get('value')
                                            clipxmldict['NDFilter'] = ndfilter
                                        if c_attrib == 'ShutterSpeedAngle':
                                            shutter = childs_items.get('value')
                                            clipxmldict['Shutterangle'] = shutter
                                        if c_attrib == 'ISOSensitivity':
                                            iso = childs_items.get('value')
                                            clipxmldict['ISO'] = iso
                                        if c_attrib == 'WhiteBalance':
                                            white = childs_items.get('value')
                                            clipxmldict['WhiteBal'] = white
                                        if c_attrib == 'CaptureGammaEquation':
                                            capgamma = childs_items.get('value')
                                            clipxmldict['CaptureGamma'] = capgamma
                                        if c_attrib == 'GammaForCDL':
                                            cdlgamma = childs_items.get('value')
                                            clipxmldict['CDLGamma'] = cdlgamma
                                        if c_attrib == 'CameraAttributes':
                                            camattrib = childs_items.get('value')
                                            clipxmldict['CamAttribute'] = camattrib
                                        if c_attrib == 'EffectiveMarkerAspectRatio':
                                            maspect = childs_items.get('value')
                                            clipxmldict['Markeraspect'] = maspect
                                        if c_attrib == 'ActiveAreaAspectRatio':
                                            activeaspect = childs_items.get('value')
                                            clipxmldict['ActiveArea'] = activeaspect
                                        if c_attrib == 'RawBlackCodeValue':
                                            rawblack = childs_items.get('value')
                                            clipxmldict['RawBlack'] = rawblack
                                        if c_attrib == 'RawGrayCodeValue':
                                            rawgrey = childs_items.get('value')
                                            clipxmldict['RawGrey'] = rawgrey
                                        if c_attrib == 'RawWhiteCodeValue':
                                            rawwhite = childs_items.get('value')
                                            clipxmldict['RawWhite'] = rawwhite
                                        if c_attrib == 'MonitoringBaseCurve':
                                            moncurve = childs_items.get('value')
                                            clipxmldict['MonCurve'] = moncurve
                                        if c_attrib == 'GammaForLook':
                                            lookgamma = childs_items.get('value')
                                            clipxmldict['LookGamma'] = lookgamma
                                        if c_attrib == 'ColorForLook':
                                            lookcolor = childs_items.get('value')
                                            clipxmldict['LookColor'] = lookcolor
                                        if c_attrib == 'PreCDLTransform':
                                            cdllut = childs_items.get('value')
                                            clipxmldict['PreCDLTransform'] = cdllut
                                        if c_attrib == 'PostCDLTransform':
                                            postcdllut = childs_items.get('value')
                                            clipxmldict['PostCDLTransform'] = postcdllut
                                        if c_attrib == 'LookProcessBaked':
                                            bakedlook = childs_items.get('value')
                                            clipxmldict['LookBakedin'] = bakedlook
                                        if c_attrib == 'MonitoringColorPrimaries':
                                            moncolor = childs_items.get('value')
                                            clipxmldict['MonColorPrimary'] = moncolor
                                        if c_attrib == 'MonitoringDescriptions':
                                            mondesc = childs_items.get('value')
                                            clipxmldict['MonDescriptor'] = mondesc
                            if childs.tag == '{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10}Meta':
                                meta_attrib = childs.get('name')
                                if meta_attrib == 'Project':
                                    project = childs.get('content')
                                    clipxmldict['Project'] = project
                                if meta_attrib == 'DirectorName':
                                    director = childs.get('content')
                                    clipxmldict['Director'] = director
                                if meta_attrib == 'DirectorOfPhotographyName':
                                    dop = childs.get('content')
                                    clipxmldict['DOP'] = dop
                                if meta_attrib == 'Production':
                                    production = childs.get('content')
                                    clipxmldict['Production'] = production
                                if meta_attrib == 'CameraIndex':
                                    camindex = childs.get('content')
                                    clipxmldict['Camindex'] = camindex
                                if meta_attrib == 'Reel':
                                    reel = childs.get('content')
                                    clipxmldict['Reel'] = reel
                                if meta_attrib == 'Scene':
                                    scene = childs.get('content')
                                    clipxmldict['Scene'] = scene
                                if meta_attrib == 'Cut':
                                    cut = childs.get('content')
                                    clipxmldict['Cut'] = cut
                                if meta_attrib == 'Take':
                                    take = childs.get('content')
                                    clipxmldict['Take'] = take
                                if meta_attrib == 'Shot':
                                    shot = childs.get('content')
                                    clipxmldict['Shot'] = shot

                            #print childs.tag, childs.attrib
                            #for children in childs:

                                #print children.tag, children.attrib
                    #print clipxmldict
        return clipxmldict
    else:
        print "--Clip XML File not found!-->", clipxmlpath


def writeheader(fpsinfo):  #For Avid ALE mandatory: Name, Tracks, TCStart, TCEnd, Tape (only Integer)
    global alefilepath
    print ('>> Please set ALE File to be saved!')
    root = Tk()
    root.withdraw()
    root.filename = tkFileDialog.asksaveasfilename(title="Save ALE")
    alefilepath = root.filename
    if len(root.filename) > 0:
        print ('--Saving File: %s ' % root.filename)
        file = open(root.filename, 'w')
        file.write('Heading' + '\n' + 'FIELD_DELIM' + '\t' + 'TABS' + '\n' + 'VIDEO_FORMAT' + '\t' + '1080' + '\n' + 'FPS' + '\t' + fpsinfo + '\n')
        file.write('\n' + 'Column' + '\n')
        file.write('Name' + '\t' + 'Tracks' + '\t' + 'Start' + '\t' + 'End' + '\t' + 'Tape' + '\t' + 'Iso' + '\t' + 'Aspect' + '\t' + 'CamAttrib' +
                   '\t' + 'LookColor' + '\t' + 'Expindex' + '\t' + 'Whitebalance' + '\t' + 'Camera' + '\t' + 'Camroll' + '\t' + 'Orig Media' +
                   '\t' + 'Reel' + '\t' + 'PreCDLtransform' + '\t' + 'Videotype' + '\t' + 'UMID' + '\t' + 'Shutter' + '\t' + 'LookGamma' +
                   '\t' + 'Lensattribute' + '\t' + 'MonColorPrimary' + '\t' + 'Manufacturer' + '\t' + 'Camserial' + '\t' + 'RecSerial' + '\t' + 'CamModel' +
                   '\t' + 'RecModel' + '\t' + 'MonCurve' + '\t' + 'NDFilter' + '\t' + 'Lookbakedin' + '\t' + 'RawGrey' + '\t' + 'RawBlack' + '\t' + 'RawWhite' +
                   '\t' + 'Formatfps' + '\t' + 'Capturefps' + '\t' + 'Shoot Date' + '\t' + 'CDLGamma' + '\t' + 'PostCDLTrans' + '\t' + 'ActiveArea' +
                   '\t' + 'Markeraspect' + '\t' + 'ProjectName' + '\t' + 'Production' + '\t' + 'Director' + '\t' + 'DoP' + '\t' + 'Medianame' + '\t' + 'Mediakind' +
                   '\t' + 'MediaID' + '\t' + 'Systemkind' + '\t' + 'SystemID' + '\t' + 'LensInfo' + '\n')
        file.write('Data' + '\n')
        file.close()


def writedata(clipmeta):
    global alefilepath
    #print clipmeta
    linedata = []
    for i in range(1, 51):
        linedata.append('')
    data_to_write = ''
    avidreel = avidcam = xmlreel = ''
    medianame = mediakind = mediaid = systemkind = systemid = ''

    #print len(linedata)

    file = open(alefilepath, 'a')

    for x, y in clipmeta.items():
        if x == 'medianame':
            medianame = y
        if x == 'mediakind':
            mediakind = y
        if x == 'mediaid':
            mediaid = y
        if x == 'systemkind':
            systemkind = y
        if x == 'systemid':
            systemid = y

    for keys, values in clipmeta.items():
        if keys.startswith('CLIP_'):
            print "\n> KeyClip: ", keys
            if type(values) is dict:
                for key, value in values.iteritems():
                    #print (key, value)
                    if key == 'Clip':
                        linedata[0] = value
                    if key == 'tcstart':
                        linedata[2] = str(value)
                    if key == 'tcend':
                        linedata[3] = str(value)
                    if key == 'Tracks':
                        linedata[1] = value
                    if key == 'Tape':
                        linedata[4] = value
                    if key == 'ISO':
                        linedata[5] = value
                    if key == 'aspect':
                        linedata[6] = value
                    if key == 'CamAttribute':
                        linedata[7] = value
                    if key == 'LookColor':
                        linedata[8] = value
                    if key == 'ExpIndex':
                        linedata[9] = value
                    if key == 'WhiteBal':
                        linedata[10] = value
                    if key == 'Camindex':
                        linedata[11] = value
                        avidcam = value
                    if key == 'Reel':
                        linedata[12] = value
                        xmlreel = value
                    if key == 'Source':
                        linedata[13] = value
                    if key == 'PreCDLTransform':
                        linedata[15] = value
                    if key == 'videotype':
                        linedata[16] = value
                    if key == 'umid':
                        linedata[17] = value
                    if key == 'Shutterangle':
                        linedata[18] = value
                    if key == 'LookGamma':
                        linedata[19] = value
                    if key == 'Lensattribute':
                        linedata[20] = value
                    if key == 'MonColorPrimary':
                        linedata[21] = value
                    if key == 'Manufacturer':
                        linedata[22] = value
                    if key == 'CamSerial':
                        linedata[23] = value
                    if key == 'RecSerial':
                        linedata[24] = value
                    if key == 'CamModel':
                        linedata[25] = value
                    if key == 'RecModel':
                        linedata[26] = value
                    if key == 'MonCurve':
                        linedata[27] = value
                    if key == 'NDFilter':
                        linedata[28] = value
                    if key == 'LookBakedin':
                        linedata[29] = value
                    if key == 'RawGrey':
                        linedata[30] = value
                    if key == 'RawBlack':
                        linedata[31] = value
                    if key == 'RawWhite':
                        linedata[32] = value
                    if key == 'formfps':
                        linedata[33] = value
                    if key == 'capfps':
                        linedata[34] = value
                    if key == 'creationdate':
                        linedata[35] = value
                    if key == 'CDLGamma':
                        linedata[36] = value
                    if key == 'PostCDLTransform':
                        linedata[37] = value
                    if key == 'ActiveArea':
                        linedata[38] = value
                    if key == 'Markeraspect':
                        linedata[39] = value
                    if key == 'Project':
                        linedata[40] = value
                    if key == 'Production':
                        linedata[41] = value
                    if key == 'Director':
                        linedata[42] = value
                    if key == 'DOP':
                        linedata[43] = value
                    if key == 'LensInfo':
                        linedata[49] = value


            avidreel = avidcam + xmlreel
            linedata[14] = avidreel
            if medianame:
                linedata[44] = medianame
            if mediakind:
                linedata[45] = mediakind
            if mediaid:
                linedata[46] = mediaid
            if systemid:
                linedata[47] = systemid
            if systemkind:
                linedata[48] = systemkind

            #print "Linedata 49: ", linedata[49]

            data_to_write = '\t'.join(linedata)
            data_to_write = data_to_write + '\n'
            #print "DATA TO WRITE: ", data_to_write
            file.write(data_to_write)
            avidreel = ''
            linedata = []
            for j in range(1, 51):
                linedata.append('')

    file.close()




def main():
    global fpsheader
    #clipdata_list = []
    sdir = searchdir()
    print '--Searching in--: ' + sdir
    mpro_list = searchfiles(sdir, 'MEDIAPRO.xml')
    if len(mpro_list) > 0:
        print ('--Found %d MEDIAPRO XMLs:' % len(mpro_list))
        for xmlfiles in mpro_list:
            print xmlfiles + '\n'

        for mpro_list_items in mpro_list:
            mpro_data = parse_mproxml(mpro_list_items)
            #print mpro_data
            writedata(mpro_data)

    else:
        print ('--Found no MEDIAPRO XMLs!')
        sys.exit(0)



main()