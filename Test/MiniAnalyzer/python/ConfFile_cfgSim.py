import FWCore.ParameterSet.Config as cms
#import FWCore.PythonUtilities.LumiList as LumiList
#goodJSON = 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
#myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',')

def read_filelist(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

filelist = read_filelist("rootfilessimtwo.txt") #rootfilessimone.txt or rootfilessimtwo.txt

process = cms.Process("Test")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(filelist)
)

# process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
# process.source.lumisToProcess.extend(myLumis)

process.hltHighLevel = cms.EDFilter("HLTHighLevel",
   TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
   HLTPaths = cms.vstring('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ*'),           # 'HLT_DoubleMu*', 'HLT_Mu17*' provide list of HLT paths (or patterns) you want
   eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
   andOr = cms.bool(True),             # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
   throw = cms.bool(True)    # throw exception on unknown path names
)

process.demo = cms.EDAnalyzer('MiniAnalyzerSim',
                              muons = cms.InputTag("slimmedMuons"),
                              xsec = cms.double(20480), #6422 for first, 20480 for second
                              lumi = cms.double(6658)
)


process.p = cms.Path(process.hltHighLevel+process.demo)
