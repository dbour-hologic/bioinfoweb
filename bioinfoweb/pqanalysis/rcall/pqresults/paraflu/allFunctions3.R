####################################################################################################
# Kyle's R Scripts for PQ/Curve/TCYC related files
# Updated: 9/16/16, 1:19PM
####################################################################################################

### This function is a basic "generator" to be used with other functions for data mining
### list_file: pass a list of directories/filepaths/etc. and it will aggregate all the data into one
#### single data frame.
### defined.function: give appender a single function and it will carry out that action as many times
#### as the length of the list
appender = function(list_file, defined.function, ...){
     require(tools)
     # list_file = assay.files
     # defined.function = grabber
     
     list_file.df = data.frame(files = list_file, stringsAsFactors = FALSE)
     list_file.df$loaded = "READ"
     
     #list_file
     #str(list_file.df)
     
     empty.df = data.frame()
     for(u in 1:length(list_file)){
          cat(list_file.df$files[u])
          cat("\n")
          b = try(defined.function(list_file.df$files[u], ...))
          #b = try(defined.function(list_file.df$files[6]))
          if(class(b) == "try-error"){
               list_file.df$loaded[u] = "ERROR"
          } else if(class(b) == "data.frame"){
               if(u == 1){
                    b$type = dirname(list_file.df$files[u])
                    final.df = rbind(empty.df, b)
                    list_file.df$loaded[u] = "LOADED"
               } else{
                    b$type = dirname(list_file.df$files[u])
                    final.df = rbind(final.df, b)     
                    list_file.df$loaded[u] = "LOADED"
               }
          } else{
               return("Something other than a dataframe was loaded.")
          }
     }
     
     #rm(list_file.df, final.df)
     cat("\n")
     cat("Finished reading and appending.")
     output = list(pq.data = final.df, list.output=list_file.df)
     return(output)
}

### Main function for reading PCRExport files
#### Instructions: for "use" pass either "report" or anything else, "report" should only be used for
#### the pq report generator if another string is pass it will behave otherwise.
grabber = function(file_path, use="report"){
     require(tools); require(xlsx); require(lubridate);
     # file_path = lof[1]
     if(file_ext(file_path) == "csv"){
          a=read.csv(file_path, stringsAsFactors = FALSE)
     } else{
          a=read.xlsx2(file_path, sheetIndex = 1)
     }
     cat("File is ", basename(file_path))
     cat("\n")
     
     names(a)[1] = "Sample"
     names(a)[names(a) == "Test.order.."] = "test.order"
     names(a)[names(a) == "LR_Ct_NonNormalized"] = "ct"
     names(a)[names(a) == "LR_TSlope_NonNormalized"] = "tslope"
     names(a)[names(a) == "Cartridge.Lot.."] = "CartridgeLotNum"
     a = a[!(grepl("end", a$Sample)),]
     
     #data-extraction from filename
     a$filepath <- file_path

     if(use=="report"){
          ### New process to extract serial number without destroying data storage
          temp = strsplit(basename(a$filepath), split="_")
          temp2 = lapply(temp, `[[`, 2)
          temp3 = unlist(temp2)
          temp4 = strsplit(temp3, split="-")
          temp5 = unlist(temp4)
          a$pantherSN = substr(temp5[1], 4, nchar(temp5[1]))
          a$ud.filename = lapply(temp, `[[`, 1)[[1]]
          a$filename = lapply(temp, `[[`, 2)[[1]]
     } else{
          a$pantherSN = a$Serial.Number
          a$ud.filename = "Non-report Use"
          a$filename = basename(file_path)
     }
     
     #metrics of interest
     a$ct = as.double(as.character(a$ct))
     a$RFU.Range = as.double(as.character(a$RFU.Range))
     a$EstimatedBaseline = as.double(as.character(a$EstimatedBaseline))
     a$tslope = as.double(as.character(a$tslope))
     
     #Time data-processing
     a$Completion.Time.UTC = as.character(a$Completion.Time.UTC)
     a$Completion.Time.UTC = mdy_hms(a$Completion.Time.UTC)
     a$pipette.Time.UTC = as.character(a$Pipette.Time.UTC)
     a$Pipette.Time.UTC = mdy_hms(a$pipette.Time.UTC)
     a$pipette.time = with_tz(a$Pipette.Time.UTC, "America/Los_Angeles")
     a$pipette.time = substr(a$pipette.time, 11, 20)
     a$completion.time = with_tz(a$Completion.Time.UTC, "America/Los_Angeles")
     a$completion.date = substr(a$completion.time, 0, 10)
     a$completion.date = as.factor(a$completion.date)
     
     
     #Turn Reagent lot info into factors
     subset.a <- a[, c("CartridgeLotNum", "CapAndVialTrayID", "FCRBarcode", "FERBarcode",
                       "ElutionBufferRFID", "CartridgeBarcode", "ReconstitutionBufferRFID", "OilRFID")]
     
     a[, c("CartridgeLotNum", "CapAndVialTrayID", "FCRBarcode", "FERBarcode",
           "ElutionBufferRFID", "CartridgeBarcode", "ReconstitutionBufferRFID", "OilRFID")] <- lapply(subset.a, as.factor)
     
     a.s = subset(a, select=c(completion.date, pipette.time, Sample, Sample.Name, Run.ID, test.order, FusionTestOrder, WellID, Flag,
                              Channel, RFU.Range, ct, EstimatedBaseline, tslope,
                              FusionAssayName, FusionAssayVersion, Software.Revision,
                              filepath, filename, ud.filename, pantherSN,
                              FCROBS, FEROBS, CartridgeBarcode, CartridgeLotNum, CapAndVialTrayID, FCRBarcode,
                              FERBarcode, ElutionBufferRFID, ReconstitutionBufferRFID, OilRFID))
     
     #returns full PCR export file
     ## return(a)
     
     #returns subseted PCR export file
     return(a.s)
}

### "lis.grabber" is a function used in the PQReportCompiler its main function is to take all lis files
#### labeled with a @Pt prefix within a given directory and append them using "appender" and add to
#### a dataframe you desire.
lis.grabber = function(directory = "current"){
     # lis.file = read.delim(file = lof, stringsAsFactors = FALSE)
     # directory = "T:/CoreTeams/Radium/Assay Development_Orig/Kyle S/PQ Data/_Assay"
     # setwd(directory)
     if (directory == "current"){
          lof = list.files(pattern="@Pt", full.names = TRUE)
     } else{
          cat(paste("LIS files are located in:", directory))
          cat("\n")
          lof = list.files(path=directory, pattern="@Pt", full.names = TRUE, recursive = TRUE)
     }
     
     lis <- appender(lof, read.delim, stringsAsFactors = FALSE)
     filtered.lis <- lis$pq.data
     
     #removes pesky [end] character
     lv <- grepl("end", filtered.lis[,1])
     filtered.lis <- filtered.lis[!lv,]
     
     lis.subset = filtered.lis %>% select(Run.ID, Assay.Name, Test.order.., Interpretation.6:Interpretation.10)
     return(lis.subset)
}

### Alternative-useful plotting function
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
     library(grid)
     
     # Make a list from the ... arguments and plotlist
     plots <- c(list(...), plotlist)
     
     numPlots = length(plots)
     
     # If layout is NULL, then use 'cols' to determine layout
     if (is.null(layout)) {
          # Make the panel
          # ncol: Number of columns of plots
          # nrow: Number of rows needed, calculated from # of cols
          layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                           ncol = cols, nrow = ceiling(numPlots/cols))
     }
     
     if (numPlots==1) {
          print(plots[[1]])
          
     } else {
          # Set up the page
          grid.newpage()
          pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
          
          # Make each plot, in the correct location
          for (i in 1:numPlots) {
               # Get the i,j matrix positions of the regions that contain this subplot
               matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
               
               print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                               layout.pos.col = matchidx$col))
          }
     }
}

### This spreader function is to be used for PQReportCompiler
spreader = function(pcrexport){
     Channels <- as.character(unique(pcrexport$Channel))
     
     spreaded <- pcrexport %>%
          unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline, passes) %>%
          spread(Channel, metrics)
     
     separated <- spreaded
     for(channel in Channels){
          # print(channel);
          separated <- separate_(separated, col=channel, into=paste0(channel, c(".ct", ".tslope", ".rr", ".eb", ".result")), sep="_")
          # cat("Finished with ", channel)
          # cat("\n")
     }
     final <- separated %>% ungroup %>% group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
     return(final)
}

### This function can be used without passes/.result will eventually merge this with "spreader"
new_spreader = function(pcrexport){
     Channels <- as.character(unique(pcrexport$Channel))
     
     spreaded <- pcrexport %>%
          unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline) %>%
          spread(Channel, metrics)
     
     separated <- spreaded
     for(channel in Channels){
          # print(channel);
          separated <- separate_(separated, col=channel, into=paste0(channel, c(".ct", ".tslope", ".rr", ".eb")), sep="_")
          # cat("Finished with ", channel)
          # cat("\n")
     }
     final <- separated %>% ungroup %>% group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
     return(final)
}

### This spread function will be deprecated
spread_channels <- list(
     Ct = function(dataset) {
          dataset %>%
               select(-RFU.Range, -EstimatedBaseline, -tslope) %>%
               spread(Channel, ct) %>%
               group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
     },
     Range = function(dataset) {
          dataset %>%
               select(-ct, -EstimatedBaseline, -tslope) %>%
               spread(Channel, RFU.Range) %>%
               group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
     }
)

### A simple grouping function which takes "assay" tags from paraflu, flu, and amr or
### the function will also take in an "inputfile" otherwise known as a worklist id
### Several assay tags have been recorded below categorizer if no "inputfile" has been designated
categorizer = function(df, assay="paraflu", inputfile){
     if(missing(inputfile)){
          if(assay=="paraflu"){
               ###### If different Sample Names are used then alter these parameters
               pattern.nc= c("Negative Control", "NEG Control")
               pattern.pc= c("Positive", "POS Control")
               pattern.pna= c("FSNPANELA", "NEGATIVE-", "NEGATIVE_", "Paraflu-Panel-A", "Panel_A", "PanelA", "UNVPANELA")
               pattern.pnc= c("Panel-C", "PARA PANEL C", "Panel_C", "PanelC", "PARPANELC", "Paraflu Panel C", "Para Panel C")
               attach(df)
               nc.lv = grepl(paste(pattern.nc, collapse="|"), Sample.Name)
               pc.lv = grepl(paste(pattern.pc, collapse="|"), Sample.Name)
               pna.lv = grepl(paste(pattern.pna, collapse="|"), Sample.Name)
               pnc.lv = grepl(paste(pattern.pnc, collapse="|"), Sample.Name)
               detach(df)
               df$sample.type[nc.lv] = "Negative Control"
               df$sample.type[pc.lv] = "Positive Control"
               df$sample.type[pna.lv] = "Panel A"
               df$sample.type[pnc.lv] = "Panel C"
               return(df)
          } else if (assay=="amr"){
               ###### If different Sample Names are used then alter these parameters
               pattern.nc= c("Negative Control", "NEG Control")
               pattern.pc= c("Positive", "POS Control")
               pattern.pncl= c("PC_L")
               pattern.pncm= c("PC_M")
               attach(df)
               nc.lv = grepl(paste(pattern.nc, collapse="|"), Sample.Name)
               pc.lv = grepl(paste(pattern.pc, collapse="|"), Sample.Name)
               pncl.lv = grepl(pattern.pncl, Sample.Name)
               pncm.lv = grepl(pattern.pncm, Sample.Name)
               detach(df)
               df$sample.type[nc.lv] = "Negative Control"
               df$sample.type[pc.lv] = "Positive Control"
               df$sample.type[pncl.lv] = "Panel C-Low"
               df$sample.type[pncm.lv] = "Panel C-Medium"
               return(df)
          } else if (assay=="flu"){
               pattern.nc= c("Negative Control", "NEG Control")
               pattern.pc= c("Positive", "POS Control")
               pattern.pna= c("FSNPANELA", "NEGATIVE-", "Paraflu-Panel-A", "Panel_A")
               pattern.pncl= c("QCP1-300c")
               attach(df)
               nc.lv = grepl(paste(pattern.nc, collapse="|"), Sample.Name)
               pc.lv = grepl(paste(pattern.pc, collapse="|"), Sample.Name)
               pna.lv = grepl(paste(pattern.pna, collapse="|"), Sample.Name)
               pncl.lv = grepl(pattern.pncl, Sample.Name)
               detach(df)
               df$sample.type[nc.lv] = "Negative Control"
               df$sample.type[pc.lv] = "Positive Control"
               df$sample.type[pncl.lv] = "QC Panel"
               df$sample.type[pna.lv] = "Panel A"
               return(df)
          } else{
               return("Error")
          }
     } else{
          for(i in 1:length(inputfile$term)){
               df$sample.type[grepl(inputfile$term[i], df$Sample.Name)] = inputfile$type[i]
          }
          return(df)
     }
}

### This function CAN'T be combined with "appender". Pass it a "pcrexport" object and it should merge
#### the tcycfile's contents with the run information as well as "sample.type" it will return a DF
#### with EstimatedBaseline Subtracted curve and as well as the Raw RFU Range.
tcyc_reader = function(file_path, pcrexport){
     #file_path=tcyc
     #pcrexport = pqexport
     if(length(file_path)==0){
          return(1);
     } else{
          if(length(file_path)>1){
               return(1);
          } else{
               #file_path=temp.file
               #pcrexport = pq
               #Load in the data and restructure the df
               tcyc = read.csv(x, header=FALSE, stringsAsFactors=FALSE)
               tcyc = tcyc[,1:16]
               names_tcyc = as.character(unlist(tcyc[1,]))
               names(tcyc) = names_tcyc
               tcyc = tcyc[-1,] #delete first row after renaming
               
               #clean up names of columns
               names(tcyc) = str_trim(names(tcyc))
               names(tcyc) = str_to_lower(names(tcyc))
               names(tcyc) = gsub(" ", ".", names(tcyc))
               tcyc = tcyc %>% filter(!(grepl("end", cyclenum)))
               
               #restructure datatypes
               tcyc$fluorescence = as.numeric(tcyc$fluorescence)
               tcyc$cyclenum = as.factor(as.numeric(tcyc$cyclenum))
               tcyc$testorder.id = as.factor(tcyc$testorder.id)
               #rename(tcyc, test.order=testorder.id)
               tcyc$test.order = tcyc$testorder.id
               
               lookup=data.frame(
                    color=c("FAM", "HEX", "Red647", "Red677", "ROX"),
                    Channel=c("FAM", "HEX", "RED647", "IC", "ROX"),
                    stringsAsFactors = FALSE
               )
               
               tcyc = left_join(tcyc, lookup, by='color')
               tcyc2 = tcyc %>% ungroup %>% select(test.order, Channel, cyclenum, fluorescence, well)
               tcyc3 = tcyc2 %>% group_by(test.order, Channel, cyclenum, well) %>% summarise(mflu=mean(fluorescence, na.rm=T))
               
               tcyc3$test.order = as.numeric(as.character(tcyc3$test.order))
               #pcrexport2 = pcrexport %>% select(Sample.Name, sample.type, test.order, Channel, EstimatedBaseline)
               pcrexport2 = pcrexport %>% select(Sample.Name, sample.type, test.order, Channel, EstimatedBaseline, tslope)
               combined=left_join(pcrexport2, tcyc3, by=c("test.order", "Channel"))
               combined$EBsubtracted = combined$mflu - combined$EstimatedBaseline
               return(combined)
          }
     }
}

### "raw_plot" is a helper function which uses "grabber", "categorizer" and "tcyc_reader" this can be
#### used in lieu of the functions individually.
raw_plot = function(pq_file, tcyc_file){
     pqexport = pq_file %>% grabber
     assay.name = unique(pqexport$FusionAssayName)
     
     if(assay.name == "AdV/hMPV/RV"){
          assay.input = "amr"     
          print(assay.input)
     } else if(assay.name == "Flu A/B/RSV"){
          assay.input = "flu"     
          print(assay.input)
     } else if(assay.name == "Paraflu"){
          assay.input = "paraflu"     
          print(assay.input)
     } else{
          cat("NO!")
     }
     
     pqexport = pqexport %>% categorizer(assay = assay.input)
     #temp = tcyc_reader(x=tcyc, pcrexport=pq)
     temp=tcyc_reader(x=tcyc_file, pcrexport=pqexport)
     return(temp)
}

### "flaggregator" is a complicated function used in the PQReportCompiler that takes in a pcrexport dataframe with pass/hits and an
#### assay type it returns a neatly compiled dataframe with the types of flags as well as the number of
#### VVFS flags in a run.
flaggregator = function(df = fleet, assay="Paraflu"){
     # df = pq
     # assay = "Paraflu"
     if(assay=="Paraflu"){
          spreaded <- df %>%
               select(-pass, -threshold, -direction) %>%
               unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline, passes) %>%
               spread(Channel, metrics)
          spreaded2 <- spreaded %>%
               separate(col="FAM", into=c("FAM.ct", "FAM.tslope", "FAM.rr", "FAM.eb", "FAM.result"), sep="_") %>%
               separate(col="HEX", into=c("HEX.ct", "HEX.tslope", "HEX.rr", "HEX.eb", "HEX.result"), sep="_") %>%
               separate(col="IC", into=c("IC.ct", "IC.tslope", "IC.rr", "IC.eb", "IC.result"), sep="_") %>%
               separate(col="RED647", into=c("RED647.ct", "RED647.tslope", "RED647.rr", "RED647.eb", "RED647.result"), sep="_") %>%
               separate(col="ROX", into=c("ROX.ct", "ROX.tslope", "ROX.rr", "ROX.eb", "ROX.result"), sep="_")
          spreaded3 <- spreaded2 %>% ungroup %>% group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
     } else{
          Channels <- as.character(unique(df$Channel))
          
          spreaded <- df %>%
               unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline, passes) %>%
               spread(Channel, metrics)
          
          separated <- spreaded
          for(channel in Channels){
               # print(channel);
               separated <- separate_(separated, col=channel, into=paste0(channel, c(".ct", ".tslope", ".rr", ".eb")), sep="_")
               # cat("Finished with ", channel)
               # cat("\n")
          }
          spreaded2 <- separated %>% ungroup %>% group_by(Run.ID, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder))
          # return(final)
     }
     flags = list(appender = function(df){
          lv = names(table(df["Flag"])) != ""
          a = table(df["Flag"])[lv]
          b = as.character(a)
          lv2 = b != "0"
          b2 = a[lv2]
          c = names(b2)
          d = paste(b2,c, sep = "-")
          e = toString(d)
          return(e)
     },VVFS_count = function(df){
          lv = names(table(df["Flag"])) != ""
          a = table(df["Flag"])[lv]
          b = as.character(a)
          lv2 = b != "0"
          b2 = a[lv2]
          c = names(b2)
          c.lv = grepl("VVFS", c)
          e = sum(as.vector(b2[c.lv]))
          return(e)
     })
     spreaded2$Software.Revision = as.character(spreaded2$Software.Revision) ###Spreaded2 is a less processed form of PQ
     zzz = split(spreaded2, spreaded2$filename) ### Will use this eventually for joining
     temp.count = lapply(zzz, FUN=flags$VVFS_count)
     temp.appended = lapply(zzz, FUN=flags$appender)
     temp2 = unlist(temp.appended)
     temp1 = unlist(temp.count)
     temp3 = data.frame(filename = names(temp1), Flags= temp2, VVFS = temp1)
     temp3$Flags = as.character(temp3$Flags)
     lv = temp3$filename != ""
     temp3 = temp3[lv,]
     temp3
}
# flaggregator = function(df = fleet, assay="paraflu"){
#      if(assay=="paraflu"){
#           df %>% select(-pass, -hits) %>% unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline) %>% spread(Channel, metrics) -> spreaded
#           spreaded %>%
#                separate(col="FAM", into=c("FAM.ct", "FAM.tslope", "FAM.rr", "FAM.eb"), sep="_") %>%
#                separate(col="HEX", into=c("HEX.ct", "HEX.tslope", "HEX.rr", "HEX.eb"), sep="_") %>%
#                separate(col="IC", into=c("IC.ct", "IC.tslope", "IC.rr", "IC.eb"), sep="_") %>%
#                separate(col="RED647", into=c("RED647.ct", "RED647.tslope", "RED647.rr", "RED647.eb"), sep="_") %>%
#                separate(col="ROX", into=c("ROX.ct", "ROX.tslope", "ROX.rr", "ROX.eb"), sep="_") -> spreaded2
#           spreaded2 %>% ungroup %>% group_by(filename, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder)) -> spreaded3
#      } else{
#           df %>% select(-pass, -hits) %>% unite(col=metrics, ct, tslope, RFU.Range, EstimatedBaseline) %>% spread(Channel, metrics) -> spreaded
#           spreaded %>%
#                separate(col="FAM", into=c("FAM.ct", "FAM.tslope", "FAM.rr", "FAM.eb"), sep="_") %>%
#                separate(col="HEX", into=c("HEX.ct", "HEX.tslope", "HEX.rr", "HEX.eb"), sep="_") %>%
#                separate(col="IC", into=c("IC.ct", "IC.tslope", "IC.rr", "IC.eb"), sep="_") %>%
#                separate(col="ROX", into=c("ROX.ct", "ROX.tslope", "ROX.rr", "ROX.eb"), sep="_") -> spreaded2
#           spreaded2 %>% ungroup %>% group_by(filename, FusionTestOrder) %>% mutate(replicate=seq_along(FusionTestOrder)) -> spreaded3
#      }
#      
#      flags = list(
#                appender = function(df){
#                     lv = names(table(df["Flag"])) != ""
#                     a = table(df["Flag"])[lv]
#                     b = as.character(a)
#                     lv2 = b != "0"
#                     b2 = a[lv2]
#                     c = names(b2)
#                     d = paste(b2,c, sep = "-")
#                     e = toString(d)
#                     return(e)
#                },
#                VVFS_count = function(df){
#                     lv = names(table(df["Flag"])) != ""
#                     a = table(df["Flag"])[lv]
#                     b = as.character(a)
#                     lv2 = b != "0"
#                     b2 = a[lv2]
#                     c = names(b2)
#                     c.lv = grepl("VVFS", c)
#                     e = sum(as.vector(b2[c.lv]))
#                     return(e)
#                }
#           )
#      
#      spreaded2$Software.Revision = as.character(spreaded2$Software.Revision)
#      zzz = split(spreaded2, spreaded2$filename)
#      temp.count = lapply(zzz, FUN=flags$VVFS_count)
#      temp.appended = lapply(zzz, FUN=flags$appender)
#      temp2 = unlist(temp.appended)
#      temp1 = unlist(temp.count)
#      temp3 = data.frame(filename = names(temp1), Flags= temp2, VVFS = temp1)
#      temp3$Flags = as.character(temp3$Flags)
#      lv = temp3$filename != ""
#      temp3 = temp3[lv,]
#      
#      return(temp3)
# }

### "other_flags" is used in the PQReportCompiler and this function is used immediately after flaggregator,
#### it will count flags and return them appending them to the PCRExport dataframe as a column called "other.flags"
#### Future plans: merge this with flaggregator and maybe clean up
other_flags = function(x=c.summary2){

     d = vector(mode="list", length=length(x$Flags))
     e = vector(mode="numeric", length=length(x$Flags))
     a = strsplit(x$Flags, ",") 
     b = lapply(a, strsplit, "-")
     
     for(i in 1:length(b)){
          for(j in 1:length(b[[i]])){
               d[[i]][j] = b[[i]][[j]][c(FALSE, TRUE)]
          }
     }
     
     e = d %in% c("IUO", "VVFS")
     
     x$other.flags = e
     return(x)
}

### "curve_wave_form" is the work horse function that comprises of "reader" which is a basic .curve file reader
#### "reader" inside "curve_wave_form" is used to process the curve files and at the end of "curve_wave_form" is
#### a generator that creates a dataframe of these curves the output is a nice dataframe that can be used with ggplot2
#### for displaying curve files.
curve_wave_form = function(file, command, type, TOIs){ #Pulls all wave forms according to specific TOI/good for a single run
     reader = function(file, command, type, TOIs=NA){
          ncol = max(count.fields(file, sep=";"))
          b0 = read.table(file, sep=";", header=F, stringsAsFactors = F, fill=TRUE, col.names=1:ncol)
          
          names_b0 = as.character(unlist(b0[1,]))
          names(b0) = names_b0
          b0 = b0[-1,] #delete first row after renaming
          
          names(b0) = str_trim(names(b0))
          names(b0) = str_to_lower(names(b0))
          names(b0) = gsub(" ", ".", names(b0))
          
          #lv = b0$command.description == command
          # lv = b0$process.step == command
          #b1 = b0[lv,]
          b1 = b0
          
          if (is.na(TOIs) & typeof(TOIs) == "logical"){
               b1 = b1
          } else{
               file.toi.split = strsplit(b1$testorder.id, split=",")
               file.toi.refined = lapply(file.toi.split, str_trim)
               file.toi.lv = grepl(paste(TOIs, collapse = "|"), file.toi.refined)
               if(any(file.toi.lv) == FALSE){
                    return("these are not the droids you are looking for...");
               } else{
                    b1 = b1[file.toi.lv,]
               }
          }
          
          name.lv = is.na(names(b1))
          length.name = sum(name.lv)
          names(b1)[name.lv] = 1:length.name
          tis = grep("^values$", names(b1)) #trace-index-start
          
          ##subset curves
          if (type == "dispense"){
               trace = as.matrix(b1[,tis:ncol]) #for dispense
          } else if (type == "aspirate"){
               trace = as.matrix(b1[,tis:ncol]) #for aspiration
          } else{
               trace = as.matrix(b1[,tis:ncol]) #for sidecar
               if(substr(type, nchar(type), nchar(type)) == "a"){
                    lv.a = b1$process.step == "Aspirate"
                    #b0=b0[lv.a,]
                    trace = as.matrix(b1[lv.a, tis:ncol])
                    b1 = b1[lv.a,]
               } else if (substr(type, nchar(type), nchar(type)) == "d"){
                    lv.d = b1$process.step == "Dispense"
                    trace = as.matrix(b1[lv.d, tis:ncol])
                    b1 = b1[lv.d,]
               } else{
                    return(1);
               }
          }
          trace = as.matrix(b1[,tis:ncol])
          
          if (type == "dispense" | type == "aspirate"){
               linkage = data.frame(rows=as.numeric(rownames(b1)), cmd=b1$command.description, stringsAsFactors=F)
          } else{
               linkage = data.frame(rows=as.numeric(rownames(b1)), cmd=b1$step.type, stringsAsFactors=F, type=b1$process.step)
          }
          #linkage
          transposed.trace = t(trace)
          tt1 = as.data.frame(transposed.trace, row.names=NULL)
          
          tt1$index = 1:nrow(tt1)
          plot_data = melt(tt1, id.var="index")
          plot_data$value = as.numeric(plot_data$value)
          
          plot_data = plot_data[complete.cases(plot_data),]
          plot_data.2 = merge(plot_data, linkage, by.x="variable", by.y="rows")
          # 
          # if(substr(type, nchar(type), nchar(type)) == "a"){
          #      plot_data.2 = plot_data.2 %>% filter(type == "Aspirate")
          #      return(plot_data.2)
          # } else if (substr(type, nchar(type), nchar(type)) == "d"){
          #      plot_data.2 = plot_data.2 %>% filter(type == "Dispense")
          #      return(plot_data.2)
          # 
          return(plot_data.2)
     } #### End of reader function
     
     ### if length == 1 then carry along
     ### however if length > 1, then fuck.
     #go through each individual file
     if (length(file) > 1){
          df = data.frame()
          i=1
          while(i<=length(file)){
               df.sub = reader(file[i], command, type, TOIs)
               if(df.sub=="these are not the droids you are looking for..."){
                    #skip this one
                    #print(i)
                    #print(dim(df))
                    i <- i + 1
               } else{
                    #move onto next
                    df = rbind(df.sub, df)
                    #print(i)
                    #print(dim(df))
                    i <- i + 1
               }
          }
          if(is.data.frame(df) & nrow(df) == 0){
               return("curve_wave_form: More than one .curve file was supplied in directory parsing through all files.")
          } else{
               return(df)
          }
     } else if (length(file) == 1){
          df = reader(file, command, type, TOIs)
          return(df)
     } else{
          return("ERROR - Proper file is not supplied.")
     }
}

###Wilson Wang's Plotting Function
summary.pq.plot <- function(dat, 
                            xvar, yvar, color.by=xvar, 
                            xgroups, ygroups, 
                            main.title = yvar, xlabel="", ylabel=yvar, 
                            accept.neg, accept.pos) {
     
     require(ggplot2)
     
     if (missing(accept.neg))
          accept.neg = data.frame(Channel=c("FAM", "HEX", "ROX", "RED647", "IC"), AcceptVal=c(500,500,500,350,2000))
     
     if (missing(accept.pos))
          accept.pos = data.frame(Channel=c("FAM", "HEX", "ROX", "RED647", "IC"), AcceptVal=c(1200,2000,1500,400,2000))   
     
     
     dat$sample.type = factor(dat$sample.type, levels=c("Negative Control",  "Positive Control", "Panel A", "Panel C"),
                                 labels=c("Negative Control",  "Positive Control", "Panel A", "Panel C"))
     dat$Channel = factor(dat$Channel, levels=c("FAM", "HEX", "ROX", "RED647", "IC"))
     
     colVals = c("darkgreen", "red3", "darkgreen", "red3")
     names(colVals) = levels(dat$sample.type)
     
     bp = ggplot(dat, aes_string(x=xvar, y=yvar, color=color.by)) + 
          scale_color_manual(values = colVals) + 
          geom_jitter(position=position_jitter(0.1), cex=1.5, na.rm=T) +
          geom_boxplot(alpha=0.5, aes_string(group=xvar), outlier.shape=NA, fill="white", na.rm=T) + 
          theme(axis.text.x = element_text(angle = 60, hjust = 1, colour="black"), 
                axis.text.y = element_text(colour="black"),
                panel.background = element_rect(fill = 'gray93')) + 
          ggtitle(main.title) + 
          xlab(xlabel) + ylab(ylabel) +
          theme(plot.title = element_text(lineheight=.8, face="bold", size=20))
     bp
     f = as.formula(paste(paste(ygroups, collapse=" + ", sep=""), "~", paste(xgroups, collapse=" + ", sep=""), sep=" "))
     if (!is.null(accept.neg) | !is.null(accept.pos)) {
          bp + facet_grid(f, scales="free") +
               geom_hline(aes(yintercept = AcceptVal), accept.neg, colour="darkgreen", na.rm=T) +
               geom_hline(aes(yintercept = AcceptVal), accept.pos, colour="red3", na.rm=T) +
               theme(strip.text.x = element_text(size = 16))
     } else {
          bp + facet_grid(f="free") +
               theme(strip.text.x = element_text(size = 16))
     }
}