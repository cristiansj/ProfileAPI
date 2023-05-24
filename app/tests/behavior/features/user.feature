Feature: User Management

  Scenario: Get user information with valid token
    Given an authenticated user
    When the user requests their own information
    Then the user details should be returned

  Scenario: Get user information with invalid token
    Given an invalid token
    When the user requests their own information
    Then an error message should be returned

  Scenario: Update user information with valid token
    Given an authenticated user
    When the user updates their information
    Then the user details should be updated

  Scenario: Update user information with invalid token
    Given an invalid token
    When the user updates their information
    Then an error message should be returned

  Scenario: Delete user with valid token
    Given an authenticated user
    When the user deletes their account
    Then the user should be deleted

  Scenario: Delete user with invalid token
    Given an invalid token
    When the user deletes their account
    Then an error message should be returned