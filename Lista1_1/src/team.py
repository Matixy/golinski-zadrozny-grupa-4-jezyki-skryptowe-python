def getTeamLen(teamMembers):
  """funkcja zwracająca liczbę członków zespołu"""
  return len(teamMembers)

def getGreeting(teamName, teamMembers):
  """funkcja formatującą powitanie"""
  greenColor: str = "\033[32m"
  resetColor: str = "\033[0m"
  
  text: str = f"{greenColor}Witamy w repozytorium zespołu: {teamName}, aktualna liczba członków: {getTeamLen(teamMembers)}{resetColor}"
  
  return text

def displayTeamInformation(teamName, teamMembers):
  """funkcja wyświetlająca dane w uporządkowanej formie"""
  print("\n" + f"+"*50)
  print(f"Nazwa Zespołu: {teamName.upper()}\n")
  print("Skład:")

  for member in teamMembers:
    print(member)

  print("+" * 50)


if __name__ == '__main__':
  teamName = "Golinski & Zadrozny Team"
  teamMembers = ["Pawel Golinski", "Mateusz Zadrozny"]

  print(getGreeting(teamName, teamMembers))
  displayTeamInformation(teamName, teamMembers)
  print("\nProjekt został uruchomiony poprawnie!")