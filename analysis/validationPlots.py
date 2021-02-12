import ROOT as r
import sys,os
sys.path.append("../external")

import utilities as utils
from plotModResAndKinks import doLegend

colors=[r.kBlack,r.kRed+2,r.kBlue+2,r.kGreen+3]

r.gStyle.SetOptStat(0)


def do2019FEEComparison(baseDir, testDirs, plotName, reference):
    
    
    #PhysRun2019FeeReconTest-ref.root
    rootFile = "PhysRun2019FeeReconTest.root"
    outDir   = "./fee_2019_validation"
    refFile  = reference + "/" + "PhysRun2019FeeReconTest-ref.root"
    

    if (not os.path.exists(outDir)):
        os.mkdir(outDir)
        
    #The input files

    fileList = [baseDir+x+"/FEE_MC/"+rootFile for x in testDirs]

    # For testing purposes only
    #legends  = [(x.split("-")[-1])[:6] for x in testDirs]
    legends = ["pass1-dev"]
    
    #The reference file
    fileList.append(refFile)
    legends.append("reference")
    
    #Open the root files
    
    print fileList 
    inputFiles = []
    for inputFile in fileList:
        inputFiles.append(r.TFile(inputFile))
        
    # The histograms
        
    histos = []
    
    for iF in inputFiles:
        histos.append(iF.Get(plotName))


    plotName = plotName.split("/")[-1]
    makeValidPlot(outDir,histos,plotName,legends, legendLocation=3,max_scale=2.)
    

def do2016FEEComparison(baseDir, testDirs, plotName, reference):
    
    #PhysRun2016FeeReconTest.root
    rootFile = "PhysRun2016FeeReconTest.root"
    outDir   = "./fee_2016_validation"
    refFile  = reference+"/"+"PhysRun2016FeeReconTest-ref.root"
    
    if (not os.path.exists(outDir)):
        os.mkdir(outDir)
        
    #The input files
    fileList = [baseDir+x+"/target/test-output/PhysRun2016FeeReconTest/"+rootFile for x in testDirs]
    legends  = [(x.split("-")[-1])[:6] for x in testDirs]
    
    #The reference file
    fileList.append(reference+"/"+rootFile)
    legends.append("reference")
    
    #Open the root files
    inputFiles = []
    for inputFile in fileList:
        inputFiles.append(r.TFile(inputFile))

    #The histograms
    histos = []
    
    for iF in inputFiles:
        histos.append(iF.Get(plotName))


    makeValidPlot(outDir,histos,plotName,legends,legendLocation=3)
    
    


def makeValidPlot(outDir,histos,plotName,legends,legendLocation=4,max_scale=1.4):
    
    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
            
    titleName = plotName.replace(" ","_")
            
    #Options
    #Normalise 
    maximum = -1 
    doNormalise = False
    
    if doNormalise:
        for histo in histos:
            if abs(histo.Integral()) > 1e-8:
                histo.Scale(1./histo.Integral())

            #Get the maximum
            if (histo.GetMaximum() > maximum):
                maximum = histo.GetMaximum()


    c.SetMargin(0,0,0,0)
    top = r.TPad("top","top",0,0.42,1,1)
    bot = r.TPad("bot","bot",0,0,1,0.38)
    top.Draw()
    top.SetBottomMargin(0)
    top.SetTopMargin(r.gStyle.GetPadTopMargin()*utils.topScale)
    bot.Draw()
    bot.SetTopMargin(0)
    bot.SetBottomMargin(0.4)
    top.cd()


    
    for ihisto in xrange(len(histos)):
        
        histos[ihisto].SetMarkerStyle(20)
        if ("Hits" not in titleName and "hits" not in titleName):
            histos[ihisto].Rebin(2)
        else:
            legendLocation = 3
        histos[ihisto].SetMarkerSize(0.5)
        histos[ihisto].Sumw2()
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].GetXaxis().SetLabelSize(0.05)
        histos[ihisto].GetYaxis().SetLabelSize(0.05)
        histos[ihisto].SetLineWidth(2)
        
        

        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(titleName)
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(0.9)
            if (doNormalise): 
                histos[ihisto].SetMaximum(maximum*1.5)
            else:
                histos[ihisto].SetMaximum(histos[ihisto].GetMaximum()*max_scale)
                
            histos[ihisto].Draw("h")

        else:
            histos[ihisto].Draw("hsame")
        

        leg = doLegend(histos,legends,legendLocation)
        leg.SetBorderSize(0)
        
        if (leg != None):
            leg.Draw()


    #-- Ratio --#
            
    bot.cd()
    #-- Take the last histogram. That's the reference --#
    reference = histos[-1].Clone("reference")
    reference.GetXaxis().SetLabelSize(0.1)
    reference.GetXaxis().SetTitleSize(0.1)
    reference.GetXaxis().SetTitle(titleName)
    reference.GetYaxis().SetTitle("Ratio")
    reference.GetYaxis().SetTitleSize(0.1)
    reference.GetYaxis().SetLabelSize(0.1)
    reference.GetYaxis().SetTitleOffset(reference.GetYaxis().GetTitleOffset()*0.7)
    reference.GetYaxis().SetRangeUser(0.3,3.1)
    reference.GetYaxis().SetNdivisions(508)
    reference.GetYaxis().SetDecimals(True)
    reference.Draw("axis")

    for ih in range(0,len(histos)-1):
        # make an unique name to avoid memory issues
        ForRatio = histos[ih].Clone("ForRatio"+str(ih)+histos[ih].GetName())
        # adjust
        ForRatio.SetMaximum(100.)
        # divide by ref
        ForRatio.Divide(reference)
        # draw a copy to avoid creating conflicts.
        ForRatio.DrawCopy("pe same")
        
    # Put a line at 1
    line = r.TLine()
    line.SetLineStyle(r.kDashed)
    line.DrawLine(reference.GetXaxis().GetXmin(),1,reference.GetXaxis().GetXmax(),1)

        
    c.SaveAs(outDir+"/"+titleName+".pdf")

    


def do2016V0Comparison(baseDir, testDirs, plotName, reference):
    
    #PhysRun2016V0ReconTest.root
    rootFile    = "PhysRun2016V0ReconTest.root"
    outDir      = "./v0_2016_validation"
    refFile     = reference+"/"+"PhysRun2016V0ReconTest-ref.root"
    plotsFolder = "UnconstrainedV0Vertices"
    

    if (not os.path.exists(outDir)):
        os.mkdir(outDir)
        
    #The input files
    fileList = [baseDir+x+"/target/test-output/PhysRun2016V0ReconTest/"+rootFile for x in testDirs]
    legends  = [(x.split("-")[-1])[:6] for x in testDirs] 
    
    #The reference file
    fileList.append(reference+"/"+rootFile)
    legends.append("reference")

    #Open the root files
    inputFiles = []
    for inputFile in fileList:
        inputFiles.append(r.TFile(inputFile))

    #The histograms
    histos = []


    for iF in inputFiles:
        #h = iF.Get(plotsFolder+"/"+plotName)
        #h.SetDirectory(0)
        print plotsFolder+"/"+plotName
        histos.append(iF.Get(plotsFolder+"/"+plotName))
            
    
    makeValidPlot(outDir,histos,plotName,legends)
        

def main():

    inputBaseDir   = "/Users/pbutti/sw/hps-java-validation/plots/"
    
    #Max 4
    inputTestDirs  = ["integration-tests-447cf1a03c75be10174ff3d05",
                      #"integration-tests-68762eb41bc404d103671d3e7",
                      "integration-tests-5c4ad3bf648abac769afcb602aaa3595e26a7928",
                      #"integration-tests-7fc0885968113847ef9d6c3a9cff0951651566",
                      #"integration-tests-c485652938aed93e1"
                      "integration-tests-pass1devfix_68fe77b148d9b32d40a784c8e0e8d9a0279410d2"
                      ] 
    
    ReferenceFolder = "/Users/pbutti/sw/hps-java-validation/reference"
    
    # Style of plots

    utils.SetStyle()

    runV0Comparison  = False
    runFEEComparison = False
    run2019FEEComparison = True
    
    
    if runV0Comparison:
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Bottom Track Momentum",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Invariant Mass",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Momentum",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Top Track Momentum",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Track Number of Hits",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Vertex x",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Vertex y",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Vertex z",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 Vertex z L1L1",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 x Momentum",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 y Momentum",ReferenceFolder)
        do2016V0Comparison(inputBaseDir,inputTestDirs,"V0 z Momentum",ReferenceFolder)
        
    if runFEEComparison:

        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom 5 Hit Track Momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom 6 Hit Track Momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top 5 Hit Track Momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top 6 Hit Track Momentum",ReferenceFolder)
        
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track Momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track X0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track Y0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track Z0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track Chisq per DoF",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track theta",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Bottom Track Number of Hits",ReferenceFolder)

        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track Momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track X0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track Y0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track Z0",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track Chisq per DoF",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track theta",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Top Track Number of Hits",ReferenceFolder)

        do2016FEEComparison(inputBaseDir,inputTestDirs,"Track deDx",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Track theta",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"Track momentum",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"track data time",ReferenceFolder)
        
        do2016FEEComparison(inputBaseDir,inputTestDirs,"cluster nHits",ReferenceFolder)
        do2016FEEComparison(inputBaseDir,inputTestDirs,"clusterSeedHit energy",ReferenceFolder)
        



    inputTestDirs = ["2019_integrationTests"]

    if run2019FEEComparison:
        tracksDir="Tracks/GBLTracks/"

        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/Hits per Track",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/Mean time of hits on track",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/Track Chi2",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/Tracks per Event",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/d0",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/omega",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/sinphi",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/tan(lambda)",ReferenceFolder)
        do2019FEEComparison(inputBaseDir,inputTestDirs,tracksDir+"all/z0",ReferenceFolder)
                
        

if __name__=="__main__":
    main()
