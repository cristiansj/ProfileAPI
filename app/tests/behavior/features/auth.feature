Feature: Testing login endpoint

  Scenario: User login
    Given the API is running
    When I send a POST request to "/login" with the following data:
      | username  | testuser  |
      | password  | password  |
    Then the response status code should be 200
    And the response body should contain a "token" field
