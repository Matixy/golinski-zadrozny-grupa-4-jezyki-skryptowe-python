def getTeamLen(teamMembers):
  """funkcja zwracająca liczbę członków zespołu"""
  return len(teamMembers)

def getGreeting(teamName, teamMembers):
  """funkcja formatującą powitanie"""
  greenColor: str = "\033[32m"
  resetColor: str = "\033[0m"
  
  text: str = f"{greenColor}Witamy w repozytorium zespołu: {teamName}, aktualna liczba członków: {getTeamLen(teamMembers)}{resetColor}"
  
  return text
  