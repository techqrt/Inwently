Feature: Delete Multiple Employees API

  Scenario: Delete multiple employees with valid JWT token and valid employee IDs
    Given I have the API endpoint "/employees/delete_many/"
    And Create 2 employees by calling employee create and note its employee code
    When I send a PATCH request with valid JWT Token and valid employee IDs
      """
      {
        "employee_code": ["E_1", "E_2", "E_3"]
      }
      """
    Then the delete many response status code with valid JWT Token should be 200
    And the delete many response with valid JWT Token should contain
      | status | message                       |
      | true   | "Employees deleted successfully" |

  Scenario: Delete multiple employees with invalid JWT token
    Given I have the API endpoint "/employees/delete_many/"
    And I have an invalid JWT token "invalid.jwt.token" to delete many employee
    When I send a PATCH request with invalid token with the following JSON body
      """
      {
        "employee_code": ["E_1", "E_2"]
      }
      """
    Then the delete many response status code with invalid token should be 401
    And the delete many response with invalid token should contain
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Delete multiple employees without JWT token
    Given I have the API endpoint "/employees/delete_many/"
    When I send a PATCH request without an authorization token with the following JSON body
      """
      {
        "employee_ids": ["E_1", "E_2"]
      }
      """
    Then the delete many response status code without an authorization token should be 401
    And the delete many response without an authorization token should contain
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Delete multiple employees with missing employee IDs in request body
    Given I have the API endpoint "/employees/delete_many/"
    And I have a valid JWT token "valid.jwt.token" to delete many employees
    When I send a PATCH request with missing employee IDs
      """
      {
        "employee_ids": []
      }
      """
    Then the delete many response status code with missing employee IDs should be 400
    And the delete many response response with missing employee IDs should contain
      | status | message                       |
      | false  | "Validation Error" |

  Scenario: Delete multiple employees with invalid employee ID format
    Given I have the API endpoint "/employees/delete_many/"
    And I have a valid JWT token "valid.jwt.token" to delete many employees
    When I send a PATCH request with invalid employee ID
      """
      {
        "employee_ids": ["invalid_id", "another_invalid_id"]
      }
      """
    Then the delete many response status code with invalid employee ID should be 400
    And the delete many response with invalid employee ID should contain
      | status | message                                   | error                      |
      | false  | "Value Error No matching employee found"  | No matching employee found    |

  Scenario: Attempt to delete employees with no employee IDs provided
    Given I have the API endpoint "/employees/delete_many/"
    And I have a valid JWT token "valid.jwt.token" to delete many employees
    When I send a PATCH request without any JSON body
    Then the delete many response status code with no employee IDs should be 400
    And the delete many response with no employee IDs should contain
      | status | message            | error|
      | false  | "Validation Error" |{ "employee_code": [  "This field is required."  ]  } |
