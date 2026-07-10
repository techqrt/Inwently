Feature: Delete Employee API

  Scenario: Delete an employee with valid JWT token and valid employee ID
    Given Create an employee by calling employee create api
    And I have a valid JWT token "valid.jwt.token" to delete employee
    When I send a DELETE request with valid Jwt Token with query parameters
      | employee_id | E_1             |
    Then the delete response status code with valid Jwt Token should be 200
    And the delete response with valid Jwt Token should contain
      | status | message                       |
      | true   | "Employee deleted successfully" |

  Scenario: Delete an employee with invalid JWT token
    Given I have the API endpoint "/employees/delete/"
    And I have an invalid JWT token "invalid.jwt.token" to delete employee
    When I send a DELETE request with invalid Jwt Token with query parameters
      | employee_id | E_1             |
    Then the delete response status code with invalid Jwt Token should be 401
    And the delete response with invalid Jwt Token should contain
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Delete an employee without JWT token
    Given I have the API endpoint "/employees/delete/"
    When I send a DELETE request without an authorization token with query parameters
      | employee_id | E_1             |
    Then the delete response status code without authorization Token should be 401
    And the delete response without authorization Token should contain
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Attempt to delete an employee with missing employee ID
    Given I have the API endpoint "/employees/delete/"
    And I have a valid JWT token "valid.jwt.token" to delete employee
    When I send a DELETE request without query parameters
    Then the delete response status code without query parameters should be 400
    And the delete response without query parameters should contain
      | status | message            | error|
      | false  | "Validation Error" |{ "employee_code": [ "This field is required."  ] } |

  Scenario: Attempt to delete an employee with invalid employee ID format
    Given I have the API endpoint "/employees/delete/"
    And I have a valid JWT token "valid.jwt.token" to delete employee
    When I send a DELETE request with invalid employee id
      | employee_id | invalid_id       |
    Then the delete response status code with invalid employee id should be 400
    And the delete response with invalid employee id should contain
      | status | message               |
      | false  | "Employee not Found"  |
