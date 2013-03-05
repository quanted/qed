pest_root<-path.expand("~/Dropbox/apppest/ppis/")

#pccode- EPA assigned pesticide chemical code for active ingredient
#casnum- Chemical Abstract System Registry number
#a single casnum may have multiple pccode and vice-versa
#regnum- EPA assigned pesticide product registration number
####### mask of ZZZZZ9-ZZZZ9 where the first 6 digits are the registrant company number
#prodname- registrant's pesticide product name

#CHEMCAS
chemcas <- read.fwf(paste(pest_root,"CHEMCAS.TXT",sep=""),widths=c(6,10))
colnames(chemcas) <- c("pccode","casnum")
dim(chemcas)
class(chemcas$pccode)
length(unique(chemcas$pccode))
class(chemcas$casnum)
length(unique(chemcas$casnum))

#CHEMNAME
#funky character at Lavandulyl senecioate deleted
#problems with the pccodes- blanks and text elements
chemname <- read.fwf(paste(pest_root,"CHEMNAME.TXT",sep=""),widths=c(6,20,253),stringsAsFactors=FALSE)
colnames(chemname) <- c("pccode","ctype","pcname")
dim(chemname)
class(chemname$pccode) <- "integer"
length(unique(chemname$pccode))
class(chemname$pcname)
length(unique(chemname$pcname))

#merge chemcas and chemname on pccode, drop pccodes that do not have both cas number and descriptive
#active ingredient name
chemmerge <- merge(chemcas,chemname)[,c(1,2,4)]
colnames(chemmerge)
dim(chemmerge)
summary(chemmerge)
length(unique(chemmerge$pccode))
length(is.na(chemmerge$pccode))
length(unique(chemmerge$casnum))
length(unique(chemmerge$ctype))
length(unique(chemmerge$pcname))

# drop blanks
chemname <- chemname[-which(chemname$pcname==""),]

cm_nrows <- dim(chemmerge)[[1]]
#write chemmerge as chemkeys
write.csv(chemmerge[1:8000,],paste(pest_root,"chemkeys1.csv",sep=""),row.names=FALSE)
write.csv(chemmerge[8001:16000,],paste(pest_root,"chemkeys2.csv",sep=""),row.names=FALSE)
write.csv(chemmerge[16001:cm_nrows,],paste(pest_root,"chemkeys3.csv",sep=""),row.names=FALSE)
#FORMULA
formula <- read.fwf(paste(pest_root,"FORMULA.TXT",sep=""),widths=c(11,6,7))
colnames(formula) <- c("regnum","pccode","pcpct")
dim(formula)
length(unique(formula$pccode))
length(unique(formula$regnum))

#PRODUCT
#eliminated funky character (ae) in MGK  Intermediate 2967 and many others
# replace all '#' with ' '
product <- read.fwf(paste(pest_root,"PRODUCT.TXT",sep=""),widths=c(11,2,1,8,8,2,70,1,2,1))
colnames(product) <- c("regnum","formcode","toxcode","apprdate","candate","ctcode","prodname","rupflag","pmcode","condflag")
dim(product)
length(unique(product$regnum))
length(unique(product$prodname))

#formulamerge on regnum
formulamerge <- merge(formula,product)[,c(1:3,9)]
dim(formulamerge)
summary(formulamerge)
colnames(formulamerge)
#"regnum"   "pccode"   "pcpct"    "prodname"
length(unique(formulamerge$regnum))

#write formulamerge as formulakeys
pr_nrows <- dim(formulamerge)[[1]] #140978
write.csv(formulamerge[1:20000,],paste(pest_root,"formulakeys1.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[20001:40000,],paste(pest_root,"formulakeys2.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[40001:60000,],paste(pest_root,"formulakeys3.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[60001:80000,],paste(pest_root,"formulakeys4.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[80001:100000,],paste(pest_root,"formulakeys5.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[100001:120000,],paste(pest_root,"formulakeys6.csv",sep=""),row.names=FALSE)
write.csv(formulamerge[120001:pr_nrows,],paste(pest_root,"formulakeys7.csv",sep=""),row.names=FALSE)
