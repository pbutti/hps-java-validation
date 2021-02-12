import ROOT as r
import sys,os
sys.path.append("/Users/pbutti/sw/hpstr/plotUtils")

import utilities as utils

import trackPlots as tp
from alignmentUtils import *
import FEE_momentum_plots as feePlots

colors=[r.kBlack,r.kRed+2,r.kBlue+2,r.kGreen+3]

binLabels = ["","L1tA","L1tS","L2tA","L2tS","L3tA","L3tS","L4tA","L4tS","L5tAh","L5tSh","L5tAs","L5tSs","L6tAh","L6tSh","L6tAs","L6tSs","L7tAh","L7tSh","L7tAs","L7tSs"]
binLabels += ["","","","",""]
binLabels += ["L1bA","L1bS","L2bA","L2bS","L3bA","L3bS","L4bA","L4bS","L5bAh","L5bSh","L5bAs","L5bSs","L6bAh","L6bSh","L6bAs","L6bSs","L7bAh","L7bSh","L7bAs","L7bSs"]
binLabels += ["","","","","",""]
binLabels += ["","","","","",""]



r.gStyle.SetOptStat(0)


def doDerPlots(inputF, name, legends=[]):
    outDir = "./derivatives"
    
    if (not os.path.exists(outDir)):
        os.mkdir(outDir)

    histos = []

    for iF in inputF:
        histos.append(iF.Get("gbl_derivatives/"+name))
        
    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()

    titleName = name
    maximum = -1.
    
    for histo in histos:
        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())

        #Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()
    
    for ihisto in xrange(len(histos)):
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].GetXaxis().SetLabelSize(0.05)
        histos[ihisto].GetYaxis().SetLabelSize(0.05)
        histos[ihisto].SetLineWidth(3)
        
        

        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(titleName + " global derivative")
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(0.9)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].Draw("p")
            
            if "223" in name or "123" in name:
                if int(name[-2:]) < 4 :
                    histos[ihisto].GetXaxis().SetRangeUser(-25,25)
                else:
                    histos[ihisto].GetXaxis().SetRangeUser(-100,100)
            else:
                histos[ihisto].GetXaxis().SetRangeUser(-5,5)
        else:
            histos[ihisto].Draw("psame")

                    
    leg = doLegend(histos,legends,3)
    
    if (leg != None):
        leg.Draw()
    
    c.SaveAs(outDir+"/"+name+".pdf")
    

def doMultVtxPlots(inputF, legends=[]):
    histos_top = []
    histos_bot = []
    histos = []
    f_path = "MultiEventVtx/"
    
    for iF in inputF:
        histos_top.append(iF.Get("MultiEventVtx/vtx_z_top"))
        histos_bot.append(iF.Get("MultiEventVtx/vtx_z_bot"))
        histos.append(iF.Get("MultiEventVtx/vtx_z"))
        
    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
    
    for ihisto in xrange(len(histos)):
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].SetLineWidth(3)
        histos[ihisto].Rebin(2)
        if (ihisto==0):
            #histos[ihisto].GetYaxis().SetRangeUser(0.,1.)
            histos[ihisto].Draw()
        else:
            histos[ihisto].Draw("same")

    leg = doLegend(histos,legends)
    if (leg != None):
        leg.Draw()
    c.SaveAs("MultiEventVtx_z.pdf")

    histos2d_top = []
    for iF in inputF:
        histos2d_top.append(iF.Get(f_path+"/vtx_x_y_top"))
    utils.Make2DPlots("MultiEventVtx_x_y_top","./",histos2d_top,legends=legends,colors2d=colors)

    histos2d_bot = []
    for iF in inputF:
        histos2d_bot.append(iF.Get(f_path+"/vtx_x_y_bottom"))
    utils.Make2DPlots("MultiEventVtx_x_y_bot","./",histos2d_bot,legends=legends,xtitle="Multi Vtx FEE V_{x} [mm]",ytitle="Multi Vtx FEE V_{y} [mm]",colors2d=colors)

    histos2d = []
    for iF in inputF:
        histos1 = iF.Get(f_path+"/vtx_x_y_top")
        histos2 = iF.Get(f_path+"/vtx_x_y_bottom")
        histos1.Add(histos2)
        histos2d.append(histos1)
        
    utils.Make2DPlots("MultiEventVtx_x_y","./",histos2d,legends=legends,colors2d=colors)
    

#1: bottom right
#2: bottom center
#3: top right and bigger

def doLegend(histos,legends, location=1,plotProperties=[]):
    if len(legends) < len(histos):
        print "WARNING:: size of legends doesn't match the size of histos"
        return None
    leg = None
    xshift = 0.3
    yshift = 0.3
    if (location==1):
        leg = r.TLegend(0.65,0.3,0.90,0.15)
    if (location==2):
        leg = r.TLegend(0.40,0.3,0.65,0.15)
    if (location==3):
        leg = r.TLegend(0.15,0.90,0.15+xshift,0.90-yshift)
    if (location==4):
        xmin = 0.6
        leg = r.TLegend(xmin,0.90,xmin+xshift,0.90-yshift)
    for l in range(len(histos)):
        if (len(plotProperties)!=len(histos)):
            leg.AddEntry(histos[l],legends[l],'lpf')
        else:
            #splitline{The Data }{slope something }
            entry = "#splitline{"+legends[l]+"}{"+plotProperties[l]+"}"
            leg.AddEntry(histos[l],entry,'lpf')
        

    return leg

        
#def doLegend(histos,legends, location=1):
#    if len(legends) < len(histos):
#        print "WARNING:: size of legends doesn't match the size of histos"
#        return None
#    leg = None
#    if (location==1):
#        leg = r.TLegend(0.65,0.3,0.90,0.15)
#    if (location==2):
#        leg = r.TLegend(0.40,0.3,0.65,0.15)
#    for l in range(len(histos)):
#        leg.AddEntry(histos[l],legends[l],'lpf')
#
#    return leg

def plot1DResiduals(inputF,name,legends=[]):

    histos = []    
    for iF in inputF:
        histos.append(iF.Get("res/"+name))
    
    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
    titleName = name.split("_")[3] + "_"+name.split("_")[5]
    maximum = -1.
    
    fitList = []
    plotProperties = []

    #Normalise and get maximum after normalisation
    for histo in histos:
        
        #Normalise the histogram
        
        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())
            
        #Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()

    if ("slot") in name:
        titleName+="_slot"
    elif "hole" in name:
        titleName+="_hole"
    
    for ihisto in xrange(len(histos)):
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].GetXaxis().SetLabelSize(0.05)
        histos[ihisto].GetYaxis().SetLabelSize(0.05)
        histos[ihisto].SetLineWidth(3)
        
        

        #Fitting
        fitList.append(MakeFit(histos[ihisto],"singleGausIterative", utils.colors[ihisto]))
        
        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(titleName + " u-residual [mm]")
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(0.9)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].Draw("p")
        else:
            histos[ihisto].Draw("psame")

        fitList[ihisto].Draw("same")
        #Save fit properties

        mu = fitList[ihisto].GetParameter(1)
        mu_err = fitList[ihisto].GetParError(1)
        sigma = fitList[ihisto].GetParameter(2)
        sigma_err = fitList[ihisto].GetParError(2)
        
        #plotProperties.append((" #mu=%.3f"%round(mu,3))+("+/- %.3f"%round(mu_err,3))
        #                      +(" #sigma=%.3f"%round(sigma,3)) +("+/- %.3f"%round(sigma_err,3) ))
        
        plotProperties.append((" #mu=%.3f"%round(mu,3))
                              +(" #sigma=%.3f"%round(sigma,3)))

            
    leg = doLegend(histos,legends,3,plotProperties)
    
    if (leg != None):
        leg.Draw()
    
    c.SaveAs(name+".pdf")
    
def plotRes(inputF,legends=[]):

    histos=[]
    for iF in inputF:
        histos.append(iF.Get("res/uresidual_GBL_mod_p"))

    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
    
    for ihisto in xrange(len(histos)):
        print(ihisto,histos[ihisto])
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].SetLineWidth(3)

        
                
        if (ihisto==0):
            
            for ibin in range(0,histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(ibin+1,binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1,270);
            histos[ihisto].GetYaxis().SetRangeUser(-0.2,0.2)
            histos[ihisto].Draw("p")
        else:
            histos[ihisto].Draw("psame")

    leg = doLegend(histos,legends)
    if (leg != None):
        leg.Draw()
    c.SaveAs("uresiduals.pdf")

def plotLambdaKinks(inputF,legends=[]):
    histos=[]
    for iF in inputF:
        histos.append(iF.Get("gbl_kinks/lambda_kink_mod_p"))

    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
    
    for ihisto in xrange(len(histos)):
        print(ihisto,histos[ihisto])
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].SetLineWidth(3)
                
        if (ihisto==0):
            histos[ihisto].GetYaxis().SetRangeUser(-0.0002,0.0002)
            histos[ihisto].Draw("p")
        else:
            histos[ihisto].Draw("psame")

    leg = doLegend(histos,legends)
    if (leg != None):
        leg.Draw()
    c.SaveAs("lambda_kinks.pdf")


def plotPhiKinks(inputF,legends=[]):
    histos=[]
    for iF in inputF:
        histos.append(iF.Get("gbl_kinks/phi_kink_mod_p"))

    c = r.TCanvas()
    c.SetGridx()
    c.SetGridy()
    
    for ihisto in xrange(len(histos)):
        print(ihisto,histos[ihisto])
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(colors[ihisto])
        histos[ihisto].SetLineColor(colors[ihisto])
        histos[ihisto].SetLineWidth(3)
                
        if (ihisto==0):
            for ibin in range(0,histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(ibin+1,binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1,270);
            histos[ihisto].GetYaxis().SetRangeUser(-0.001,0.001)
            histos[ihisto].Draw("p")
        else:
            histos[ihisto].Draw("psame")

    leg = doLegend(histos,legends,2)
    if (leg != None):
        leg.Draw()
    c.SaveAs("phi_kinks.pdf")

def main():


    doTrackPlots = False
    doFEEs = False
    doResiduals = False
    doSummaryPlots = False
    doDerivatives = True

    #Style of plots

    utils.SetStyle()
    
    #MAX 4 FILES
    inputFiles=[

        
        
        #these filesare the ones I'm interested the most.
#
#                "AlignMonitoring_10103_FEESkims_TY_pass2_tight_TY_iter6.root",
#                "AlignMonitoring_10103_FEESkims_TY_TY_iter2.root",
#                "AlignMonitoring_10103_FEESkims_TY_TY_iter3.root",
#                "AlignMonitoring_10103_FEESkims_TY_TY_iter4.root",

        
        
        #"AlignMonitoring_10103_FEESkims_TY_TY_iter5.root",
        #"AlignMonitoring_10103_FEESkims_TY_pass2_tight_TY_iter6.root",
        #"AlignMonitoring_10103_FEESkims_TY_Nominal_iter0.root",
        
        #"AlignMonitoring_10103_FEESkims_TY_BOT_TY_SPLIT_iter1.root",        
        #"AlignMonitoring_9921_FEESkims_TY_BOT_TY_SPLIT_9921_iter2.root",
        #"AlignMonitoring_9921_FEESkims_TY_BOT_TY_SPLIT_9921_iter3.root",


        #"AlignMonitoring_10666_FEE_MC_2019_Nominal_iter0.root",
        #"AlignMonitoring_10103_FEESkims_TY_BOT_KF_TY_SPLIT_iter1.root",
        #"AlignMonitoring_10666_FEE_MC_2019_KF_Nominal_iter0.root"
        #"AlignMonitoring_10103_FEESkims_TY_MOMC_ONLY_SEL_TY_iter5.root",
        #"AlignMonitoring_10666_FEE_MC_2019_Nominal_iter0.root",
        #"FEE_MC.slcio_gblplots.root",


        #Derivative files
        "GBLRefitterDriverplots.root",
        "KalmanToGBLDriverplots.root"
        ]
    
    #legends=["6", "2","3","4"]    
    #legends = ["FEE 10103","Single e^{-} 4.5 GeV"]
    #legends  = ["Nominal Geo", "FEE 10103 iter5", "FEE MC",]
#    legends = ["Nominal","AllDof It3","AllDofIt3 L1-L4 It1","Older L1-L4 Iteration","wrongSign","TopUCAllDof iter2"]
    #legends = ["ModL1L4","TopUCAllDof + L1L4 TyTx","TopUCAllDof + L1L4 TyTx + momC" ]
    #legends = ["Nominal","ModL1L4","MOMC-it2","MOMC-UC"]
    #legends = ["With Survey Constants","Without Survey Constants","BSC-MOMC 0","BSC-MOMC 1"]#,"Align pD0 noC"]
    #legends =["Nominal","PASS4 iter3 NH", "ONLY Y"]
    #legends  = ["FEE 10103 Nominal Geo", "FEE 9921 align", "FEE 10103 align",]
    #legends  = ["9921 ST+GBL", "FEE MC", "10103 ST+GBL", "10103 KF+GBL"]
    #legends  = ["FEE MC STF+GBL", "FEE MC KF+GBL"]
    #legends  = ["FEE MC STF+GBL"]
    #legends  = ["FEE 10103 STF+GBL ali", "FEE 9921 STF+GBL UC level", "FEE 9921 STF+GBL module level"]
    legends = ["GBL rot der","KF rot der"]
    
    inputF = []
    for inputFile in inputFiles:
        inputF.append(r.TFile(inputFile))

    if doSummaryPlots:
        plotLambdaKinks(inputF,legends)
        plotPhiKinks(inputF,legends)
        
    
    if (doResiduals):
        
        plotRes(inputF,legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L1b_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L1b_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L2b_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L2b_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L3b_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L3b_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L4b_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L4b_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5b_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5b_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5b_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5b_halfmodule_stereo_slot_sensor0",legends)
        
        plot1DResiduals(inputF,"uresidual_GBL_module_L6b_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6b_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6b_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6b_halfmodule_stereo_slot_sensor0",legends)

        plot1DResiduals(inputF,"uresidual_GBL_module_L7b_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7b_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7b_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7b_halfmodule_stereo_slot_sensor0",legends)

        plot1DResiduals(inputF,"uresidual_GBL_module_L1t_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L1t_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L2t_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L2t_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L3t_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L3t_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L4t_halfmodule_axial_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L4t_halfmodule_stereo_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5t_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5t_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5t_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L5t_halfmodule_stereo_slot_sensor0",legends)
        
        plot1DResiduals(inputF,"uresidual_GBL_module_L6t_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6t_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6t_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L6t_halfmodule_stereo_slot_sensor0",legends)

        plot1DResiduals(inputF,"uresidual_GBL_module_L7t_halfmodule_axial_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7t_halfmodule_axial_slot_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7t_halfmodule_stereo_hole_sensor0",legends)
        plot1DResiduals(inputF,"uresidual_GBL_module_L7t_halfmodule_stereo_slot_sensor0",legends)
        
    
    #doMultVtxPlots(inputF,legends)
    
    
    if (doTrackPlots):
        tp.trackPlots(inputFiles,"trackPlots",legends)
    
    
    if (doFEEs):
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_bottom")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_top")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_slot_top")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_hole_top")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_slot_bottom")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p_hole_bottom")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p6h_top")
        feePlots.feeMomentumPlot(inputF,legends,"trk_params/p6h_bottom")
        #feePlots.feeMomentumPlot(inputF,legends,"trk_params/p7h_bottom")
        
        
    if (doDerivatives):
        print "doDerivatives"
        #doDerPlots(inputF,"12101", legends)
        #doDerPlots(inputF,"12201", legends)
        doDerPlots(inputF,"12301", legends)
        
        #doDerPlots(inputF,"22101", legends)
        #doDerPlots(inputF,"22201", legends)
        doDerPlots(inputF,"22301", legends)


        #doDerPlots(inputF,"12105", legends)
        #doDerPlots(inputF,"12205", legends)
        doDerPlots(inputF,"12305", legends)
        
        #doDerPlots(inputF,"22105", legends)
        #doDerPlots(inputF,"22205", legends)
        doDerPlots(inputF,"22305", legends)

        #doDerPlots(inputF,"12110", legends)
        #doDerPlots(inputF,"12210", legends)
        doDerPlots(inputF,"12310", legends)
        
        #doDerPlots(inputF,"22110", legends)
        #doDerPlots(inputF,"22210", legends)
        doDerPlots(inputF,"22310", legends)

        
        
        
if __name__=="__main__":
    main()




    






