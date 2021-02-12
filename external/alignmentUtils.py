from ROOT import *

def MakeFit(histoGram, fitType, markerColor):

    #make sure the styles are integers
    markerColor = int(markerColor)

    #no Fit
    if fitType=="noFit":
        return None
    elif fitType=="singleGausIterative":
        fit = singleGausIterative(histoGram, 2)

    fit.SetLineColor(markerColor)
    
    return fit


def singleGausIterative(hist, sigmaRange):
     debug = False
     # first perform a single Gaus fit across full range of histogram
     min = hist.GetBinLowEdge(1)
     max = (hist.GetBinLowEdge(hist.GetNbinsX()))+hist.GetBinWidth(hist.GetNbinsX())
     fitA = TF1("fitA", "gaus", min,max)
     hist.Fit("fitA","ORQN","same")
     fitAMean = fitA.GetParameter(1)
     fitASig = fitA.GetParameter(2)
 
     # performs a second fit with range determined by first fit
     max = fitAMean + (fitASig*sigmaRange)
     min = fitAMean - (fitASig*sigmaRange)
     fitB = TF1("fitB", "gaus", min,max)
     hist.Fit("fitB","ORQN","same")
     fitMean = fitB.GetParameter(1)
     fitSig = fitB.GetParameter(2)
     
     newFitSig = 99999
     newFitMean = 99999
     i = 0
     max = fitMean + (fitSig*sigmaRange)
     min = fitMean - (fitSig*sigmaRange)
     fit = TF1("fit", "gaus", min,max)
 
     while abs(fitSig - newFitSig) > 0.0005 or abs(fitMean - newFitMean) > 0.0005:
         
         if(i > 0):
             fitMean = newFitMean
             fitSig = newFitSig
         #print "i = ",i," fitMean = ",fitMean," fitSig = ",fitSig
         max = fitMean + (fitSig*sigmaRange)
         min = fitMean - (fitSig*sigmaRange)
         fit.SetRange(min,max)
         hist.Fit("fit","ORQN","same")
         newFitMean = fit.GetParameter(1)
         newFitSig = fit.GetParameter(2)
         #print "i = ",i," newFitMean = ", newFitMean, " newFitSig = ",newFitSig
         if(i > 50):
             if debug:
                 print "WARNING terminate iterative gaus fit because of convergence problems"
                 print "final mean =  ", newFitMean, ", previous iter mean = ", fitMean
                 print "final sigma =  ", newFitSig, ", previous iter sigma = ", fitSig
             break
 
         i = i + 1
 
 
 
     if debug:
         print "Final i = ",i," finalFitMean = ", fit.GetParameter(1), " finalFitSig = ",fit.GetParameter(2)
 
     fit.SetLineWidth(2)
     
     return fit
