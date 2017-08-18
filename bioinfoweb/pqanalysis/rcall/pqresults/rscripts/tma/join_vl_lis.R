#join_vl_lis V0.1
#author: Kyle Suico
#change log
#7/14/2017, 5:58am: script annotation
#7/18/2017, 3:28pm: improvements to variable names for readability

#For debugging and interacting
# args <- c("C:/Users/KS0316/Documents/qHIV-1 Report Generator/config4.txt")
#config <- read.table(args[1], header=TRUE, sep="\t", stringsAsFactors = FALSE)

###Dependencies and functions
#Packages
require(dplyr)
require(stringr)
require(tidyr)

#user-defined functions
read.lis <- function(x){
  max.num.cols = length(count.fields(x))-2
  file <- read.delim(x, nrows=max.num.cols, stringsAsFactors = FALSE)
  file
}
read.vli <- function(x){
  max.num.cols = length(count.fields(x))-2
  file <- read.csv(x, nrows=max.num.cols, stringsAsFactors = FALSE)
  file
}
#end user-defined functions

#config input: Specify working directory
setwd(params$DATA_DIR)

#find all lis and viral load exports
lof.lis <- list.files(pattern="@Pt", full.names = TRUE)
lof.vl <- list.files(pattern="@VLI", full.names = TRUE)

#logic and potential error handling do inputs match?

cat("Checking a mismatch in Viral Export and LIS inputs...", sep="\n")
if(length(lof.lis) == length(lof.vl)){
  lof.lis.short <- lof.lis %>% str_split(pattern=".lis") %>% sapply(`[`, 1) %>% str_split(pattern="-") %>% lapply(`[`, 4:6) %>% sapply(paste, collapse="-")
  lof.vl.short <- lof.vl %>% str_split(pattern=".csv") %>% sapply(`[`, 1) %>% str_split(pattern="-") %>% lapply(`[`, 4:6) %>% sapply(paste, collapse="-")
  if(all(lof.lis.short %in% lof.vl.short)){
    cat("No issues detected.", sep="\n")
  } else{
    cat("Non-matching files exist.", sep="\n")
  }
} else{
  cat("Please upload the correct number of files.", sep="\n")
  cat("There exists a non-matching set of LIS and VL files.", sep="\n")
  lof.lis.short <- lof.lis %>% str_split(pattern=".lis") %>% sapply(`[`, 1) %>% str_split(pattern="-") %>% lapply(`[`, 4:6) %>% sapply(paste, collapse="-")
  lof.vl.short <- lof.vl %>% str_split(pattern=".csv") %>% sapply(`[`, 1) %>% str_split(pattern="-") %>% lapply(`[`, 4:6) %>% sapply(paste, collapse="-")
  cat("Inputs will be filtered down to only matching files.", sep="\n")
  lof.lis <- lof.lis[lof.lis.short %in% lof.vl.short]
  lof.vl <- lof.vl[lof.vl.short %in% lof.lis.short]
}

#Load the lis and viral export data
cat("Loading in the data...", sep="\t")
lis <- data.frame(stringsAsFactors = FALSE)
lis.list <- lapply(lof.lis, read.lis)
lis <- do.call("rbind", lis.list)

vli <- data.frame(stringsAsFactors = FALSE)
vli.list <- lapply(lof.vl, read.vli)
vli <- do.call("rbind", vli.list)
if(exists("vli") & exists("lis")){
  cat("All data loaded!", sep="\n")
} else{
  cat("Error during data loading...", sep="\n")
}


#Channel/RTF/Target Dictionary
chnl.dict <- data.frame(Channel=c("RTF1", "RTF3", "RTF5"),
                 Color=c("FAM", "HEX", "ROX"),
                 Target=c("POL", "LTR", "GIC"),
                 stringsAsFactors = FALSE)

#Change viral load data from long to wide format.
cat("Spreading Viral Load file...", sep="\t")
vl.spread <- vli %>%
  left_join(chnl.dict) %>%
  select(Run.ID, Sample.Type, Test.order.., Sample.Name, Target, RFU.Range, EstimatedBaseline, LR_TTime, LR_TSlope) %>%
  unite(metrics, RFU.Range, EstimatedBaseline, LR_TTime, LR_TSlope, sep="_") %>%
  spread(key=Target, value=metrics)

targets <- c("POL", "LTR", "GIC")
for(target in targets){
  vl.spread <- vl.spread %>% separate_(col=target, into=paste0(target, c(".RR", ".EB", ".TT", ".TS")), sep="_")  
}

if(exists("vl.spread")){
  cat("Spread, works!", sep="\n")
} else{
  cat("Spread, failed.", sep="\n")
}

if(nrow(lis) == nrow(vl.spread)){
  cat("Samples are missing.\n")
} else{
  cat("Number of samples missing:", abs(nrow(vl.spread)-nrow(lis)), "\n")
}

#Join lis and vl.spreaded files
joined <- left_join(lis, vl.spread, by=c("Run.ID", "Sample.Name", "Test.order..", "Sample.Type"))
joined <- joined %>% rename(Test.order = Test.order..)
names(joined)[1] <- "Specimen.Barcode"

#Main separating feature between the US and EU LIS report styles
joined$ReportStyle[!is.na(joined$Interpretation.5)] = "US"
joined$ReportStyle[is.na(joined$Interpretation.5)] = "CE"

joined$GIC.TT <- as.numeric(joined$GIC.TT)

#config input: worklist id
wlid <- read.csv(params$WRKLIST, stringsAsFactors = FALSE, colClasses=c("SearchTerm"="character"))

for(i in 1:length(wlid$SearchTerm)){
  #cat(wlid$SearchTerm[i])
  #cat("\n")
  joined$SampleType[grepl(wlid$SearchTerm[i], joined$Sample.Name)] = wlid$SampleType[i]
}
joined$SampleType[is.na(joined$SampleType)] = "Uncategorized"

joined$Lot.Number <- joined$Sample.Name %>% str_split(" - Lot ") %>% sapply(`[`, 2)

#config input: control specification
contspecs <- read.csv(file = params$CNTRL_SPEC, stringsAsFactors = FALSE, colClasses = c("Lot.Number"="character"))
joined.wlid.spec <- left_join(joined, contspecs, by=c("SampleType", "Lot.Number"))

#config input: limits file
limits <- read.csv(params$LIM_FILE, stringsAsFactors = FALSE)
join.wlid.limits <- left_join(joined.wlid.spec, limits, by="SampleType")

###GIC check - Does the sample have valid internal control?
###Notes:CE = Interpretation.3,US = Interpretation.4
join.wlid.limits.ic <- join.wlid.limits %>%
  mutate(GIC.pass = ifelse(is.na(GIC.TT), FALSE,
                           ifelse(GIC.TT_max == 99 & !is.na(GIC.TT), TRUE,
                           ifelse(round(GIC.TT) <= GIC.TT_max, TRUE, FALSE))))

### HIV log copies calculation
isSign <- join.wlid.limits.ic$Interpretation.2 %>% substr(0,1)
#Code the positive calbirator as '1'
join.wlid.limits.ic$Interpretation.2.num <- ifelse(isSign == ">" | isSign == "<" | isSign == "", 1, as.numeric(join.wlid.limits.ic$Interpretation.2))
# join.wlid.limits.ic %>% select(contains("Interpretation.2")) %>% utils::View()

### Create variable called HIVSpecPass and check whether sample result is between Interp_min/max
join.wlid.limits.ic.hiv <- join.wlid.limits.ic %>%
  mutate(Interpretation.2.num=ifelse(is.na(Interpretation.2.num), -1, Interpretation.2.num)) %>%
  mutate(HIVSpecPass=ifelse(Interpretation.2.num == -1 & is.na(GIC.TT), FALSE,
                            ifelse(Interpretation.2_min == 0.0 & Interpretation.2_max == 0.0 & Interpretation.2.num == -1, TRUE,
                                   ifelse(Interpretation.2.num >= Interpretation.2_min & Interpretation.2.num <= Interpretation.2_max, TRUE, FALSE))))

#Change data types from character => numeric
numeric.columns <- c("GIC.RR", "GIC.EB", "GIC.TT", "LTR.RR", "LTR.EB", "LTR.TT", "POL.RR", "POL.EB", "POL.TT")
join.wlid.limits.ic.hiv[,numeric.columns] <- lapply(join.wlid.limits.ic.hiv[,numeric.columns], as.numeric)

#Recovery Rate criteria
# join.wlid.limits.ic.hiv %>% filter(!is.na(POL.truth) | !is.na(LTR.truth)) %>% utils::View()
# join.wlid.limits.ic.hiv %>% filter(ReportStyle == "US") %>% utils::View()

join.wlid.limits.ic.hiv <- join.wlid.limits.ic.hiv %>% mutate(recovery.spec.pass = ifelse((!is.na(POL.truth) & !is.na(LTR.truth)), "check", NA))
join.wlid.limits.ic.hiv <- join.wlid.limits.ic.hiv %>%
  # select(POL.truth, LTR.truth, recovery.spec.pass, Interpretation.2.num, ReportStyle, Interpretation.3) %>%
  mutate(LogCopy.truth = ifelse(ReportStyle == "CE" & recovery.spec.pass == "check", log10(POL.truth),
                                ifelse(ReportStyle == "US" & recovery.spec.pass == "check" & Interpretation.3 == "POL", log10(POL.truth),
                                       ifelse(ReportStyle == "US" & recovery.spec.pass == "check" & Interpretation.3 == "LTR", log10(LTR.truth), NA)))) %>%
  # filter(recovery.spec.pass == "check") %>%
  mutate(Logdiff = abs(Interpretation.2.num - LogCopy.truth)) %>%
  mutate(recovery.spec.pass = ifelse(is.na(recovery.spec.pass), NA,
                                     ifelse(recovery.spec.pass == "check" & Logdiff < 0.5, TRUE, FALSE)))
# join.wlid.limits.ic.hiv$logdiff <- abs(join.wlid.limits.ic.hiv$Interpretation.2.num - log10(join.wlid.limits.ic.hiv$POL.truth))
# join.wlid.limits.ic.hiv %>% filter(ReportStyle == "US") %>% utils::View()


# join.wlid.limits.ic.hiv$Interpretation.1.num <- gsub(pattern=",", replacement="", join.wlid.limits.ic.hiv$Interpretation.1)
# join.wlid.limits.ic.hiv$Interpretation.1.num <- as.numeric(join.wlid.limits.ic.hiv$Interpretation.1.num)
# join.wlid.limits.ic.hiv$Interpretation.1 %>% str
# join.wlid.limits.ic.hiv %>% filter(!is.na(POL.truth) | !is.na(LTR.truth)) %>% utils::View()
# join.wlid.limits.ic.hiv %>% mutate(Recovery = ifelse(Interpretation.1) %>% utils::View()

save.image(file=paste0(params$OUTPUT_DIR, "/", params$ANA_ID, ".RData"))