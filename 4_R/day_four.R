# local({r <- getOption("repos")
#        r["CRAN"] <- "http://cran.r-project.org"
#        options(repos=r)})
# install.packages("tidyverse")


library(tidyverse)

partOne <- function(){
    fileName <- 'day_four_data.txt'
    data <- readChar(fileName, file.info(fileName)$size)
    values <- c("byr","iyr","eyr","hgt","hcl","ecl","pid")
    codes <- unlist(str_split(data,'\n\n'))
    summary <- c()
    i <- 1
    for (code in codes) { 
        summary[[i]] <- all(str_detect(code, values))
        i <- i + 1
    }
    sum(unlist(summary))
}
# partOne()

checkHeight <- function(height){
    inch = strtoi(str_match(height,'([0-9]*)in$')[1,2])
    inch_valid <- (inch >= 59 ) & (inch <= 76)

    cm = strtoi(str_match(height,'([0-9]*)cm$')[1,2])
    cm_valid <- (cm >= 150 ) & (cm <= 193)

    replace_na(cm_valid | inch_valid, FALSE)
}

checkValid <- function(passport){
    byr <- strtoi(str_match(passport,"byr:(.*?)(?: |$|\n)")[1,2])
    byr_valid <- (byr >= 1920) & (byr <= 2002)
    
    iyr <- strtoi(str_match(passport,"iyr:(.*?)(?: |$|\n)")[1,2])
    iyr_valid <- (iyr >= 2010) & (iyr <= 2020)

    eyr <- strtoi(str_match(passport,"eyr:(.*?)(?: |$|\n)")[1,2])
    eyr_valid <- (eyr >= 2020) & (eyr <= 2030)

    hgt <- str_match(passport,"hgt:(.*?)(?: |$|\n)")[1,2]
    hgt_valid <- checkHeight(hgt)

    hcl <- str_match(passport,"hcl:(.*?)(?: |$|\n)")[1,2]
    hcl_valid <- str_detect(hcl,'^#[0-9a-f]{6}$')

    ecl <- str_match(passport,"ecl:(.*?)(?: |$|\n)")[1,2]
    ecl_valid <- ecl %in% c('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    pid <- str_match(passport,"pid:(.*?)(?: |$|\n)")[1,2]
    pid_valid <- str_detect(pid,'^[0-9]{9}$')

    replace_na(c(byr_valid, iyr_valid, eyr_valid, hgt_valid, hcl_valid, ecl_valid, pid_valid), FALSE)
}

# passport <- "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
# hcl:#623a2f"
# checkValid(passport)

partTwo <- function(){
    fileName <- 'day_four_data.txt'
    data <- readChar(fileName, file.info(fileName)$size)
    codes <- unlist(str_split(data,'\n\n'))
    summary <- c()
    i <- 1
    for (code in codes) { 
        summary[[i]] <- all(checkValid(code))
        i <- i + 1
    }
    sum(summary)
}
partTwo()