Feature: User Authentication

  Scenario: User login with valid credentials
    Given a user with username "testuser" and password "password"
    When the user logs in with username and password
    Then a token should be returned

  Scenario: User login with invalid credentials
    Given a user with username "testuser" and password "password"
    When the user logs in with invalid username or password
    Then an error message should be returned