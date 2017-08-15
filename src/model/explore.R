library(RSQLite)
library(ggplot2)
library(dplyr)

StadiaTest = function() {
  leagues = c("NHL","MLB","NFL","NBA")
  for(league in leagues) {
    league_cap = capacity %>%
      filter(League == league) %>%
      select(Capacity, Team, Stadium)
    
    league_tbl = attendance %>% 
      filter(League == league) %>%
      select(Avg.Home,Total.Home,Team,Stadium,Year)
    
    league_merge = left_join(league_tbl, league_cap, "Stadium", all = TRUE)
    print(paste0(league," is: ",!any(is.na(league_merge))))
  }
}

StadiaTest()
