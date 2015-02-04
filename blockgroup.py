blockgroup.data = function(token, state = "*", county = "*", blockgroup = "*", variables, year = 2010, survey = "sf1"){
  state = as.character(state)
  county = as.character(county)
  blockgroup = as.character(blockgroup)
  year = as.character(year)
  variables = paste(variables, collapse = ",")

  if(state == "*"){
    state = process.api.data(fromJSON(file=url(
      paste("http://api.census.gov/data/2000/sf3?key=", token,"&get=P001001&for=state:*", sep = ""))))$state
  }

  if(county == "*"){
    mycounties = sapply(state, get.counties, token = token)
    #mystates = expand.states(mycounties)
    my.url = matrix(paste("http://api.census.gov/data/", year, "/", survey , "?key=", token,
                          "&get=",variables,"&for=block+group:*&in=state:", state,
                          "+county:", unlist(mycounties), sep = ""),ncol = 1)
  }else{
    mycounties = list(county)
    names(mycounties) = state
    mystates = expand.states(mycounties)
    my.url = matrix(paste("http://api.census.gov/data/", year, "/", survey, "?key=", token,
                          "&get=",variables,"&for=block+group:*&in=state:", unlist(mystates),
                          "+county:", unlist(mycounties), sep = ""),ncol = 1)
  }

  process.url = apply(my.url, 1, function(x) process.api.data(fromJSON(file=url(x))))
  rbind.dat = data.frame(rbindlist(process.url))
  rbind.dat = rbind.dat[, c(tail(seq_len(ncol(rbind.dat)), 4), seq_len(ncol(rbind.dat) - 4))]
  rbind.dat
}