#Author: KSuico
#Wrapper for calling report generator script

#Use absolute paths for first two lines
# Command Arguments
args=commandArgs(trailingOnly = TRUE)

cat(args, sep="\n")

if(length(args)==0){
  stop("At least one argument must be supplied (input directory)", call.=TRUE)
} else if(length(args) == 13){
  # params <- read.table(args[1], header=TRUE, sep="\t", stringsAsFactors = FALSE)
} else{
  stop("Please provide the correct number of arguments (13).")
}



cat("Here are the arguments provided:\n")
params = list(ANALYSIS_FILE=args[1],
              RMD_FILE=args[2],
              OUTPUT_DIR=args[3],
              USR_NAME=args[4],
              DATA_DIR=args[5],
              STAT_TYPE=args[6],
              AS_TYPE=args[7],
              WRKLIST=args[8],
              LIM_FILE=args[9],
              ANA_ID=args[10],
              GRPH_TYPE=args[11],
              IGN_FLAGS=args[12],
              CNTRL_SPEC=args[13])

cat("Starting analysis script.", sep="\n")
source(params$ANALYSIS_FILE)
cat("Finished sourcing the analysis script...\n")

cat("End dataframe dimensions:\n")
cat(dim(join.wlid.limits.ic.hiv), "\n")

rmarkdown::render(params$RMD_FILE,
                  output_file=paste0(params$OUTPUT_DIR, "/", params$ANA_ID, ".html"))

#Sample windows, local execution script
# system(paste('Rscript wrapper.R "C:/Users/KS0316/Documents/qHIV-1 Report Generator/params4.txt"'))
# system(paste('Rscript "C:/Users/KS0316/qHIV-1 Report Generator/wrapper.R" "C:/Users/KS0316/Documents/qHIV-1 Report Generator/params4.txt"'))
# system(paste('Rscript wrapper.R',
#              'C:/Users/KS0316/Documents/qHIV-1 Report Generator/join_vl_lis.R',
#              'C:/Users/KS0316/Documents/qHIV-1 Report Generator/flexdashboard_test.Rmd',
#              'C:/Users/KS0316/Documents/qhivtest/AnalysisID1234',
#              'Kyle',
#              'C:/Users/KS0316/Documents/qhivtest/AnalysisID1234',
#              'NA',
#              'qHIV',
#              'C:/Users/KS0316/Documents/qhivtest/wlid.csv',
#              'C:/Users/KS0316/Documents/qhivtest/limits.csv',
#              'Analysis1234',
#              'NA',
#              'NA',
#              'C:/Users/KS0316/Documents/qhivtest/contspecs2.csv'))


