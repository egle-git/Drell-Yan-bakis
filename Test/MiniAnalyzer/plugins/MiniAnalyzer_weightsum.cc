// -*- C++ -*-
//
// Package:    Test/MiniAnalyzer
// Class:      MiniAnalyzer
// 
/**\class MiniAnalyzer MiniAnalyzer.cc Test/MiniAnalyzer/plugins/MiniAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  
//         Created:  Thu, 01 Feb 2024 02:16:09 GMT


// system include files
#include <memory>
#include <vector>
#include "TFile.h"
#include "TH1D.h"
#include <fstream>
#include <iostream>
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

// class declaration

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

// edm::one::WatchRuns /////after SharedResources, before >

class MiniAnalyzer_weightsum : public edm::one::EDAnalyzer<edm::one::SharedResources> {
   public:
      explicit MiniAnalyzer_weightsum(const edm::ParameterSet&);
      ~MiniAnalyzer_weightsum();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::EDGetTokenT<GenEventInfoProduct> weightToken_;

      std::string mcProcess_;
      double weight_sum = 0; 
};

// constants, enums and typedefs
// static data member definitions
// constructors and destructor


MiniAnalyzer_weightsum::MiniAnalyzer_weightsum(const edm::ParameterSet& iConfig):
      weightToken_(consumes<GenEventInfoProduct>(iConfig.getUntrackedParameter<edm::InputTag>("GenEventInfo"))),
      mcProcess_(iConfig.getParameter<std::string>("mcProcess"))
    {
        usesResource("TFileService");
    }


MiniAnalyzer_weightsum::~MiniAnalyzer_weightsum()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


void
MiniAnalyzer_weightsum::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<GenEventInfoProduct> weightHandle;
   iEvent.getByToken(weightToken_, weightHandle);
   double event_weight = weightHandle.isValid() ? weightHandle->weight() : 1.0;
   double norm_weight = event_weight / std::abs(event_weight);
   weight_sum += norm_weight;
   // std::cout << "weight sum = " << weight_sum << std::endl;
   // std::cout << "event weight: " << event_weight << std::endl;
   // std::cout << "norm weight: " << norm_weight << std::endl;
}
   

/** 
#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
*/

// ------------ method called once each job just before starting event loop  ------------
void 
MiniAnalyzer_weightsum::beginJob()
{

}

// ------------ method called once each job just after ending the event loop  ------------
void 
MiniAnalyzer_weightsum::endJob() 
{
   std::string outputfile;
   if (mcProcess_ == "sim1")
      outputfile = "weight_sumtest.txt";
   else if (mcProcess_ == "sim2")
      outputfile = "weight_sumtest2.txt";
   else if (mcProcess_ == "tt")
      outputfile = "weight_sumtestTT.txt";
   else if (mcProcess_ == "tt_inclusive")
      outputfile = "weight_sumtestTTinclusive.txt";
   else if (mcProcess_ == "ww")
      outputfile = "weight_sumtestww.txt";
   else if (mcProcess_ == "wz")
      outputfile = "weight_sumtestwz.txt";
   else if (mcProcess_ == "zz")
      outputfile = "weight_sumtestzz.txt";
   else if (mcProcess_ == "twtop")
      outputfile = "weight_sumtesttwtop.txt";
   else if (mcProcess_ == "twantitop")
      outputfile = "weight_sumtesttwantitop.txt";
   else if (mcProcess_ == "tchantop")
      outputfile = "weight_sumtesttchantop.txt";
   else if (mcProcess_ == "tchanantitop")
      outputfile = "weight_sumtesttchanantitop.txt";
   std::ofstream outFile(outputfile.c_str());
   
   if (outFile.is_open())
   {
      outFile << weight_sum << std::endl;
      outFile.close();
   }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MiniAnalyzer_weightsum::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MiniAnalyzer_weightsum);
