Feature: Update Employee API

  Scenario: Update an employee with valid JWT token and valid data
    Given I have the API endpoint "/employees/update/"
    And I have a valid JWT token "valid\.jwt\.token" to update employees
    When I send a PUT request with the following JSON body
      """
      {
        "employee_id": "E_1",
        "name": "John Doe Updated",
        "mobile_number": "1234567890",
        "dob": "2024-11-10",
        "shop_access": ["shop_1", "shop_2"],
        "email_id": "john.doe.updated@example.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St Updated",
        "profile_photo_url": "",
        "permissions": {
          "master": {
            "item": true,
            "shop": true,
            "supplier": true,
            "customer": true,
            "create": true,
            "employee": true
          },
          // Other permissions omitted for brevity
        }
      }
      """
    Then the update response status code for valid data should be 200
    And the update response should contain employee updated successfully
      | status | message                       |
      | true   | "Employee updated successfully" |

  Scenario: Update an employee with missing employee ID
    Given I have the API endpoint "/employees/update/"
    And I have a valid JWT token "valid.jwt.token"
    When I send a PUT request with the following JSON body with employee_code missing
      """
      {
        // Missing employee_code
        "name": "Jane Doe Updated",
        // Other fields omitted for brevity
      }
      """
    Then the update response status code for missing employee_code should be 400
    And the update response for missing employee_code should contain Validation error
      | status | message                       |
      | false  | "Validation Error" |

  Scenario: Update an employee with invalid email ID format
    Given I have the API endpoint "/employees/update/"
    And I have a valid JWT token "valid.jwt.token"
    When I send a PUT request with the following JSON body with invalid email ID format
      """
      {
        "employee_id": "E_1",
        "name": "Alice Smith Updated",
        "mobile_number": "9876543210",
        "dob": "2024-11-10",
        "shop_access": ["shop_1"],
        "email_id": "invalid_email_format",  # Invalid email format
        // Other fields omitted for brevity
      }
      """
    Then the update response status code for invalid email ID format should be 400
    And the update response for invalid email ID format should contain
      | status | message                       |
      | false  | "Validation Error"       |

  Scenario: Update an employee without JWT token
    Given I have the API endpoint "/employees/update/"
    When I send a PUT request with the following JSON body with valid data but without Jwt Token
      """
      {
        "employee_id": "E_1",
        // Valid data as above but missing token
      }
      """
    Then the update response status code without jwt token should be 401
    And the update response without jwt token should contain
      | status | message                       |
      | false  | "Authentication Error"       |

  Scenario: Update an employee with invalid JWT token
    Given I have the API endpoint "/employees/update/"
    And I have an invalid JWT token "invalid.jwt.token"
    When I send a PUT request with the following JSON body with valid data but invalid token
      """
      {
        "employee_id": "E_1",
        // Valid data as above but invalid token
      }
      """
    Then the update response status code for invalid JWT Token should be 401
    And the update response for invalid JWT Token should contain
      | status | message                       |
      | false  | "Authentication Error"       |
