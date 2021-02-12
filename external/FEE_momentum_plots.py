from ROOT import *
from alignmentUtils import *
import utilities as utils


def conditionHistos(histos):
    for ihisto in xrange(len(histos)):
        print(ihisto,histos[ihisto])
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(utils.colors[ihisto])
        histos[ihisto].SetLineColor(utils.colors[ihisto])
        histos[ihisto].SetLineWidth(3)
        

def feeMomentumPlot(inputF,legends,histopath): 
    
    c = TCanvas()
    c.SetGridx()
    c.SetGridy()
    
    histos = []
    for iF in inputF:
        histos.append(iF.Get(histopath))
    
    conditionHistos(histos)
    
    fitList = []
    plotProperties = []
    
    for ihisto in xrange(len(histos)):

        #Scale the histogram to unity
        histos[ihisto].Scale(1./histos[ihisto].Integral())
                
        fitList.append(MakeFit(histos[ihisto],"singleGausIterative", utils.colors[ihisto]))
        
        if (ihisto==0):
            histos[ihisto].Draw("p")
            histos[ihisto].GetYaxis().SetRangeUser(0,0.14)
        else:
            histos[ihisto].Draw("psame")
        
        fitList[ihisto].Draw("same")
        mu = fitList[ihisto].GetParameter(1)
        mu_err = fitList[ihisto].GetParError(1)
        sigma = fitList[ihisto].GetParameter(2)
        sigma_err = fitList[ihisto].GetParError(2)
        
        plotProperties.append((" #mu=%.3f"%round(mu,3))+("+/- %.3f"%round(mu_err,3))
                              +(" #sigma=%.3f"%round(sigma,3)) +("+/- %.3f"%round(sigma_err,3) ))
    
        
    leg = doLegend(histos,legends,3,plotProperties)
    
    leg.Draw("same")

    c.SaveAs(histopath.split("/")[-1]+".pdf")
        

#1: bottom right
#2: bottom center
#3: top right and bigger

def doLegend(histos,legends, location=1,plotProperties=[]):
    if len(legends) < len(histos):
        print "WARNING:: size of legends doesn't match the size of histos"
        return None
    leg = None
    if (location==1):
        leg = TLegend(0.65,0.3,0.90,0.15)
    if (location==2):
        leg = TLegend(0.40,0.3,0.65,0.15)
    if (location==3):
        leg = TLegend(0.2,0.90,0.50,0.6)
    for l in range(len(histos)):
        if (len(plotProperties)!=len(histos)):
            leg.AddEntry(histos[l],legends[l],'lpf')
        else:
            #splitline{The Data }{slope something }
            entry = "#splitline{"+legends[l]+"}{"+plotProperties[l]+"}"
            leg.AddEntry(histos[l],entry,'lpf')
        

    return leg
