import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.parseArguments()
process = cms.Process('XSec')

def read_filelist(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

filelist = read_filelist(options.inputFiles[0])

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",
    fileNames = cms.untracked.vstring(filelist), 
    secondaryFileNames = secFiles)
process.xsec = cms.EDAnalyzer("GenXSecAnalyzer")

process.ana = cms.Path(process.xsec)
process.schedule = cms.Schedule(process.ana)
