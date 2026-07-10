Feature: Search Employees API

  Scenario: Search employees with valid JWT token and valid search key
    Given I have the API endpoint "/employees/search/"
    And I have a valid JWT token "valid.jwt.token" to search employees
    When I send a GET request with query parameters with key admin
      | key         | admin             |
      | limit       | 20               |
      | page_num    | 1                |
    Then the search response status code with valid search key should be 200
    And the search response with valid search key should contain data fetched successfully
      | status | message                       |
      | true   | "Data fetched successfully"   |
      | data   | [ {"name": "admin", "mobileNumber": " ", "isActive": true, "employeeCode": "T_1", "dob": "2020-01-01", "profilePhotoUrl": ""} ] |

  Scenario: Search employees with valid JWT token and no search key
    Given I have the API endpoint "/employees/search/"
    And I have a valid JWT token "valid.jwt.token" to search employees
    When I send a GET request with query parameters without key
      | limit       | 20               |
      | page_num    | 1                |
    Then the search response status code with no search key should be 400
    And the search response with no search key should contain validation error
      | status | message                       |
      | false  | "Validation Error" |

  Scenario: Search employees with invalid JWT token
    Given I have the API endpoint "/employees/search/"
    And I have an invalid JWT token "invalid.jwt.token" to search employees
    When I send a GET request with query parameters key john
      | key         | John             |
      | limit       | 20               |
      | page_num    | 1                |
    Then the response status with invalid jwt token code should be 401
    And the search response with invalid jwt token should contain authentication error
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Search employees without JWT token
    Given I have the API endpoint "/employees/search/"
    When I send a GET request without an authorization token
    Then the response status code without jwt token should be 401
    And the search response without jwt token should contain authentication error
      | status | message                       |
      | false  | "Authentication Error"        |

  Scenario: Search employees with invalid limit value
    Given I have the API endpoint "/employees/search/"
    And I have a valid JWT token "valid.jwt.token" to search employees
    When I send a GET request with query parameters limit invalid_value
      | key         | John             |
      | limit       | invalid_value     |
      | page_num    | 1                |
    Then the search response status code for invalid limit value should be 400
    And the search response for invalid limit value should contain validation error
      | status | message                       |
      | false  | "Validation Error"     |

  Scenario: Search employees with negative page number
    Given I have the API endpoint "/employees/search/"
    And I have a valid JWT token "valid.jwt.token" to search employees
    When I send a GET request with query parameters page_num -1
      | key         | admin             |
      | limit       | 20               |
      | page_num    | -1               |
    Then the search response status for negative page number code should be 400
    And the search response for negative page number should contain validation error
      | status | message                       |
      | false  | "Validation Error"     |

  Scenario: Search employees with unsupported sorting order
    Given I have the API endpoint "/employees/search/"
    And I have a valid JWT token "valid.jwt.token" to search employees
    When I send a GET request with query parameters sort_order unsupported
      | key         | admin             |
      | limit       | 20               |
      | page_num    | 1                |
      | sort_order  | unsupported       |
      | sort_key  | unsupported       |
    Then the search response status code for unsupported sorting order should be 400
    And the search response for unsupported sorting order should contain validation error
      | status | message                       |
      | false  | "Validation Error"     |
