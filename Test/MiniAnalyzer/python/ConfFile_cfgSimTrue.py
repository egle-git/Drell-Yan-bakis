import FWCore.ParameterSet.Config as cms

def read_filelist(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

filelist = read_filelist("rootfilessimone.txt") #rootfilessimone.txt or rootfilessimtwo.txt

process = cms.Process("Test")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(filelist)
)


process.hltHighLevel = cms.EDFilter("HLTHighLevel",
   TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
   HLTPaths = cms.vstring('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ*'),
   eventSetupPathsKey = cms.string(''),
   andOr = cms.bool(True),
   throw = cms.bool(True)
)

process.demo = cms.EDAnalyzer('MiniAnalyzerSimTrue',
                              particles = cms.InputTag("genParticles"),
                              xsec = cms.double(6422), #6422 for first, 20480 for second
                              lumi = cms.double(6658),
                              GenEventInfo = cms.untracked.InputTag("generator")
)


process.p = cms.Path(process.hltHighLevel+process.demo)
