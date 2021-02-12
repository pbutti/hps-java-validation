import os,sys
import ROOT as r

from optparse import OptionParser

#path = "/u/ea/pbutti/public_html/alignment_monitoring_files/"

colors = [r.kRed, r.kBlue, r.kBlack, r.kGreen+2, r.kOrange-2,r.kTeal-5]

parser=OptionParser()
parser.add_option("-i","--indir",dest="indir",help="inputdir",metavar="indir",default="nominal_10031")
parser.add_option("-f","--inputFile",dest="inputFile",help="inputFile",metavar="inputFile",default="")
parser.add_option("-o","--outdir",dest="outdir",help="outdir",metavar="outdir",default="")
(config,sys.argv[1:]) = parser.parse_args(sys.argv[1:])

legName=(config.inputFile.split("/")[-1]).strip("_gblmon.root")
if ("_AlignmentMonitoring" in legName):
    legName=(legName).replace("_AlignmentMonitoring", "")
if ("_MPIIdata" in legName):
    legName=legName.replace("_MPIIdata","")
if ("_projections" in legName):
    legName=legName.replace("_projections","")

print legName
 
refName = (config.indir)
if ("/" in refName):
    refName = (refName.strip("/")).split("/")[-1]
legends     = [refName,legName]
outdir     = config.outdir
inputFiles = []
oFext = ".pdf"
