from Lista1_1.src.team import getTeamLen, getGreeting

def test_team_length():
    """Test sprawdza funkcję zwracającą liczbę członków"""
    members = ["Paweł", "Mateusz"]
    assert getTeamLen(members) == 2
    print("Test getTeamLen: PASSED")

def test_greeting_format():
    """Test sprawdza funkcję formatującą powitanie"""
    result = getGreeting("Aura", ["Pawel"])
    assert "Aura" in result
    assert "1" in result
    print("Test getGreeting: PASSED")

if __name__ == "__main__":
    test_team_length()
    test_greeting_format()