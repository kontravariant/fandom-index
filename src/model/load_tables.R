library(RSQLite)
library(ggplot2)
library(dplyr)

supplementStadia = function(capTbl) {
  # add old stadia rows
  old_stadia = read.csv("data/edit/stadium_rows.csv")
  capTbl = rbind(capTbl,old_stadia)
  
  # load name changes
  stadia_map = read.csv("data/edit/stadium_map.csv")
  for(row in 1:nrow(stadia_map)) {
    oldName = stadia_map[row,'Old.Name']
    newName = stadia_map[row,'New.Name']
    if(newName %in% capTbl$Stadium & !(oldName %in% capTbl$Stadium)) {
      oldInfo = capTbl %>% filter(Stadium == newName)
      oldInfo$Stadium = paste(oldName)
    }
    if(oldName %in% capTbl$Stadium & !(newName %in% capTbl$Stadium)) {
      oldInfo = capTbl %>% filter(Stadium == oldName)
      oldInfo$Stadium = paste(newName)
    }
    capTbl = rbind(capTbl,oldInfo)
  }
  
  return(capTbl)
}


dbname = "data/fandom.sqlite"
con = dbConnect(SQLite(),dbname)
dbListTables(con)

census = dbReadTable(con,"census")
capacity = dbReadTable(con,"capacity")
capacity = supplementStadia(capacity)
attendance = dbReadTable(con,"attendance")

