#!/usr/bin/env python
#-*- coding:utf-8 -*-

#import some general python modules:
import sys
import os

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status

import transformers

#When the wrapper is started, the current working directory corresponds to the project directory, input files are in input/ , output files should go in output/ .

#make a shortcut to the shellsafe() function
shellsafe = clam.common.data.shellsafe

#this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY
#(as configured at COMMAND= in the service configuration file, there you can
#reconfigure which arguments are passed and in what order.
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]

#If you make use of CUSTOM_FORMATS, you need to import your service configuration file here and set clam.common.data.CUSTOM_FORMATS
#Moreover, you can import any other settings from your service configuration file as well:

#from yourserviceconf import CUSTOM_FORMATS
#clam.common.data.CUSTOM_FORMATS = CUSTOM_FORMATS

#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml)), always pass CUSTOM_FORMATS as second argument if you make use of it!
clamdata = clam.common.data.getclamdata(datafile)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Initialising...")

gpu = False
kwargs = {}
try:
    gpu = clamdata['gpu']
except KeyError:
    pass

clam.common.status.write(statusfile, "Loading model...")

undisputed_best_model = transformers.MBartForConditionalGeneration.from_pretrained(
    "ml6team/mbart-large-cc25-cnn-dailymail-xsum-nl"
)
tokenizer = transformers.MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")
pipeline = transformers.pipeline(
    task="summarization",
    model=undisputed_best_model,
    tokenizer=tokenizer,
)
if gpu:
    import torch
    pipeline.to(torch.device("cuda"))
pipeline.model.config.decoder_start_token_id = tokenizer.lang_code_to_id[
    "nl_XX"
]

clam.common.status.write(statusfile, "Starting...")

for inputfile in clamdata.input:
    inputtemplate = inputfile.metadata.inputtemplate
    inputfilepath = str(inputfile)

    clam.common.status.write(statusfile, "Processing " + os.path.basename(inputfilepath),100) # status update

    with open(inputfilepath,'r', encoding="utf-8") as f:
        text = f.read()


    outputfilepath = os.path.join(outputdir, os.path.basename(inputfilepath)[:-4]) + ".summary.txt"
    with open(outputfilepath,"w") as f:
        print(pipeline(
            text,
            do_sample=True,
            top_p=0.75,
            top_k=50,
            min_length=50,
            early_stopping=True,
            truncation=True,
        )[0]["summary_text"], file=f)

#A nice status message to indicate we're done
clam.common.status.write(statusfile, "Done",100) # status update

sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
