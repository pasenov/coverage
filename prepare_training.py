#!/usr/bin/env python3
import json
import logging
logger = logging.getLogger("flashsim")
from flashsim.common.core import (
    FlashSimTrainingDatasetModule,
    FlashSimEfficiencyDatasetModule,
)
import ROOT
from array import array
from flashsim.training.generate_varprocessors import save_processors
from flashsim.common.event import FlashSimEvent
import os
import pickle
import torch
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import yaml
def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(dict, dict_representer)

#np.seterr(all='raise')

def prepare_training(config, folder, inputfiles, name,skip_extraction=False, skip_plots=False, debug=False):
    # check if the folder exists
    # create the folder
    if not skip_extraction:
      if not os.path.exists(folder):
        os.makedirs(folder)
      else:
        # delete npys
        files = [f for f in os.listdir(folder)]
        for f in files:
            if f.endswith(".npy"):
                os.remove(os.path.join(folder, f))

      sequence = [
        FlashSimTrainingDatasetModule(name, config, folder),
        
      ]
      if config["type"] == "vector":
        sequence.append(FlashSimEfficiencyDatasetModule(name, config, folder))
      j=0
      
      for inputfile in inputfiles:
        inputfile = ROOT.TFile.Open(inputfile)
        inputtree = inputfile.Get("Events")
        events = FlashSimEvent()
        totevents=inputtree.GetEntries()


        # --- save number of Events entries ---
        event_count_file = os.path.join(folder, "event_counts.json")

        # load existing counts if the file already exists
        if os.path.exists(event_count_file):
            with open(event_count_file, "r") as f:
                event_counts = json.load(f)
        else:
            event_counts = {}

        # use the ROOT filename as key
        event_counts[os.path.basename(inputfile.GetName())] = int(totevents)

        with open(event_count_file, "w") as f:
            json.dump(event_counts, f, indent=2)
        # ------------------------------------

        batches = int(totevents / 100000)+1
#       batches=1
        pbar = tqdm.tqdm(range(batches))
        for batch in pbar:
            logger.debug("batch %s" % batch)
            # create rdf
            events.new_batch(
                ROOT.RDataFrame(inputtree).Range(batch * 100000, (batch + 1) * 100000)
            )
            for o in sequence:
                logger.debug(o)
                events = o.run(events)

            if "out_types" not in config:
                config["out_types"] = {}
                for c in config["target_features"]:
                    config["out_types"][c] = events.rdf.GetColumnType(c)
            if debug:
                logger.debug("saving debug data")
                if isinstance(config["matching"]["target_mask"],str):
                    events.rdf.Snapshot("Events", os.path.join(folder, f"debug_data_{j}.root"),
                                    config["target_features"]+config["conditioning_features"]+[config["matching"]["target_mask"],config["matching"]["conditioning_index"]]
                                    +["M"+x for x in config["target_features"]+config["conditioning_features"]]
                                    )
                else:
                    events.rdf.Snapshot("Events", os.path.join(folder, f"debug_data_{j}.root"),
                                    config["target_features"]+config["conditioning_features"]+
                                    config["matching"]["target_mask"]+config["matching"]["conditioning_index"]+
                                    ["M"+x for x in config["target_features"]+config["conditioning_features"]]
                                    )

            j+=1
            
    # read numpy from folder
      for m in sequence:
        m.out.close()
      if len(inputfiles)>1:
          logger.debug("Shuffling data")
          data =np.load(folder + "/data.npy")
          #shuffle data and save it back
          np.random.shuffle(data)
          np.save(folder + "/data.npy",data)
          #now for data_eff if it exists
          if "data_eff.npy" in os.listdir(folder):
              data_eff =np.load(folder + "/data_eff.npy")
              np.random.shuffle(data_eff)
              np.save(folder + "/data_eff.npy",data_eff)
        
    else:
        rdf=ROOT.RDataFrame("Events",inputfiles[0])
        config["out_types"] = {}
        for c in config["target_features"]:
            config["out_types"][c] = rdf.GetColumnType(c)

    if "matching" in config and config["matching"] is not None and (  isinstance(config["matching"]["target_mask"], list) or 
    isinstance(config["matching"]["target_index"], list)     ):
        config["conditioning_features"] = [""]+config["conditioning_features"] 
   
    training_phy2nn, validation_nn2phy, inference_phy2nn, inference_nn2phy = save_processors(config, folder)
    #    logger.debug(config)
 
    pickle.dump(config, open(os.path.join(folder, "config.pkl"), "wb"))
    yaml.dump(config, open(os.path.join(folder, "config.yaml"), "w"))

    if not skip_plots:
      outfolder=folder+"/transformed_figures/"
      if not os.path.exists(outfolder):
        os.makedirs(outfolder)
      orig_phys=torch.tensor(np.load(folder + "/data.npy"))
      transformed=training_phy2nn(orig_phys) # [:,len(config["conditioning_features"]):].detach().numpy()
      phys=inference_nn2phy(torch.cat(
        (
        transformed[:,len(config["conditioning_features"]):],
        orig_phys[:,:len(config["conditioning_features"])],
        ) , 
      dim=1))
      # print transformed and orig wher phys is nan or inf
      #logger.debug("nan or inf")
      #logger.debug("tr nan/inf",transformed[torch.isnan(phys).detach().numpy() | torch.isinf(phys).detach().numpy()])
      #logger.debug("or nan/inf",orig_phys[torch.isnan(phys).detach().numpy() | torch.isinf(phys).detach().numpy()])
      # #logger.debug("tr nan",transformed[torch.isnan(phys).detach().numpy()])
      #logger.debug("or nan",orig_phys[torch.isnan(phys).detach().numpy()])
      phys=phys.detach().numpy()
      transformed=transformed.detach().numpy()
      orig_phys=orig_phys.detach().numpy()
      if len(phys) > 10 :
        logger.debug("Making plots")
      
        for ic,c in enumerate(config["conditioning_features"]+config["target_features"]):
        #  logger.debug(c)
        #  logger.debug("nan or inf for column",c )
        #  logger.debug("%s %s %s","tr nan/inf",transformed[np.isnan(phys[:,ic-len(config["conditioning_features"])]) | np.isinf(phys[:,ic-len(config["conditioning_features"])]),ic])
        #  logger.debug("%s %s %s","or nan/inf",orig_phys[np.isnan(phys[:,ic-len(config["conditioning_features"])]) | np.isinf(phys[:,ic-len(config["conditioning_features"])]),ic])
        #logger.debug("tr nan/inf",transformed[torch.isnan(phys).detach().numpy() | torch.isinf(phys).detach().numpy()])
        # logger.debug("or nan/inf",orig_phys[torch.isnan(phys).detach().numpy() | torch.isinf(phys).detach().numpy()])
          if np.isnan(phys[:,ic-len(config["conditioning_features"])]).any() or np.isinf(phys[:,ic-len(config["conditioning_features"])]).any():
              logger.debug("nan or inf for column %s",c )
              logger.debug("tr nan/inf %s",transformed[np.isnan(phys[:,ic-len(config["conditioning_features"])]) | np.isinf(phys[:,ic-len(config["conditioning_features"])]),ic])
              logger.debug("%s %s","or nan/inf",orig_phys[np.isnan(phys[:,ic-len(config["conditioning_features"])]) | np.isinf(phys[:,ic-len(config["conditioning_features"])]),ic])
              logger.warning("Removing nan or inf values from the plot")
          phys[np.isnan(phys)] = 0
          phys[np.isinf(phys)] = 0
          transformed[np.isnan(transformed)] = 0
          transformed[np.isinf(transformed)] = 0
          orig_phys[np.isnan(orig_phys)] = 0
          orig_phys[np.isinf(orig_phys)] = 0

          
              # phys[torch.isnan(phys[:,ic-len(config["conditioning_features"])])] = 0
              # phys[torch.isinf(phys[:,ic-len(config["conditioning_features"])])] = 0
              # transformed[torch.isnan(phys[:,ic-len(config["conditioning_features"])])] = 0
              # transformed[torch.isinf(phys[:,ic-len(config["conditioning_features"])])] = 0
              # orig_phys[torch.isnan(phys[:,ic-len(config["conditioning_features"])])] = 0
              # orig_phys[torch.isinf(phys[:,ic-len(config["conditioning_features"])])] = 0
          #change color for cond variables
          bins=np.histogram_bin_edges(orig_phys[:,ic],bins=100)
          if c in config["conditioning_features"]:
              color="red"
              plt.hist(orig_phys[:,ic],bins=bins,color=color,alpha=0.5)
              suff = "_original.png"
          else:
              color="blue"
              # use same binning
              plt.hist(orig_phys[:,ic],bins=bins,color="blue",alpha=0.5)
              plt.hist(phys[:,ic-len(config["conditioning_features"])],bins=bins,color="red",alpha=0.5)
              suff = "_identity_check.png"
          plt.savefig(outfolder + c + suff)
          plt.close()
              
          plt.hist(transformed[:,ic],bins=100,color=color)
          plt.savefig(outfolder+c+".png")
          plt.close()
          #log y scale version
          plt.hist(transformed[:,ic],bins=100,color=color)
          plt.yscale("log")
          plt.savefig(outfolder+c+"_log.png")
          plt.close()
          #draw on same plot orig and phys
      else:
        logger.debug("Not enough data to make plots")    
          


        
           
           


import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare training")
    parser.add_argument("folder", type=str, help="folder to save the training")
    parser.add_argument("config", type=str, help="config file")
    parser.add_argument("inputfiles", type=str, nargs="+", help="input files")
    parser.add_argument(
        "--skip_extraction",
        action=argparse.BooleanOptionalAction,
        help="only recompute the transforms",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--skip_plots",
        action=argparse.BooleanOptionalAction,
        help="only recompute the transforms",
        required=False,
        default=False,
    )
    #debug
    parser.add_argument(
        "--debug",
        action=argparse.BooleanOptionalAction,
        help="enable debug mode, saves one ROOT file per batch",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--loglevel", type=str, help="logging level", default="INFO", required=False
    )
    #config version
    parser.add_argument(
        "--nanoversion", type=str, help="config version", default="nanoV9", required=False
    )
    
    args = parser.parse_args()
    #import config given nanoversion
    import importlib
    config_module = importlib.import_module(f"flashsim.config.{args.nanoversion}")
    globals().update(
       {n: getattr(config_module, n) for n in dir(config_module) if not n.startswith("_")} 
    )

    logger.setLevel(args.loglevel)
    handler = logging.StreamHandler()
    handler.setLevel(args.loglevel)
    # Create formatter and add it to the handlers
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # import config from py file
    #   logger.debug(f"#{args.config}#")
    c = eval(args.config)
    prepare_training(c, args.folder, args.inputfiles, args.config,args.skip_extraction,args.skip_plots, args.debug)
