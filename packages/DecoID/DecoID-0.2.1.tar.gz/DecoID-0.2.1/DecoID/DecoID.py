
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import sys
import os
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
from multiprocessing import Queue, Process,Manager,Value,Lock
from threading import Thread
import time
import gzip
import pickle as pkl
import dill
import pandas as pd
import uuid

import numpy as np
np.seterr(divide='ignore', invalid='ignore')

import scipy.optimize as opt
import sklearn.linear_model as linModel

from pyteomics import mzml

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

from bisect import bisect_left

MAXMASS = 3000


def collapseAsNeeded(spectra,targetRes):
    tempSpec = {np.round(x,targetRes):0 for x in spectra}
    for key,val in spectra.items():
        tempSpec[np.round(key,targetRes)] += val
    return tempSpec

def solveSystem(S,o,resPenalty,maxQuant=1000):
    return deconvolveLASSO(np.transpose(S), [[x] for x in o], [0 for _ in S], [maxQuant for _ in S], resPenalty=resPenalty)

def normalizeSpectra(spectra,method="sum"):
    if method == "sum": maxSpec = np.sum(spectra)
    else: maxSpec = np.max(spectra)
    if np.isinf(np.power(np.float(maxSpec/maxSpec),2)) or np.isnan(np.power(np.float(maxSpec/maxSpec),2)):
        return [0.0 for x in spectra]
    normSpec = [x/maxSpec for x in spectra]
    if np.max(normSpec) > 1.1:
        return [0.0 for x in spectra]
    return [x/maxSpec for x in spectra]

def isPossible(query,candidate,threshold=.75):
    if len(candidate.keys()) == 0:
        return False
    if len(set(query.keys()).intersection(set(candidate.keys())))/float(len(candidate.keys())) > threshold:
        return True
    else:
        return False


def findMaxL1Norm(A,b):
    func = lambda x:np.dot(np.transpose(np.subtract(b,np.dot(A,x*np.ones((len(A[0]),1))))),np.subtract(b,np.dot(A,x*np.ones((len(A[0]),1)))))
    sol = opt.minimize_scalar(func,options={"maxiter":100},tol=1e-1)
    val = sol.x
    return val*len(A[0])

def checkPSD(x):
    delta = .1 * np.mean(flatten(x))
    try:
        np.linalg.cholesky(x)
        return True
    except:
        if np.all(np.linalg.eigvals(x) >= 0):
            return True
        else:
            return False

def deconvolveLASSO(A, b, lb, ub, resPenalty=10,numRepeats = 10):

    scores = []
    sparseQ = True
    if resPenalty == 0:
        sparseQ = False
        resPenalty = 1
    if np.isinf(resPenalty):
        return [[0 for _ in A[0]],0.0]
    if sparseQ:
        model = linModel.Lasso(alpha=resPenalty, fit_intercept=False, positive=True)
        A = np.asfortranarray(A)
        model.fit(A,b,check_input=False)
        params = [[x] for x in model.coef_]
        foundSpectra = np.dot(A,params)
        s2nR = np.sum(flatten(foundSpectra))/np.sum(np.abs(np.subtract(flatten(foundSpectra),flatten(b))))
        return [flatten(params),s2nR]
    else:
        params,_ = opt.nnls(np.array(A),np.array(flatten(b)),maxiter=1e4)
        foundSpectra = np.dot(A, params)
        s2nR = np.sum(flatten(foundSpectra)) / np.sum(
             np.abs(np.subtract(flatten(foundSpectra), flatten(b))))
        return [flatten(params),s2nR]

def dotProductSpectra(foundSpectra,b):

    if type(foundSpectra) == type(dict()):
        mzs = set(foundSpectra.keys()).intersection(set(b.keys()))
        num = np.sum([foundSpectra[x]*b[x] for x in mzs])
        denom = np.sqrt(np.sum([x**2 for x in foundSpectra.values()])*sum([x**2 for x in b.values()]))
        val = num/denom
        return num/denom
    else:
        b = flatten(b)
        foundSpectra = flatten(foundSpectra)
        val = np.sum([x*y for x,y in zip(b,foundSpectra) if x > 1e-4 or y > 1e-4])/np.sqrt(np.sum([x**2 for x in foundSpectra])*(np.sum(
                [x**2 for x in b])))
    if np.isnan(val): val = 0
    return val

def replaceAllCommas(string):
    while "," in string:
        string = string.replace(",","_")
    return string

def splitList(l, n):
    n = int(np.ceil(len(l)/float(n)))
    return list([l[i:i + n] for i in range(0, len(l), n)])

def flatten(l):
    if len(l) > 0 and type(l[0]) == type(l):
        return [item for sublist in l for item in sublist]
    else:
        return l



def scoreDeconvolution(originalSpectra, matrix, res, metIDs, treeIDs, masses, centerMz, DDA, massAcc):

    """Goal is to take deconvolved aspects of the spectra"""
    numComponents = len([x for x in range(len(res)) if res[x] > 0 if type(metIDs[x]) != type(tuple())])
    numComponents += len(set([treeIDs[x] for x in range(len(res)) if res[x] > 0 and type(metIDs[x]) == type(tuple)]))
    resScores = [[0,[0 for _ in originalSpectra],[0 for _ in originalSpectra],"original",masses[x]] for x in range(len(res))]
    if len(matrix) > 0:
        solvedSpectraTotal = np.dot(np.transpose(matrix),[[x] for x in res])
        differences =  np.subtract(flatten(originalSpectra),flatten(solvedSpectraTotal))/numComponents
    else:
        solvedSpectraTotal = [0 for _ in originalSpectra]
        differences = flatten(originalSpectra)



    components = []
    uniqueIsotope = {(metIDs[x][0],t):{"spectrum":-1,"indices":[],"mass":-1,"abundance":0} for x,t in zip(range(len(metIDs)),treeIDs) if type(metIDs[x]) == type(tuple())}
    allUniqueIsotope = {(metIDs[x][0],t):{"spectrum":-1,"indices":[],"mass":-1,"abundance":0} for x,t in zip(range(len(metIDs)),treeIDs) if type(metIDs[x]) == type(tuple())}

    componentsMass = []
    #Form components
    componentName = []
    componentAbudance = []
    allComponents = []
    allComponentMass = []
    allComponentName = []
    allComponentAbundance = []

    resSum = np.sum(res)
    if len([x for x in res if x > 0]) > 1:
        for x in range(len(res)):
            if res[x] > 0:
                if (abs(masses[x]-centerMz)/centerMz*1e6 < massAcc):
                    if type(metIDs[x]) != type(tuple()):
                        components.append([max([res[x] * m + d, 0]) for m, d in zip(matrix[x], differences)])
                        componentsMass.append(masses[x])
                        componentName.append(str(metIDs[x]))
                        componentAbudance.append(res[x])
                    else:
                        uniqueIsotope[(metIDs[x][0],treeIDs[x])]["spectrum"] = [res[x] * m for m in matrix[x]]
                        uniqueIsotope[(metIDs[x][0],treeIDs[x])]["mass"] = masses[x]
                        uniqueIsotope[(metIDs[x][0], treeIDs[x])]["indices"].append(x)
                        uniqueIsotope[(metIDs[x][0], treeIDs[x])]["abundance"] += res[x]


                # closestFrag = [[abs(masses[x]-f),f] for f in fragments]
                # closestFrag.sort(key=lambda x: x[0])
                # closestFrag = closestFrag[0][1]
                if type(metIDs[x]) != type(tuple()):
                    allComponents.append([max([res[x] * m + d, 0]) for m, d in zip(matrix[x], differences)])
                    allComponentMass.append(masses[x])
                    allComponentName.append(str(metIDs[x]))
                    allComponentAbundance.append(res[x])
                else:
                    allUniqueIsotope[(metIDs[x][0], treeIDs[x])]["spectrum"] = [res[x] * m for m in matrix[x]]
                    allUniqueIsotope[(metIDs[x][0],treeIDs[x])]["mass"] = masses[x]
                    allUniqueIsotope[(metIDs[x][0], treeIDs[x])]["indices"].append(x)
                    allUniqueIsotope[(metIDs[x][0], treeIDs[x])]["abundance"] += res[x]



        for x in uniqueIsotope:
            if len(uniqueIsotope[x]["indices"]) > 0:
                components.append([max([p+d,0]) for p,d in zip(uniqueIsotope[x]["spectrum"],differences)])
                componentsMass.append(uniqueIsotope[x]["mass"])
                componentName.append(x[0] + " M+1")
                truePercentage = sum([res[i] for i in uniqueIsotope[x]["indices"]])/len(uniqueIsotope[x]["indices"])
                componentAbudance.append(truePercentage)
                for ind in uniqueIsotope[x]["indices"]:
                    matrix[ind] = uniqueIsotope[x]["spectrum"]
                    res[ind] = truePercentage

        for x in allUniqueIsotope:
            if len(allUniqueIsotope[x]["indices"]) > 0:
                allComponents.append([max([p+d,0]) for p,d in zip(allUniqueIsotope[x]["spectrum"],differences)])
                allComponentMass.append(allUniqueIsotope[x]["mass"])
                allComponentName.append(x[0] + " M+1")
                truePercentage = sum([res[i] for i in allUniqueIsotope[x]["indices"]])/len(allUniqueIsotope[x]["indices"])
                allComponentAbundance.append(truePercentage)
                for ind in allUniqueIsotope[x]["indices"]:
                    matrix[ind] = allUniqueIsotope[x]["spectrum"]
                    res[ind] = truePercentage

    components = {(name,m,ab/resSum):s for m,x,s,name,ab in zip(componentsMass,range(len(componentsMass)),components,componentName,componentAbudance)}
    allComponents = {(name,m,ab/resSum):s for m,x,s,name,ab in zip(allComponentMass,range(len(allComponentMass)),allComponents,allComponentName,allComponentAbundance)}


    #components.append(originalSpectra)
    #componentsMass.append(centerMz)
    components[("original",centerMz,0.0)] = originalSpectra
    #components.append([max([d,0.0]) for d in differences])
    #componentsMass.append(centerMz)
    if len([x for x in res if x > 0]) > 1:
        components[("residual",centerMz,0.0)] = [max([d,0.0]) for d in differences]

    allComponents[("original",centerMz,0.0)] = originalSpectra
    #components.append([max([d,0.0]) for d in differences])
    #componentsMass.append(centerMz)
    if len([x for x in res if x > 0]) > 1:
        allComponents[("residual",centerMz,0.0)] = [max([d,0.0]) for d in differences]

    for x in range(len(res)):
        for comp,mz,ab in components:
            if abs(mz-masses[x])/masses[x]*1e6 < massAcc:
                dp = 100*dotProductSpectra(matrix[x],components[(comp,mz,ab)])
                if dp > resScores[x][0]:
                    resScores[x] = [dp,components[(comp,mz,ab)],matrix[x],comp,centerMz]
    return resScores,allComponents

def safeDivide(num,denom):
    if abs(num) < 1e-12 and abs(denom) < 1e-12:
        return 0.0
    elif abs(num) >= 1e-12 and abs(denom) < 1e-12:
        return np.inf
    else:
        return num/denom



def splitList(l, n):
    n = int(np.ceil(len(l)/float(n)))
    return list([l[i:i + n] for i in range(0, len(l), n)])

def createM1SpectrumfromM0(spectra,massIncrease = 1.003,numFrags=5):

    if len(spectra) > 0:
        newSpectra = []
        frags = [f for f in spectra]
        frags.sort(key=lambda x:spectra[x],reverse=True)
        if len(frags) > numFrags:
            frags = frags[:numFrags]
        for frag in frags:
            tempMzs = dict(spectra)
            tempMzs[frag] = 0
            tempMzs[frag+massIncrease] = spectra[frag]
            newSpectra.append(tempMzs)
        sumSpectra = newSpectra[0]
        for spec in newSpectra[1:]:
            for m in spec:
                if m in sumSpectra:
                    sumSpectra[m] += spec[m]
                else:
                    sumSpectra[m] = spec[m]
    else:
        newSpectra = [{}]
        sumSpectra = {}
    return newSpectra, sumSpectra


def cleanIsotopes(result):
    isotopes = set([(x[0][0],x[1],x[2],x[4]) for x in result if type(x[0]) == type(tuple())])
    update = {(key[3],key[0],key[1],key[2],key[4]):val for key,val in result.items() if type(key[0]) != type(tuple())}
    for iso in isotopes:
        scores = []
        comp = 0.0
        for metID,tree,mass,name,c in result:
            if type(metID) == type(tuple()) and metID[0] == iso[0] and iso[1] == tree:
                scores.append(result[(metID,tree,mass,name,c)][0])
                metOfInterest = metID
                treeOfInterest = tree
                massOfInterest = mass
                nameOfInterest = name
                compOfInterest = c
                comp = c
        scores = np.mean(scores)
        update[(str(nameOfInterest[0]) + " (M+1)",iso[0],iso[1],iso[2],comp)] = [scores] + result[(metOfInterest,treeOfInterest,massOfInterest,nameOfInterest,compOfInterest)][1:]
    return update


def collapse1Fold(spec):
    inc = 10
    ind = 0
    newVect = []
    #print(len(spec))
    while ind+inc < len(spec):
        newVect.append(sum(spec[ind:ind+inc]))
        ind += inc
    newVect.append(sum(newVect[ind:]))
    #print(len(newVect))
    return newVect

def clusterSpectraByMzs(mzs,ids,rts,groups,mzTol = 5):

    prelimClusters = {}
    clusterGroups = {}
    for x in range(len(mzs)):
        good = True
        for x2 in prelimClusters:
            if 1e6*abs(x2 - mzs[x])/mzs[x] <= mzTol or groups[x] in clusterGroups[x2]:
                clusterGroups[x2].append(groups[x])
                prelimClusters[x2].append([mzs[x],ids[x]])
                good = False
                break
        if good:
            prelimClusters[mzs[x]] = [[mzs[x],ids[x]]]
            clusterGroups[mzs[x]] = [groups[x]]

    return prelimClusters

def clusterSpectra(samples,peakData):
    groups = list(set([s["group"] for s in samples]))
    clusters = {g:[] for g in groups}
    for s in samples:
        for g in groups:
            if s["group"] == g:
                clusters[g].append(s)
                break
    clustFormatted = []
    for clust in clusters:
        spec = clusters[clust][0]["spectra"]

        if len(clusters[clust]) > 1:
            for spec2 in clusters[clust][1:]:
                spec = mergeSpectrum(spec,spec2["spectra"])
        clustFormatted.append({"group":clust,"spectrum":spec ,"m/z":np.mean([x["center m/z"] for x in clusters[clust]]),"rtWindow":[peakData.at[clust,"rt_start"],peakData.at[clust,"rt_end"]]})



        #def mergeCluster(cluster1,cluster2):
        #     return {"mergedSpectrum": mergeSpectrum(cluster1["mergedSpectrum"],cluster2["mergedSpectrum"]),
        #             "allSpec":cluster1["allSpec"]+cluster2["allSpec"],"ids":cluster1["ids"]+cluster2["ids"],
        #             "mzs": cluster1["mzs"]+cluster2["mzs"],"rts":cluster1["rts"]+cluster2["rts"]}
        #
        # ppmWindow = lambda m: mzTol * 1e-6 * m
        #
        # uniqueMzs = list(set(mzs))
        # absUniqueMzs = []
        # for x in range(len(uniqueMzs)):
        #     win = ppmWindow(uniqueMzs[x])
        #     good = True
        #     for x2 in absUniqueMzs:
        #         if abs(x2 - uniqueMzs[x]) <= win:
        #             good = False
        #             break
        #     if good:
        #         absUniqueMzs.append(np.round(uniqueMzs[x],6))
        #
        #
        # prelimClusters = {mz:[] for mz in absUniqueMzs}
        #
        # for mz in absUniqueMzs:
        #     win = ppmWindow(mz)
        #     toRemove = []
        #     for m,r,o,i in zip(mzs,rts,order,range(len(order))):
        #         if abs(mz-m) <= win:
        #             prelimClusters[mz].append([o,m,r])
        #             toRemove.append(i)
        #
        #     mzs = [mzs[x] for x in range(len(order)) if x not in toRemove]
        #     rts = [rts[x] for x in range(len(order)) if x not in toRemove]
        #     order = [order[x] for x in range(len(order)) if x not in toRemove]
        # totalClusters = []
        # for c in prelimClusters:
        #     tempClust = [{"mergedSpectrum":spectra[id],"allSpec":[spectra[id]],"ids":[id],"mzs":[mz],"rts":[rt]} for id,mz,rt in prelimClusters[c]]
        #     delta = (1-minScores)/numRounds
        #     thresh = 1.0
        #     numSame = 0
        #     #rd.seed(1300)
        #
        #     for r in range(3*numRounds):
        #         if thresh >= minScores:
        #             thresh = thresh - delta
        #         rd.shuffle(tempClust)
        #         numBefore = len(tempClust)
        #         index = 0
        #         for c in deepcopy(tempClust):
        #             index+=1
        #             for cp in range(tempClust.index(c)):
        #                 if dotProductSpectra(c["mergedSpectrum"][0],tempClust[cp]["mergedSpectrum"][0]) >= .5:
        #                     tempClust[cp] = mergeCluster(tempClust[cp],c)
        #                     tempClust.remove(c)
        #                     break
        #
        #             #clusters = [clusters[x] for x in range(len(clusters)) if x not in toRemove]
        #         if len(tempClust) == numBefore and abs(thresh-minScores) < .01:
        #             numSame += 1
        #             if numSame == 2:
        #                 break
        #         else:
        #             numSame = 0
        #     #print(numRounds)
        #     #rd.seed(datetime.now())
        #     totalClusters += tempClust
    return clustFormatted


def mergeSpectrum(consensous,toAdd):
    def getVal(dict,key):
        if key not in dict:
            return 0.0
        else:
            return dict[key]
    keys = set(list(consensous.keys()) + list(toAdd.keys()))
    new = {x:getVal(consensous,x)+getVal(toAdd,x) for x in keys}
    return new

def findMax(mzs,ms1,rtStart,allRts):
    getInt = lambda rt: np.sum([ms1[rt][x] for x in mzs if x in ms1[rt]])
    rInd = allRts.index(rtStart)
    grad = lambda ind,d: (getInt(allRts[ind+d]) - getInt(allRts[ind]))/(allRts[ind+d]-allRts[ind])#,(getInt(allRts[ind]) - getInt(allRts[ind-1]))/(allRts[ind]-allRts[ind-1])])
    while rInd >= len(allRts) -1:
        rInd -= 1
    while rInd <= 1:
        rInd += 1
    pk = grad(rInd,1)
    pkOld = pk
    while(pk * pkOld > 0 and rInd-1 > 1 and rInd+1 < len(allRts)-1):
        pkOld = pk
        if pk > 0:
            rInd += 1
            try:
                pk = grad(rInd,1)
            except:
                print("1",rInd,len(allRts))
        else:
            try:
                rInd -= 1
                pk = grad(rInd,-1)
            except:
                print("-1",rInd,len(allRts))
        #pk = grad(rInd)
        #plt.plot([allRts[rInd],allRts[rInd]],[0,1e7])

    if pk * pkOld <= 0:
        if pkOld > 0:
            rInd -= 1
        else:
            rInd += 1


    return getInt(allRts[rInd]),allRts[rInd]




def extractFeatures(mzs,rts,ids,ms1,mError = 5):
    allRt = list(ms1.keys())
    allRt.sort()
    chromatograms = {}
    allMzList = list()
    for s in ms1:
        allMzList += [x for x in ms1[s] if ms1[s][x] > 0]
    allMzList = np.array(list(set(allMzList)))

    #print("found mzs")
    for id,mz,rt in zip(ids,mzs,rts):
        #plt.figure()
        temp = [[r,abs(r-rt)] for r in allRt]
        temp.sort(key=lambda x: x[1])
        rtRep = temp[0][0]
        mzOI = np.extract(np.abs((10**6)*(allMzList-mz))/mz < mError,allMzList)
        #print("foundmzOI")
        getInt = lambda rt: np.sum([ms1[rt][x] for x in mzOI if x in ms1[rt]])
        maxInt,apex = findMax(mzOI,ms1,rtRep,allRt)
        # maxInt = np.max(list(tempMs1.values()))
        #print("XCR Done")
        r = allRt.index(rtRep)
        tempInts = getInt(allRt[r])
        while(tempInts > .001*maxInt and r > 0 and r < len(allRt)-1):
            r -= 1
            tempInts = getInt(allRt[r])

        rtMin = allRt[r]
        #print("rt min done")
        r = allRt.index(rtRep)
        tempInts = getInt(allRt[r])
        while(tempInts > .001*maxInt and r > 0 and r < len(allRt)-1):
            r += 1
            tempInts = getInt(allRt[r])


        rtMax = allRt[r]
        #print("rtMaxDone")
        chromatograms[id] = [rtMin,rtMax]
        rtMinBound = rtMin-.5*(rtMax-rtMin)
        rtMaxBound = rtMax+.5*(rtMax-rtMin)
        #tempMs1 = [[key,getInt(key)] for key in allRt if key > rtMinBound and key < rtMaxBound]


        # plt.figure()
        # plt.plot([x[0] for x in tempMs1],[x[1] for x in tempMs1])
        # plt.plot([rt,rt],[0,maxInt])
        # plt.plot([rtMin,rtMin],[0,maxInt])
        # plt.plot([rtMax,rtMax],[0,maxInt])
        # plt.plot([apex,apex],[0,maxInt])
        # plt.xlim([rtMinBound,rtMaxBound])

        # plt.figure()
        # plt.plot([allRt[x] for x in range(len(allRt)-1) if allRt[x] > rtMinBound and allRt[x] < rtMaxBound],
        #          [(tempMs1[allRt[x+1]] - tempMs1[allRt[x]])/(allRt[x+1] - allRt[x]) for x in range(len(allRt)) if allRt[x] > rtMinBound and allRt[x] < rtMaxBound])
        # plt.plot([rt, rt], [0, maxInt])
        # plt.plot([rtMin, rtMin], [0, maxInt])
        # plt.plot([rtMax, rtMax], [0, maxInt])
        # plt.xlim([rtMinBound, rtMaxBound])

        #print("plots done")
    #plt.show()
    return chromatograms


def getMatricesForGroup(trees,spectra,possCompounds,possIsotopes,isotope,res,clusters):

    spectrum = dict(spectra[0])
    for spec in spectra[1:]:
        for m,i in spec.items():
            if m in spectrum:
                spectrum[m] += i
            else:
                spectrum[m] = i

    compoundDict = pullMostSimilarSpectra({key:val for key,val in trees.items() if key in possCompounds},spectrum)
    compoundDict = {key: [val[0], collapseAsNeeded(val[1],res)] for key,val in compoundDict.items()}#convertSpectra2Vector(val[0], MAXMASS, res)] for key, val in
                    #compoundDictFull.items()}

    keys = list(compoundDict.keys())

    if isotope:
        isotopeDictFull = pullMostSimilarSpectraIsotopologues({key:val for key,val in trees.items() if key in possIsotopes}, spectrum)

        isotopeDict2 = {}
        for key, val in isotopeDictFull.items():
            isotopeSpectras = val[1]
            for spec, num in zip(isotopeSpectras, range(len(isotopeSpectras))):
                tempKey = ((str(key[0]), num), key[1], key[2] + 1.003, (key[3], num))
                isotopeDict2[tempKey] = [key[1], spec]
        isotopeKeys = list(isotopeDict2.keys())
        isotopeDict = {key: [val[0], collapseAsNeeded(val[1], res)] for key, val in isotopeDict2.items()}


    if type(clusters) != type(None):
        clusterKeys = list(clusters.keys())

    metIDs = [x[0] for x in keys]
    spectraTrees = [x[1] for x in keys]
    masses = [x[2] for x in keys]
    metNames = [x[3] for x in keys]
    spectraIDs = [compoundDict[x][0] for x in keys]
    matrix = [compoundDict[x][1] for x in keys]

    if isotope:
        metIDs += [x[0] for x in isotopeKeys]
        masses += [x[2] for x in isotopeKeys]
        spectraTrees += [x[1] for x in isotopeKeys]
        spectraIDs += [isotopeDict[x][0] for x in isotopeKeys]
        metNames += [x[3] for x in isotopeKeys]
        matrix += [isotopeDict[x][1] for x in isotopeKeys]

    if type(clusters) != type(None):
        metIDs += [str(key[0]) + "|" + str(np.mean(key[2])) for key in clusterKeys]
        masses += [key[0] for key in clusterKeys]
        spectraTrees += [-1 for _ in clusterKeys]
        spectraIDs += [-1 for _ in clusterKeys]
        metNames += [
            "Predicted Analyte: m/z = " + str(np.round(key[0], 5)) + " rt_Range: [" + str(key[1]) + "-" + str(
                key[2]) + "]" for key in clusterKeys]
        matrix += [clusters[key] for key in clusterKeys]

        # convert dicts to lists for deconvolution

    coeffs = []
    for m in metIDs:
        if type(m) != type(tuple()):
            coeffs.append(1.0)
        else:
            coeffs.append(1.0)
            # coeffs.append(len([m1 for m1 in mets if type(m1) == type(tuple()) and m1[0] == m[0]]))
    indexRef = [np.round(x * 10 ** (-1 * res), res) for x in list(range(int(MAXMASS * 10 ** res)))]
    indices = list(set(flatten([list(spectrum.keys())] + [list(m.keys()) for m in matrix])))
    indices.sort()

    indicesAll = [indexRef.index(np.round(x, res)) for x in indices]
    matrix = [[s * c for s in normalizeSpectra([getVal(m, x) for x in indices])] for m, c in
                      zip(matrix, coeffs)]
    reduceSpec = [[getVal(spec, x) for x in indices] for spec in spectra]

    return metIDs, spectraTrees, spectraIDs, matrix, masses, metNames, indicesAll, reduceSpec

def pullMostSimilarSpectraIsotopologues(trees,spectra):
    returnDict = {}
    for tree,ms2Scans in trees.items():
        if len(ms2Scans) > 0:
            generatedIsotopologus = {id:createM1SpectrumfromM0(ms2) for id,ms2 in ms2Scans.items()}
            temp = [[id,ms2[0],dotProductSpectra(spectra,ms2[1])] for id,ms2 in generatedIsotopologus.items()]
            temp.sort(key=lambda x:x[2],reverse=True)
            returnDict[tree] = temp[0][:2]
    return returnDict


def pullMostSimilarSpectra(trees,spectra):
    returnDict = {}
    for tree,ms2Scans in trees.items():
        if len(ms2Scans) > 0:
            temp = [[id,ms2,dotProductSpectra(spectra,ms2)] for id,ms2 in ms2Scans.items()]
            temp.sort(key=lambda x:x[2],reverse=True)
            returnDict[tree] = temp[0][:2]
    return returnDict


# get value from dictionary or return 0 if it is not in the dictionary
def getVal(dict,key):
    if key in dict:
        return dict[key]
    else:
        return 0.0


# determine if m/z is within ppmThresh of an m/z in fragments
def inScan(fragments,candidate_mz,ppmThresh=10):
    if type(fragments) != type(str()):
        try:
            if any(abs(candidate_mz-x)/candidate_mz/(1e-6) < ppmThresh for x in fragments):
                return True
            else:
                return False
        except:
            print(candidate_mz,fragments)
    else:
        return True

def inScanIso(fragments,candidate_mz,ppmThresh=10):
    if type(fragments) != type(str()):
        if any(abs(candidate_mz - x) / candidate_mz / (1e-6) < ppmThresh for x in fragments) and any(abs(candidate_mz-1.003 - x)/(candidate_mz-1.003)/(1e-6) < ppmThresh for x in fragments):
            return True
        else:
            return False
    else:
        return True


#https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before


def readRawDataFile(filename, maxMass, resolution, useMS1, ppmWidth = 50,offset=0.65,tic_cutoff=5):
   try:
        delete = False
        if ".mzML" not in filename:
            toRemove = filename.split("/")[-1]
            command = "msconvert " + filename + " --outdir " + filename.replace(toRemove,"") + ' --filter "peakPicking true 1-" --ignoreUnknownInstrumentError > junk.txt'
            #command = "msconvert " + filename + " --outdir " + filename.replace(toRemove,"") + ' --ignoreUnknownInstrumentError > junk.txt'
            os.system(command)
            filename = filename.replace(".raw", "")
            filename = filename.replace('"', "")
            filename = filename+".mzML"
            delete = True
        reader = mzml.read(filename.replace('"', ""))
        result = []
        ms1Scans = {}
        scanIDCount = 0
        for temp in reader:
            if temp['ms level'] == 2:
                    tic = np.log10(float(temp["total ion current"]))
                    if tic >= tic_cutoff:
                        id = scanIDCount#temp["id"].split()[-1].split("=")[-1]
                        scanIDCount += 1
                        #centerMz = temp["precursorList"]["precursor"][0]["isolationWindow"]['isolation window target m/z']
                        centerMz = temp["precursorList"]["precursor"][0]["selectedIonList"]["selectedIon"][0]["selected ion m/z"]
                        try:
                            lowerBound = centerMz - temp["precursorList"]["precursor"][0]["isolationWindow"]['isolation window lower offset']
                            upperBound = centerMz + temp["precursorList"]["precursor"][0]["isolationWindow"]['isolation window upper offset']
                        except:
                            lowerBound = centerMz - offset
                            upperBound = centerMz + offset
                        #filter = temp["scanList"]["scan"][0]["filter string"]
                        #acquisitionMode = filter.split("@")[0].split()[1]
                        if 'positive scan' in temp:
                            acquisitionMode = "Positive"
                        else:
                            acquisitionMode = "Negative"
                        #settings = filter.split("@")[1].split()[0]
                        #fragmentMode = settings[:3]
                        #NCE = float(settings[3:])
                        rt = temp["scanList"]["scan"][0]["scan start time"]
                        mzs = list(zip(temp["m/z array"],temp["intensity array"]))
                        tempSpecs = []

                        spectra ={np.round(x[0],resolution):0 for x in mzs}
                        for x,y in mzs: spectra[np.round(x,resolution)] += y

                        result.append({"id":id,"spectra":spectra,"mode":acquisitionMode,"center m/z":
                                           centerMz,"lower m/z":lowerBound,"higher m/z":upperBound,"rt":rt,"signal":tic})
            elif useMS1 and temp['ms level'] == 1:
                ms1Scans[temp["scanList"]["scan"][0]["scan start time"]] = {mz: i for mz, i in zip(temp["m/z array"], temp["intensity array"])}
        reader.close()
        if len(ms1Scans) > 0 and useMS1:
            rts = list(ms1Scans.keys())
            rts.sort()
            for samp in range(len(result)):
                isoWidth = result[samp]["center m/z"] - result[samp]["lower m/z"]

                mzScan = ms1Scans[takeClosest(rts,result[samp]["rt"])]

                peaksOfInterest = [[m, i] for m, i in mzScan.items() if m >= result[samp]["center m/z"] - isoWidth - 1.3
                                   and m <= result[samp]["center m/z"] + isoWidth]
                peaksOfInterest.sort(key=lambda x: x[0])
                precursorPeaks = [x for x in peaksOfInterest if
                                  abs(x[0] - result[samp]["center m/z"]) * 1e6 / result[samp]["center m/z"] <= ppmWidth and x[1] > 0]
                chimericPeaks = [x for x in peaksOfInterest if
                                 abs(x[0] - result[samp]["center m/z"]) * 1e6 / result[samp]["center m/z"] > ppmWidth and
                                 x[0] >= result[samp]["center m/z"] - isoWidth and x[1] > 0]
                if len(chimericPeaks) > 0 or len(precursorPeaks) > 0:
                    # result[samp]["percentContamination"] = min([1, max([0, simps([x[1] for x in chimericPeaks],
                    #                                                               [x[0] for x in chimericPeaks],
                    #                                                               even="avg") / (
                    #                                                              simps([x[1] for x in chimericPeaks],
                    #                                                                    [x[0] for x in chimericPeaks],
                    #                                                                    even="avg") + simps(
                    #                                                          [x[1] for x in precursorPeaks],
                    #                                                          [x[0] for x in precursorPeaks],
                    #                                                          even="avg"))]), ])
                    result[samp]["percentContamination"] = np.sum([x[1] for x in chimericPeaks])/(np.sum([x[1] for x in chimericPeaks]) + np.sum([x[1] for x in precursorPeaks]))
                # elif len(chimericPeaks) > 0:
                #     result[samp]["percentContamination"] = 1.0
                else:
                    result[samp]["percentContamination"] = 0.0
                result[samp]["fragments"] = [x[0] for x in peaksOfInterest if x[1] > 1e-6]
                result[samp]["ms1"] = [x for x in peaksOfInterest if x[0] >= result[samp]["center m/z"] - isoWidth]

            if delete:
                #os.remove(filename)
                os.remove("junk.txt")
        return result,ms1Scans

   except:
        print(sys.exc_info())
        print(filename + " does not exist or is ill-formatted")
        return -1,-1


def createDictFromString(string, resolution):
    specDict = {}
    for val in string.split():
        mz = np.round(float(val.split(":")[0]), resolution)
        if mz in specDict:
            specDict[mz] += float(val.split(":")[1])
        else:
            specDict[mz] = float(val.split(":")[1])
    return specDict



class DecoID():
    def __init__(self,libFile,useAuto = False,numCores=1,resolution = 2,label="",api_key="none"):
        self.libFile = libFile
        self.useDBLock = False
        if ".tsv" in libFile:
            try:
                f = open(libFile,"r",encoding = "utf-8")
                data = [x.replace(",","_").rstrip().split("\t") for x in f.readlines()]
                header = data[0]
                data = [{k:replaceAllCommas(val) for k,val in zip(header,x)} for x in data[1:]]
                for x in data:
                    x["m/z"] = float(x["m/z"])
                    x["spectrum"] = createDictFromString(x["spectrum"],resolution)

                posData = {x["id"]:x for x in data if "ositive" in x["mode"]}
                negData = {x["id"]:x for x in data if "egative" in x["mode"]}
                self.library = {"Positive":posData,"Negative":negData}
            except:
                print("bad library file: ", libFile)
                return -1
            self.lib = customDBpy
            self.cachedReq = "none"
            self.ms_ms_library = "custom"
            self.useAuto = useAuto
            pkl.dump(self.library, open(libFile.replace(".tsv", ".db"),"wb"))
            print("Library loaded successfully: " + str(
            len(self.library["Positive"]) + len(self.library["Negative"])) + " spectra found")

        elif ".msp" in libFile:
            try:
                mz = -1
                id = -1
                cpdid = -1
                polarity = -1
                exactMass = -1
                spectrum = {}
                f = open(libFile,"r",encoding="utf-8")
                self.library = {"Positive":{},"Negative":{}}
                first = True
                good = False
                looking = False
                for line in f:
                    line = line.rstrip()
                    if "Name:" in line:
                        if not first:
                            if exactMass != -1 or mz != -1:
                                if polarity != -1:
                                    if mz == -1:
                                        if polarity == "Negative":
                                            mz = exactMass - 1.0073
                                        else:
                                            mz = exactMass + 1.0073
                                    if cpdid == -1:
                                        cpdid = name
                                    if id != -1 and len(spectrum) > 0:
                                        self.library[polarity][id] = {"id":id,"cpdID":cpdid,"name":replaceAllCommas(name),"mode":polarity,"spectrum":spectrum,"m/z":np.round(mz,4)}
                                        good = True


                        else:
                            first = False
                        name = line.split(": ")[1]
                        mz = -1
                        id = -1
                        cpdid = -1
                        polarity = -1
                        spectrum = {}
                        looking = False
                        good = False
                    if "DB#: " in line:
                        id = line.split(": ")[1]
                    if "InChiKey:" in line or "InChIKey" in line:
                        cpdid = line.split(": ")[1]
                    if "Precursor_type:" in line:
                        temp = line.split(": ")[1]
                        if "]+" in temp:
                            polarity = "Positive"
                        elif "]+" in temp:
                            polarity = "Negative"
                    if "ExactMass:" in line:
                        exactMass = float(line.split(": ")[1])
                    if "PrecursorMZ: " in line:
                        mz = float(line.split(": ")[1])
                    if "Ion_mode: " in line:
                        temp = line.split(": ")[1]
                        if temp == "P":
                            polarity = "Positive"
                        elif temp == "N":
                            polarity = "Negative"
                    if looking and len(line.split()) == 2:
                        spectrum[float(line.split()[0])] = float(line.split()[1])
                    if "Num Peaks" in line:
                        looking = True
                print("Library loaded successfully: " + str(len(self.library["Positive"]) + len(self.library["Negative"])) + " spectra found")
                pkl.dump(self.library,open(libFile.replace(".msp",".db"),"wb"))
            except:
               print(sys.exc_info())
               print("bad library file: ", libFile)
               return -1
            self.lib = customDBpy
            self.cachedReq = "none"
            self.ms_ms_library = "custom"
            self.useAuto = useAuto

        elif ".db" in libFile:
            self.lib = customDBpy
            self.cachedReq = "none"
            self.ms_ms_library = "custom"
            self.useAuto = useAuto
            self.library = pkl.load(open(libFile,"rb"))
            print("Library loaded successfully: " + str(
                len(self.library["Positive"]) + len(self.library["Negative"])) + " spectra found")

        else:
            self.useDBLock = True
            self.lib = mzCloudPy
            self.ms_ms_library = "mzCloud"
            self.library = ["reference"]
            self.useAuto = useAuto


            if useAuto:
                self.library.append("autoprocessing")

        self.key = api_key
        self.numCores = numCores
        self.recursive = False
        self.label = label

    @classmethod
    def writeObj(cls,class_instance,filename):
        dill.dump(class_instance, open(filename, "wb"))

    @classmethod
    def fromDill(cls,filename):
        return dill.load(open(filename,"rb"))


    @classmethod
    def from_DecoID(cls, class_instance):
        name = str(uuid.uuid1())
        DecoID.writeObj(class_instance,name)
        obj = DecoID.fromDill(name)
        os.remove(name)
        return obj


    def readData(self,filename,resolution,peaks,DDA,massAcc,offset=.65,peakDefinitions = "",tic_cutoff=0):
        samples, ms1 = readRawDataFile(filename, MAXMASS, resolution, peaks,offset=offset,tic_cutoff=tic_cutoff,ppmWidth=massAcc)
        if samples != -1:
            self.samples = samples
            self.ms1 = ms1
            self.resolution = resolution
            self.peaks = peaks
            self.massAcc = massAcc
            self.DDA = DDA
            if len(self.ms1) < 1:
                self.peaks = False
            if not DDA and not peaks:
                self.DDA = True
            # samples = samples[:100]
            print(len(self.samples), " MS2 spectra detected")
            fileending = "." + filename.split(".")[-1]
            self.filename = filename.replace(fileending, "")
            self.filename = self.filename.replace('"', "")
            self.clusters = {}
            self.data2WriteFinal = []
            self.outputDataFinal = {}

            if peakDefinitions != "":
                self.peakData = pd.read_csv(peakDefinitions)
                self.peakData = self.peakData[["mz","rt_start","rt_end"]]
                dfIndex = list(self.peakData.index.values)

                if self.DDA:
                    i = -1
                    goodSamps = []
                    for samp in samples:
                        i += 1
                        for index in dfIndex:#,row in self.peakData.iterrows():
                            if abs(samp["center m/z"]-self.peakData.at[index,"mz"])/self.peakData.at[index,"mz"]*1e6 < self.massAcc:
                                if samp["rt"] >= self.peakData.at[index,"rt_start"] and samp["rt"] <= self.peakData.at[index,"rt_end"]:
                                    samp["group"] = index
                                    goodSamps.append(i)
                                    break
                    self.samples = [self.samples[x] for x in goodSamps]
                    numGroups = len(set([samp["group"] for samp in self.samples]))
                    print("Number of compounds with acquired MS2: ",numGroups)
                    print("Number of spectra to deconvolve: ",len(self.samples))

                else:
                    samplesDict = {x["id"]: x for x in samples}
                    mzGroups = clusterSpectraByMzs([x["center m/z"] for x in samples], [x["id"] for x in samples],
                                                   [x["rt"] for x in samples],list(range(len(samples))) ,self.massAcc)
                    index = 0
                    for mz in mzGroups:
                        for m, id in mzGroups[mz]:
                            samplesDict[id]["group"] = index
                        index += 1

            else:
                index = 0
                for samp in samples:
                    samp["group"] = index
                    index += 1
                self.peakData = pd.DataFrame.from_dict({i:{"mz":samp["center m/z"],"rt_start":samp["rt"]-.05,"rt_end":samp["rt"]+.05} for i,samp in zip(range(len(samples)),samples)},orient="index")

    def readMS_DIAL_data(self,file,mode,massAcc,peakDataFile):
        self.resolution = 2
        self.peaks = False
        DDA = True
        self.peakData = pd.read_csv(
           peakDataFile)
        self.peakData = self.peakData[["mz", "rt_start", "rt_end"]]
        i = -1
        sampleData = pd.read_csv(file, sep="\t")
        samples = []

        for index, row in sampleData.iterrows():
            id = row["PeakID"]
            if not pd.isna(row["MSMS spectrum"]):
                spectra = row["MSMS spectrum"].split()
                spectra = [x.split(":") for x in spectra]
                spectra = {float(mz): float(i) for mz, i in spectra if float(i) > 0}
                spectra = collapseAsNeeded(spectra, 2)
                centerMz = row["Precursor m/z"]
                upperBound = centerMz + .1
                lowerBound = centerMz - .1
                rt = row["RT (min)"]
                signal = row["Area"]
                samples.append({"id": id, "spectra": spectra, "mode": mode, "center m/z":
                    centerMz, "lower m/z": lowerBound, "higher m/z": upperBound, "rt": rt, "signal": signal})

        self.ms1 = {}
        self.massAcc = massAcc
        self.DDA = DDA

        # samples = samples[:100]
        fileending = "." + file.split(".")[-1]
        self.filename = file.replace(fileending, "")
        self.filename = self.filename.replace('"', "")
        self.clusters = {}
        self.data2WriteFinal = []
        self.outputDataFinal = {}

        goodSamps = []
        for samp in samples:
            i += 1
            for index, row in self.peakData.iterrows():
                if abs(samp["center m/z"] - row["mz"]) / row["mz"] * 1e6 < massAcc and samp["rt"] >= row[
                    "rt_start"] and samp["rt"] <= row["rt_end"]:
                    samp["group"] = index
                    goodSamps.append(i)
                    break
        self.samples = [samples[x] for x in goodSamps]
        print(len(self.samples), " MS2 spectra detected")

    def recursiveRunQ(self,q, data2WriteLater,outputDataFile):
        toQuit = False
        while True:
            if not q.empty():
                new = q.get()

                if new == "EXIT" or toQuit:
                    toQuit = True
                    if q.empty():
                        return 0
                [result, centerMz, id, rt, s2n, indices, numComponents, fragments, decoSpec,components] = new
                if fragments == "none":
                    fragments = [centerMz]
                data2WriteLater.append(list(new))
                outputDataFile[id] = {}
                outputDataFile[id]["decoSpec"] = decoSpec
                outputDataFile[id]["center m/z"] = centerMz
                outputDataFile[id]["rt"] = rt
                outputDataFile[id]["Hits"] = {}
                outputDataFile[id]["index"] = indices
                outputDataFile[id]["fragments"] = fragments
                for x in result:
                    outputDataFile[id]["Hits"][x] = result[x]
            else:
                time.sleep(1)

    def identifyUnknowns(self,resPenalty=100,percentPeaks=0.01,iso=False,ppmThresh = 10,dpThresh = 20):
        try: self.samples
        except: print("datafile not loaded");return -1
        self.iso = iso
        self.percentPeaks = percentPeaks

        self.resPenalty = resPenalty

        q = Queue(maxsize=1000)
        if not self.peaks or not self.DDA:
            print("MS1 and DDA Required for Unknown ID Recursion")
            self.recursive = False
            return -1
        else:
            self.recursive = True
            samplesToGo = []
            samplesLeft = []
            sigThresh = 4
            for x in self.samples:
                if (x["percentContamination"] < .2) and x["signal"] > sigThresh:
                    samplesToGo.append(x)
                else:
                    samplesLeft.append(x)

            data2Write = []
            outputData = {}
            t = Thread(target=self.recursiveRunQ, args=(q,data2Write,outputData))
            t.start()

            self.runSamples(samplesToGo,q)

            t.join()


            unknownGroupIDs = []
            unknownThreshold = dpThresh
            unknownPPMThreshold = ppmThresh
            for result, centerMz, id, rt, s2n, indices, numComponents, fragments, decoSpec,components in data2Write:
                if not any(result[x][0] >= unknownThreshold and ((result[x][4] - x[3]) * (10 ** 6)) / x[
                    3] < unknownPPMThreshold for x in result):
                    unknownGroupIDs.append(id)

            unknownSamples = []
            for id in unknownGroupIDs:
                for samp in samplesToGo:
                    if samp["group"] == id:
                        unknownSamples.append(samp)


            self.clusters = clusterSpectra(unknownSamples,self.peakData)

            print("Number of Predicted Unknown Compounds: ", len(self.clusters))



    def searchSpectra(self,verbose,resPenalty = 100,percentPeaks=0.01,iso=False,threshold = 0.0):
        try: self.samples
        except: print("datafile not loaded");return -1
        q = Queue(maxsize=1000)

        self.iso = iso
        self.percentPeaks = percentPeaks

        self.resPenalty = resPenalty
        if len(self.ms1) < 1:
            self.recursive = False
            self.peaks = False
            # if resPenalty > 10:
            #     self.resPenalty = 10

        if not self.peaks and not self.DDA:
            self.DDA = True


        if type(self.samples) != type(-1):
            self.paramSuffix = ""
            for x in [self.useAuto, self.recursive, self.iso, self.peaks]:
                self.paramSuffix += "_" + str(int(x))
            success = False
            error = True
            while (not success):
                #try:
                    outfile = open(self.filename+ self.label + "_decoID" + ".csv", "w")
                    success = True
                # except:
                #     if error:
                #         print("Error: please close " + self.filename + self.label + "_decoID.csv")
                #         error = False
                #         time.sleep(2)

            outfile.write(
                "#scanID,isolation_center_m/z,rt,compound_m/z,DB_Compound_ID,Compound_Name,DB_Spectrum_ID,dot_product,ppm_Error,Abundance,ComponentID\n")
            t = Thread(target=self.runQ, args=(
            q,outfile,threshold,self.outputDataFinal,self.filename + self.label + ".DecoID",
            self.filename + self.label + "_scanInfo.csv", verbose))
            t.start()

            t2 = Thread(target=self.sendCompleteSamples, args=(self.data2WriteFinal,q))
            t2.start()

            self.runSamples(self.samples,q)


            t.join()
            t2.join()


    def sendCompleteSamples(self, data2Send,q):
        for x in data2Send:
            success = False
            while not success:
                try:
                    q.put(x, timeout=5)
                    success = True
                except:
                    pass

    def runQ(self,q,outfile,threshold, outputDataFile, filename, scanInfoFileName,
             verbose="y"):
        index = 0
        status = 0
        outputScanFile = open(scanInfoFileName, "w")
        outputScanFile.write("#scanID,Signal to Noise Ratio,numComponents,componentID,componentAbundance,componentMz,rt,spectrum\n")
        toQuit = False
        delimiter = ","
        if self.DDA:
            numSamples = len(set([samp["group"] for samp in self.samples]))
        else:
            numSamples = len(self.peakData)

        indexRef = [np.round(x * 10 ** (-1 * self.resolution), self.resolution) for x in list(range(int(MAXMASS * 10 ** self.resolution)))]

        while True:
            if not q.empty():
                new = q.get()
                if new == "EXIT" or toQuit:
                    toQuit = True
                    if q.empty():
                        outfile.close()
                        if filename != "None":
                            fh = gzip.open(filename, "wb")
                            pkl.dump([self.samples,self.peakData,self.ms1,outputDataFile], fh)
                            fh.close()
                        outputScanFile.close()
                        break
                elif new != "EXIT":
                    [result, centerMz, id, rt, s2n, indices, numComponents, fragments, decoSpec,components] = new

                    if fragments == "none":
                        fragments = [centerMz]

                    for c in components:
                        outputScanFile.write(str(id) + "," + str(s2n) + "," + str(numComponents) + "," + str(c[0]) + "," +str(c[2]) + "," + str(c[1]) + "," + str(rt) + ",")
                        for ind,i in zip(indices,components[c]):
                            if i > 0:
                                outputScanFile.write(str(indexRef[ind]) + ":" + str(i) + " ")
                        outputScanFile.write("\n")
                    update = False
                    if id not in outputDataFile:
                        outputDataFile[id] = {}
                        outputDataFile[id]["decoSpec"] = decoSpec
                        outputDataFile[id]["center m/z"] = centerMz
                        outputDataFile[id]["rt"] = rt
                        outputDataFile[id]["Hits"] = {}
                        outputDataFile[id]["index"] = indices
                        outputDataFile[id]["fragments"] = fragments
                        outputDataFile[id]["components"] = components
                        update = True
                    for x in result:
                        if result[x][0] > threshold:

                            try:
                                tempMz = result[x][4]
                            except:
                                print(result[x])
                                break
                            componentName = result[x][3]
                            outfile.write(str(id) + "," + str(tempMz))

                            try:
                                [outfile.write(delimiter + z) for z in
                                 [str(rt), str(x[3]), str(x[1]), x[0], str(x[2]), str(result[x][0]),
                                  str((x[3] - tempMz) * 1e6 / tempMz), str(x[4]),str(componentName)]]
                            except:
                                [outfile.write(delimiter + z) for z in
                                 [str(x[1]), str(x[2]), str(result[x][0]),
                                  str((x[3] - tempMz) * 10 ** 6 / tempMz), str(x[4]),str(componentName)]]
                            outfile.write("\n")
                            if filename != "None" and update:
                                outputDataFile[id]["Hits"][x] = result[x]
                index += 1
                if type(verbose) == type(str()):
                    if status == 0:
                        print("0................................................100")
                    if numSamples == 0:
                        for _ in range(50):
                            if "yV" in verbose:
                                print("x", flush=True)
                            else:
                                print("x", end="", flush=True)
                    else:
                        while index / numSamples > status:
                            if "yV" in verbose:
                                print("x", flush=True)
                            else:
                                print("x", end="", flush=True)
                            status += .02
                else:
                    if numSamples == 0:
                        for _ in range(50):
                            verbose.put("1")
                    else:
                        while index / numSamples > status:
                            status += 0.02
                            verbose.put("1")

            else:
                time.sleep(1)

    def prepareForCluster(self,numberOfFiles):
        # if self.recursive:
        #     tempObject = DecoID.from_DecoID(self)
        #     tempObject.filename+="_unknowns_"
        #     tempObject.samples = []
        #     DecoID.writeObj(tempObject,tempObject.filename+".dill")
        groups = list(set([x["group"] for x in self.samples]))
        numGroupsPerFile = int(len(groups)/numberOfFiles)
        self.data2WriteFinal = []
        self.outputDataFinal = {}
        groupBegin = 0
        processes = []
        groupEnd = groupBegin + numGroupsPerFile
        for num in range(numberOfFiles):
            tempObject = DecoID.from_DecoID(self)
            tempObject.filename += "_" + str(num) + "_"
            if num != numberOfFiles - 1:
                group = groups[groupBegin:groupEnd]
            else:
                group = groups[groupBegin:]
            groupBegin = groupEnd
            groupEnd = groupBegin + numGroupsPerFile
            tempObject.samples = [samp for samp in tempObject.samples if samp["group"] in group]
            DecoID.writeObj(tempObject,tempObject.filename+".dill")

    @staticmethod
    def combineResults(filenames,newFilename,endings = ["_scanInfo.csv","_decoID.csv",".DecoID"]):
        goodFiles = []
        for file in filenames:
            try:
                open(file+"_decoID.csv","r")
                goodFiles.append(file)
            except:
                pass
        if len(goodFiles) > 0:
            for end in endings:
                if ".csv" in end:
                    base = open(goodFiles[0]+end,"r").readlines()
                    if len(goodFiles) > 1:
                        for f in goodFiles[1:]:
                            base += open(f+end,"r").readlines()[1:]
                        outfile = open(newFilename+end,"w")
                        [outfile.write(x) for x in base]
                        outfile.close()
                # else:
                #     print(end)
                #     fh = gzip.open(goodFiles[0]+end, "rb")
                #     [samples,ms1,peakData,baseDict] = pkl.load(fh)
                #     fh.close()
                #     if len(goodFiles) > 1:
                #         for f in goodFiles[1:]:
                #             fh = gzip.open(f + end, "rb")
                #             [samp,_,_,tempDict] = pkl.load(fh)
                #             baseDict.update(tempDict)
                #             samples += samp
                #             fh.close()
                #     fh = gzip.open(newFilename+end,"wb")
                #     pkl.dump([samples,ms1,peakData,baseDict],fh)
        else:
            print("no files detected")
    def runSamples(self,samples,q,numConcurrentMzGroups=20):

        numProcesses = Value('i', 0)
        lock = Lock()
        processes = []
        dbLock = Lock()
        availableToGrab = Value('i',1)
        samplesDict = {x["id"]:i for x,i in zip(samples,range(len(samples)))}
        keys = list(samplesDict.keys())
        mzGroups  = clusterSpectraByMzs([samples[samplesDict[k]]["center m/z"] for k in keys],[samples[samplesDict[k]]["id"] for k in keys],[samples[samplesDict[k]]["rt"] for k in keys],[samples[samplesDict[k]]["group"] for k in keys],self.massAcc)
        mzGroupsWSamples = {x:{"samples":[]} for x in mzGroups}
        for mz in mzGroups:
            for m,id in mzGroups[mz]:
                mzGroupsWSamples[mz]["samples"].append(samples[samplesDict[id]])

        for mz in mzGroupsWSamples:
            mzGroupsWSamples[mz]["lower m/z"] = np.min([x["lower m/z"] for x in mzGroupsWSamples[mz]["samples"]])
            mzGroupsWSamples[mz]["higher m/z"] = np.max([x["higher m/z"] for x in mzGroupsWSamples[mz]["samples"]])
            if type(self.clusters) != type(None):
                toAdd = [c for c in self.clusters if
                         c["m/z"] >= mzGroupsWSamples[mz]["lower m/z"] and c["m/z"] <= mzGroupsWSamples[mz]["higher m/z"]]
                toAdd = {(c["m/z"], c["rtWindow"][0], c["rtWindow"][1]): c["spectrum"] for
                         c in toAdd}
            else:
                toAdd = self.clusters

            #self.processMzGroup(mzGroupsWSamples[mz]["samples"], toAdd, numProcesses, mzGroupsWSamples[mz]["higher m/z"],
            #    mzGroupsWSamples[mz]["lower m/z"], availableToGrab, lock, q)
            p = Thread(target=self.processMzGroup,args=(mzGroupsWSamples[mz]["samples"],toAdd,numProcesses,mzGroupsWSamples[mz]["higher m/z"],mzGroupsWSamples[mz]["lower m/z"],availableToGrab,lock,q,dbLock))
            while len(processes) >= numConcurrentMzGroups:
                processes = [proc for proc in processes if proc.is_alive()]
                time.sleep(1)
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

        q.put("EXIT")


    def processMzGroup(self,allSamples, clusters, numProcesses, upperBound, lowerBound, availableToGrab,lock,q,dbLock):

        def startProc(numP, l,samples,trees,possCompounds,possIsotopes):
            spectra = [samp["spectra"] for samp in samples]
            toAdd = {key: value for key, value in clusters.items() if
                     any(key[1] < samp["rt"] and key[2] > samp["rt"] for samp in samples)}
            p = Process(target=DecoID.processGroup,
                        args=(
                            samples,group,trees, spectra, possCompounds, possIsotopes, self.iso,self.DDA,self.massAcc,self.peaks,q,self.resPenalty,self.resolution,toAdd,self.peakData,lowerBound,upperBound))
            #t = Thread(target=startProc, args=(p, numProcesses, lock))
            while not checkRoom(numProcesses, lock):
                time.sleep(1)
            p.start()
            p.join()
            with l:
                numP.value -= 1
            return 0

        def checkRoom(val, l):
            with l:
                if val.value < self.numCores:
                    #print(val.value,self.numCores)
                    val.value += 1
                    return True
                else:
                    return False

        mode = allSamples[0]["mode"]
        if self.useDBLock:
            with dbLock:
                trees, possCompounds, possIsotopes = self.lib.getCanidateCompoundTrees(mode, upperBound, lowerBound, self.iso,
                                                                          self.library,self.key)
        else:
            trees, possCompounds, possIsotopes = self.lib.getCanidateCompoundTrees(mode, upperBound, lowerBound,
                                                                                   self.iso,
                                                                                   self.library, self.key,)
        featureGroups = {x["group"]:[] for x in allSamples}
        [featureGroups[x["group"]].append(x) for x in allSamples]



        threads = []
        for group,samples in featureGroups.items():
            t = Thread(target=startProc,args=(numProcesses,lock,samples,trees,possCompounds,possIsotopes))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    @staticmethod
    def processGroup(samples,group,trees, spectra, possCompounds, possIsotopes, iso,DDA,massAcc,peaks,q,resPenalty,resolution,toAdd,peakData,lowerbound,upperbound):

        [metIDs, spectraTrees, spectraIDs, matrix, masses, metNames, indicesAll,
         reduceSpec] = getMatricesForGroup(trees, spectra, possCompounds, possIsotopes, iso,
                                           # make get matrices for group independent of library source
                                           resolution, toAdd)
        isoIndices = [x for x in range(len(metIDs)) if type(metIDs[x]) == type(tuple())]

        results = []
        samples2Go = list(samples)
        reduceSpec2Go = list(reduceSpec)

        for sample, spectrum in zip(samples2Go, reduceSpec2Go):
            results.append(DecoID.processSample(sample, spectrum, masses, matrix, massAcc, peaks,resPenalty,isoIndices))

        if DDA:
            combinedSpectrum = np.sum(reduceSpec, axis=0)
            resVector = np.sum([x[0] for x in results], axis=0)
            centerMz = np.mean([s["center m/z"] for s in samples])
            rt = np.mean([s["rt"] for s in samples])
            foundSpectra = np.sum([x[2] for x in results], axis=0)
            numComponents = len([i for i in resVector if i > 1e-8])
            s2n = (1.0 / max([1, numComponents])) * np.sum(flatten(foundSpectra)) / np.sum(
                np.abs(np.subtract(foundSpectra, combinedSpectrum)))
            if peaks:
                frags = flatten([s["fragments"] for s in samples])
            else:
                frags = []

            scores, components = scoreDeconvolution(combinedSpectrum, matrix, resVector, metIDs, spectraTrees,
                                                    masses, centerMz, DDA, massAcc)

            result = {(met, specID, mass, name, safeDivide(comp, sum(resVector))): coeff for
                      met, name, specID, coeff, mass, comp in
                      zip(metIDs, metNames, spectraIDs, scores, masses, resVector)}

            # combine isotopes together
            result = cleanIsotopes(result)

            # output result
            success = False
            while not success:
                try:
                    q.put([result, centerMz, group, rt, s2n, indicesAll, len(components), frags, foundSpectra, components],
                          timeout=5)
                    success = True
                except:
                    print("waiting to put in q")
                    pass
        else:
            rts = [samp["rt"] for samp in samples]
            for index,row in peakData.iterrows():
                if row["mz"] >= lowerbound and row["mz"] <= upperbound:
                    goodIndices = [x for x in range(len(rts)) if rts[x] >= row["rt_start"] and rts[x] <= row["rt_end"]]
                    if len(goodIndices) > 0:
                        combinedSpectrum = np.sum([reduceSpec[x] for x in goodIndices], axis=0)
                        resVector = np.sum([results[x][0] for x in goodIndices], axis=0)
                        centerMz = row["mz"]
                        rt = np.mean([row["rt_start"], row["rt_end"]])
                        foundSpectra = np.sum([results[x][2] for x in goodIndices], axis=0)
                        numComponents = len([i for i in resVector if i > 1e-8])
                        s2n = (1.0 / max([1, numComponents])) * np.sum(flatten(foundSpectra)) / np.sum(
                            np.abs(np.subtract(foundSpectra, combinedSpectrum)))
                        if peaks:
                            frags = flatten([s["fragments"] for s in samples])
                        else:
                            frags = []

                        scores, components = scoreDeconvolution(combinedSpectrum, matrix, resVector, metIDs, spectraTrees,
                                                                masses, centerMz, DDA, massAcc)

                        result = {(met, specID, mass, name, safeDivide(comp, sum(resVector))): coeff for
                                  met, name, specID, coeff, mass, comp in
                                  zip(metIDs, metNames, spectraIDs, scores, masses, resVector)}

                        # combine isotopes together
                        result = cleanIsotopes(result)

                        # output result
                        success = False
                        while not success:
                            try:
                                q.put([result, centerMz, index, rt, s2n, indicesAll, len(components), frags, foundSpectra,
                                       components],
                                      timeout=5)
                                success = True
                            except:
                                print("waiting to put in q")
                                pass

            #get peaks in window
            #parse out by retention time where peaks occur
            #repeat the above with the targeted m/z
            #no peaks => no results

    @staticmethod
    def processSample(sample,spectrum,masses,matrix,massAcc,peaks,resPenalty,isoIndices):

        centerMz = sample["center m/z"]
        lowerBound = sample["lower m/z"]  # lowest m/z in isolation window
        upperBound = sample["higher m/z"]  # highest

        def checkScan(mass,index):
            if index in isoIndices:
                return inScanIso(sample["fragments"],mass,massAcc)
            else:
                return inScan(sample["fragments"],mass,massAcc)

        if len(matrix) > 0:
            goodIndices = [x for x in range(len(masses)) if masses[x] < upperBound and masses[x] > lowerBound and ((not peaks) or checkScan(masses[x],x))]
            if len(goodIndices) > 0:
                resTemp, s2n = solveSystem([matrix[x] for x in goodIndices], spectrum,resPenalty)  # deconvolution
                res = [0.0 for _ in masses]
                for x in range(len(goodIndices)):
                    res[goodIndices[x]] = resTemp[x]
                decoSpec = flatten(np.dot(np.transpose(matrix), [[x] for x in res]).tolist())
            else:
                res = [0.0 for _ in masses]
                s2n = 0.0
                decoSpec = [0 for _ in spectrum]
            #q.put([res,s2n,decoSpec])
            return [res,s2n,decoSpec]
        else:
            #q.put([[],0,[0 for _ in spectrum]])
            return [[],0,[0 for _ in spectrum]]


            # score the components found in the deconvolution

        #    numComponents = len([x for x in res if x > 0])

        #
        #     scores,components = metaboliteSensitivity(spectra[-1], matrices[-1], res, metIDs[-1], spectraTrees[-1],masses[-1],centerMz,DDA,massAcc,fragments)
        #
        #     result = {(met, specID, mass, name, safeDivide(comp, sum(res))): coeff for
        #               met, name, specID, coeff, mass, comp in
        #               zip(metIDs[-1], metNames[-1], spectraIDs[-1], scores, masses[-1], res)}
        #
        #     # combine isotopes together
        #     result = cleanIsotopes(result)
        #
        #     # output result
        #     success = False
        #     while not success:
        #         try:
        #             q.put([result, centerMz, id, rt, s2n, indices[-1], numComponents, fragments, decoSpec,components ], timeout=5)
        #             success = True
        #         except:
        #             pass
        # else:
        #     q.put([[], centerMz, id, rt, 0, [], 0, [], [0 for _ in spectra[0]],{}])


    @staticmethod
    def toSiriusOutput(filename,polarity,spectype="o",ppmErr=10):
        data = pd.read_csv(filename)
        dir = filename.replace("_scanInfo.csv","_sirius/")
        os.mkdir(dir)
        if spectype == "o":
            key = "original"
            data = data[data["componentID"] == key]
        scanIDs = list(set(data["#scanID"].values))
        for scanID in scanIDs:
            relevant = data[data["#scanID"] == scanID]
            targetMz = relevant[relevant["componentID"] == "original"]
            targetMz = targetMz.at[targetMz.index.values[0],"componentMz"]
            for index,row in relevant.iterrows():
                if 1e6*abs(row["componentMz"] - targetMz)/targetMz < ppmErr:
                    spec = row["spectrum"]
                    id  = row["componentID"].replace("|","-")
                    id = id.replace("/","-")
                    outfile = open(dir+str(scanID) + "_" + str(id) + ".ms","w")
                    outfile.write(">compound " + str(scanID) + "_" + str(id))
                    outfile.write("\n>parentmass " + str(row["componentMz"]))
                    outfile.write("\n>charge " + str(polarity))
                    outfile.write("\n>ms1\n")
                    outfile.write(str(row["componentMz"]) + " 100")
                    outfile.write("\n\n\n>ms2")
                    for pair in spec.split():
                        mz = pair.split(":")[0]
                        i = pair.split(":")[1]
                        outfile.write("\n" + mz + " " + i)
                    outfile.close()


import grequests
import json
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
    MZCOMPOUNDTREELINK = {"reference": pkl.load(
        open(os.path.join(application_path, "mzCloudCompound2TreeLinkagereference.pkl"), "rb")),
        "autoprocessing": pkl.load(open(os.path.join(application_path,
                                                     "mzCloudCompound2TreeLinkageautoprocessing.pkl"),
                                        "rb"))}
elif __file__:

    application_path = os.path.dirname(__file__)
    MZCOMPOUNDTREELINK = {"reference": pkl.load(
        open(os.path.join(application_path, "mzCloudCompound2TreeLinkagereference.pkl"), "rb")),
        "autoprocessing": pkl.load(open(os.path.join(application_path,
                                                     "mzCloudCompound2TreeLinkageautoprocessing.pkl"),
                                        "rb"))}

timeout = 30
CONCURRENTREQUESTMAX = 1
MAXMASS = 5000

class customDBpy():
    def __init__(self):
        pass
    @staticmethod
    def getCanidateCompoundTrees(mode, upperBound, lowerBound, isotope=False, library="none", key="none",
                                 resolution=2):

        possCompounds = set()
        possIsotopes = set()

        # get compounds in isolation window
        possCompoundsTemp = {
            (library[mode][x]["cpdID"], library[mode][x]["cpdID"], library[mode][x]["name"], library[mode][x]["id"], x):
                library[mode][x]["m/z"] for x in
            library[mode] if library[mode][x]["m/z"] >= lowerBound and library[mode][x]["m/z"] <= upperBound}
        possCompoundsTemp = [(str(x[0]), x[1], possCompoundsTemp[x], x[2], x[3], x[4]) for x in possCompoundsTemp]

        possCompounds = possCompounds.union({tuple(x) for x in possCompoundsTemp})

        # get isotopes if necessary
        if isotope:
            possIsotopesTemp = {(library[mode][x]["cpdID"], library[mode][x]["cpdID"], library[mode][x]["name"],
                                 library[mode][x]["id"], x): library[mode][x]["m/z"] for x in
                                library[mode] if library[mode][x]["m/z"] >= lowerBound - 1.00335 and library[mode][x][
                                    "m/z"] <= lowerBound}
            possIsotopesTemp = [(str(x[0]), x[1], possIsotopesTemp[x], x[2], x[3], x[4]) for x in possIsotopesTemp]
            possIsotopes = possIsotopes.union({tuple(x) for x in possIsotopesTemp})

        trees = {x[:-1]: library[mode][x[-1]]["spectrum"] for x in possIsotopes.union(possCompounds)}
        uniqueCPDs = list(set([tuple(x[:-1]) for x in trees]))
        trees2 = {c: {} for c in uniqueCPDs}
        for x in trees:
            trees2[tuple(x[:-1])][x[-1]] = trees[x]
        possCompounds = {key[:-2] for key in possCompounds}
        possIsotopes = {key[:-2] for key in possIsotopes}
        return trees2, possCompounds, possIsotopes

class Keys():
    def __init__(self,api_code):
        self.HEADER = {
            'V1-API-Secret': api_code,
            'cache-control': "no-cache",
            }
    SPECTRAURL = "https://mzcloud.org/api/v1/LIBRARY/trees/TREENUMBER/spectra"
    COMPOUNDURL = "https://mzcloud.org/api/v1/LIBRARY/compounds"

class mzCloudPy():
    def __init__(self):
        pass
    @staticmethod
    def getCanidateCompoundTrees(mode, upperBound, lowerBound, isotope=False, library=["reference"], key="none"):

        keys = Keys(key)
        # make list of isolation window range
        centerMz = [lowerBound, upperBound]
        centerMz[0] = int(np.floor(centerMz[0]))
        centerMz[1] = int(np.ceil(centerMz[1]))
        possCompoundsTrueAll = set()
        possIsotopesTrueAll = set()
        possCompounds = set()
        possIsotopes = set()
        for lib in library:
            # get compounds in isolation window
            possCompoundsTemp = {tuple(x[:2]) + (x[3],): x[2] for x in
                                 flatten([MZCOMPOUNDTREELINK[lib][mode][x] for x in
                                          range(centerMz[0] - 1, centerMz[1] + 1)])}
            possCompoundsTemp = [(lib[0] + str(x[0]), x[1], possCompoundsTemp[x], x[2]) for x in possCompoundsTemp if
                                 possCompoundsTemp[x] >= lowerBound and possCompoundsTemp[x] <= upperBound]

            possCompounds = possCompounds.union({tuple(x) for x in possCompoundsTemp})

            # get isotopes if necessary
            if isotope:
                possIsotopesTemp = {tuple(x[:2]) + (x[3],): x[2] for x in flatten(
                    [MZCOMPOUNDTREELINK[lib][mode][x] for x in range(centerMz[0] - 1, centerMz[1])])}
                possIsotopesTemp = [(lib[0] + str(x[0]), x[1], possIsotopesTemp[x], x[2]) for x in possIsotopesTemp if
                                    possIsotopesTemp[x] >= lowerBound - 1.00335 and possIsotopesTemp[x] <= lowerBound]

                possIsotopes = possIsotopes.union({tuple(x) for x in
                                                   possIsotopesTemp})  # if x[2] >= centerMzOrig - isolationWidth - 1 and x[2] <= centerMzOrig - isolationWidth}

        trees = mzCloudPy.getTreesAsync(possIsotopes.union(possCompounds),keys)

        return trees, possCompounds, possIsotopes

    """
    take spectra from m/z cloud after being read in by json and convert to dictionary
    """
    @staticmethod
    def convertSpectra2Vector(spectra, maxMass, resolution):
        mzs = {np.round(x["MZ"], resolution): x["Abundance"] for x in spectra["Peaks"]}
        return mzs
    @staticmethod
    def getTreesAsync(trees,keys, calibration="recalibrated", maxRetries=3, cache="none", maxMass=MAXMASS, resolution=2):
        libraryDict = {"a": "autoprocessing", "r": "reference"}
        requestTuple = []
        keyList = []
        alreadyCached = {}
        toCache = []
        for tree in trees:
            url = keys.SPECTRAURL.replace("TREENUMBER", str(tree[1]))
            library = libraryDict[tree[0][0]]
            url = url.replace("LIBRARY", library)
            querystring = {"stage": "2", "processing": calibration, "peaks": "true"}
            payload = ""
            if type(cache) != type("") and (library, tree) in cache:
                alreadyCached[tree] = cache[(library, tree)]
            else:
                toCache.append([library, tree])
                keyList.append(tree)
                requestTuple.append(
                    grequests.get(url, data=payload, headers=keys.HEADER, params=querystring, timeout=timeout))
        requestTuple = tuple(requestTuple)
        responses = grequests.map(requestTuple, size=CONCURRENTREQUESTMAX)
        errors = [key for key in range(len(keyList)) if
                  type(responses[key]) == type(None) or "An error has occurred" in responses[
                      key].text or "Service Unavailable" in responses[key].text]
        numTries = 1
        while (len(errors) > 0) and maxRetries > numTries:
            requestTuple = []
            # print("error", len(errors),len(trees))
            for tree in errors:
                url = keys.SPECTRAURL.replace("TREENUMBER", str(keyList[tree][1]))
                url = url.replace("LIBRARY", library)
                querystring = {"stage": "2", "processing": calibration, "peaks": "true"}
                payload = ""
                requestTuple.append(
                    grequests.get(url, data=payload, headers=keys.HEADER, params=querystring, timeout=timeout))
            requestTuple = tuple(requestTuple)
            responsesNew = grequests.map(requestTuple, size=CONCURRENTREQUESTMAX)
            for response, tree in zip(responsesNew, errors):
                responses[tree] = response
            errors = [key for key in range(len(keyList)) if
                      type(responses[key]) == type(None) or "An error has occurred" in responses[
                          key].text or "Service Unavailable" in responses[key].text]
            numTries += 1
        if numTries >= maxRetries:
            print("Number of retries exceeded to contact m/zCloud. Check network")
        responses = [responses[x] for x in range(len(responses)) if x not in errors]
        keyList = [keyList[x] for x in range(len(keyList)) if x not in errors]
        output = {key: mzCloudPy.getAllSpectraInTree(mzCloudPy.reformatSpectraDictList(json.loads(val.text)), maxMass, resolution) for
                  key, val in zip(keyList, responses)}

        return output
    @staticmethod
    def reformatSpectraDictList(dictList):
        dat = {x["Id"]: {key: val for key, val in x.items() if key != "Id"} for x in dictList}
        return dat
    @staticmethod
    def getAllSpectraInTree(dat, maxMass, resolution):
        return {id: mzCloudPy.convertSpectra2Vector(dat[id], maxMass, resolution) for id in dat}
    @staticmethod
    def getCompoundList(page, pageSize=100, library="reference"):
        url = keys.COMPOUNDURL
        url = url.replace("LIBRARY", library)
        querystring = {"page": str(page), "pageSize": str(pageSize), "newer": "2000-09-03"}
        payload = ""

        response = 1
        while (response == 1):
            try:
                response = (grequests.get(url, data=payload, headers=keys.HEADERSCOMP, params=querystring, timeout=timeout),)
                response = grequests.map(response)[0]
                if type(response) == type(
                        None) or "An error has occurred" in response.text or "Service Unavailable" in response.text:
                    response = 1
                else:
                    dat = mzCloudPy.reformatSpectraDictList(json.loads(response.text)["Items"])
            except:
                pass
        return dat
    @staticmethod
    def getListofSpectrainTree(trees,keys, calibration="recalibrated", library="reference"):
        response = 1
        requestTuple = []
        treeOrder = list(trees)
        for tree in trees:
            url = keys.SPECTRAURL.replace("TREENUMBER", str(tree[0]))
            url = url.replace("LIBRARY", library)
            querystring = {"stage": "2", "processing": calibration, "peaks": "true"}
            payload = ""
            requestTuple.append(grequests.get(url, data=payload, headers=keys.HEADER, params=querystring, timeout=40))
        requestTuple = tuple(requestTuple)
        responses = grequests.map(requestTuple)

        errors = [key for key in range(len(responses)) if
                  type(responses[key]) == type(None) or "An error has occurred" in responses[key].text]
        while (len(errors) > 0):
            requestTuple = []
            for tree in [treeOrder[x] for x in errors]:
                url = keys.SPECTRAURL.replace("TREENUMBER", str(tree[0]))
                url = url.replace("LIBRARY", library)
                querystring = {"stage": "2", "processing": calibration, "peaks": "true"}
                payload = ""
                requestTuple.append(
                    grequests.get(url, data=payload, headers=keys.HEADER, params=querystring, timeout=40))
            requestTuple = tuple(requestTuple)
            responsesNew = grequests.map(requestTuple)
            for error, res in zip(errors, responsesNew):
                responses[error] = res

            errors = [key for key in range(len(responses)) if
                      type(responses[key]) == type(None) or "An error has occurred" in responses[
                          key].text or "Service Unavailable" in responses[key].text or "unavailable" in responses[
                          key].text]

        output = {tree: mzCloudPy.reformatSpectraDictList(json.loads(response.text)) for response, tree in
                  zip(responses, treeOrder)}
        return output
    @staticmethod
    def generateCompoundID2SpectralIDIndexedByM_ZStrict(numPerPage=100, key="none",library="reference"):
        # get number of items
        keys = Keys(key)
        totalCompounds = json.loads(grequests.map((grequests.get(keys.COMPOUNDURL.replace("LIBRARY", library), data="",
                                                                 headers=keys.HEADER, params={"page": str(1),
                                                                                              "pageSize": "5",
                                                                                              "newer": "2000-09-03"}),))[
                                        0].text)["Total"]
        numPages = int(np.ceil(float(totalCompounds) / numPerPage))
        pos = [[] for _ in range(5000)]
        neg = [[] for _ in range(5000)]
        linkage = {"Positive": pos, "Negative": neg}
        for page in range(1, numPages + 1):
            compounds = mzCloudPy.getCompoundList(page, numPerPage, library=library)
            # print(compounds)
            treeDict = {}
            for comp in compounds:
                treeDict.update({(key, comp, compounds[comp]["SearchCompoundName"]): val for key, val in
                                 mzCloudPy.reformatSpectraDictList(compounds[comp]["SpectralTrees"]).items()})

            allSpectra = mzCloudPy.getListofSpectrainTree(list(treeDict.keys()),keys)

            for tree in treeDict:
                posValsRounded = []
                posValsTrue = []
                spectras = allSpectra[tree]
                for spectra in spectras:
                    rounded = int(np.floor(spectras[spectra]["IsolationWidth"]["XPos"]))
                    posValsRounded.append(rounded)
                    posValsTrue.append(np.round(spectras[spectra]["IsolationWidth"]["XPos"], 7))
                try:
                    [linkage[treeDict[tree]["Polarity"]][x].append((tree[1], tree[0], y, tree[2])) for x, y in
                     zip(posValsRounded, posValsTrue)]
                except:
                    print(tree, posValsRounded)
            print(float(page) * numPerPage / totalCompounds)
        pkl.dump(linkage, open("mzCloudCompound2TreeLinkage" + library + ".pkl", "wb"), pkl.HIGHEST_PROTOCOL)







