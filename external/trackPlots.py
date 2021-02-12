import ROOT as r
import os,sys
sys.path.append("/Users/pbutti/sw/hpstr/plotUtils")

import utilities as utils
from commonConfig import * 

utils.SetStyle()

inFileList = [
    config.indir+"/nominal_gblmon.root",
    config.inputFile
]

inputFiles = []
legName=(config.inputFile.split("/")[-1]).strip(".root")

r.gROOT.SetBatch(1)

def trackPlots(inFileList,outdir,legends):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for ifile in inFileList:
        print "Loading ... ", ifile
        inf = r.TFile(ifile)
        inputFiles.append(inf)
        print inf
        pass

    plotFolder="trk_params/"
    charges  = ["","_neg","_pos"] #_neg #_pos
    vols  = ["_top","_bottom"] #_bottom
    variables=["Chi2","d0","z0","nHits","p","phi","tanLambda","trk_extr_bs_x","trk_extr_bs_y","trk_extr_bs_x_rk","trk_extr_bs_y_rk",]

    for crg in charges:
        for vol in vols:
            for var in variables:
                hname = plotFolder+var+vol+crg
                #### TEMPORARY ###
                ### BUG ###
                
                
                
                if ("pos" in crg):
                    corrcrg = "q-"
                elif ("neg" in crg):
                    corrcrg = "q+"
                else:
                    corrcrg = "All"
                    
                ### BUG ###
                
                print hname
                # File loop
                histos=[]
                
                for i_f in xrange(len(inputFiles)):
                    histo_u = inputFiles[i_f].Get(hname)
                    histos.append(histo_u)
                    pass

                can = utils.Make1DPlot(var+vol+crg,outdir,histos,legends,oFext,xtitle=var+" "+vol+" "+corrcrg,ytitle="tracks",RebinFactor=1, ymax=0.05,Normalise=True)
                    
                pass
            pass
        pass
    pass




