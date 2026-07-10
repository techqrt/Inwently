Feature: Create Employee API

  Scenario: Create an employee with valid JWT token and valid data
    Given I have the API endpoint "/employees/create/"
    And I have a valid JWT token "valid.jwt.token" to create employee
    When I send a POST request to create employee with the following JSON body
      """
      {
        "name": "Alan Roy",
        "mobile_number": "123560890",
        "alternate_mobile_number":"7435371001",
        "dob": "2024-11-10",
        "shop_access": ["adminshop"],
        "email_id": "Alanr.roy@example.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "permissions": {
          "master": {
            "item": true,
            "shop": true,
            "supplier": true,
            "customer": true,
            "create": true,
            "employee": true
          },
          "inventory": {
            "inventory": true
          },
          "billing": {
            "bill_history": true,
            "pos": true,
            "return_item": true
          },
          "reports": {
            "overview": true,
            "general": true,
            "administration": true,
            "day_book": true,
            "gst": true
          },
          "printer_templates": {
            "printer_templates": true
          },
          "dashboard": {
            "dashboard": true
          },
          "stock": {
            "stock": true,
            "purchase_list": true,
            "return_purchase": true
          },
          "quotations": {
            "quotations": true
          }
         }
        }
      """
    Then the response status code to create employee should be 201
    And the response to create employee should contain
      | status | message                       |
      | true   | Employee created successfully |

  Scenario: Create an employee with missing required fields
    Given I have the API endpoint "/employees/create/"
    And I have a valid JWT token "valid.jwt.token" to create employee
    When I send a POST request to create employee with missing required fields
      """
      {}
      """
    Then the create response status code with missing required fields should be 400
    And the create response with missing required fields should contain
      | status | message            |
      | false  | Validation Error   |

  Scenario: Create an employee with invalid mobile number format
    Given I have the API endpoint "/employees/create/"
    And I have a valid JWT token "valid.jwt.token" to create employee
    When I send a POST request to create employee with invalid mobile number
      """
      {
        "name": "Jane Doe",
        "mobile_number": "invalid_mobile",
        "dob": "2024-11-10",
        "shop_access": ["shop_1"],
        "email_id": "jane.doe@example.com",
        "state": "",
        "country": "",
        "street": "",
        "permissions": {}
      }
      """
    Then the create response status code with invalid phone number should be 400
    And the create response with invalid phone number should contain
      | status | message          |
      | false  | Validation Error |

  Scenario: Create an employee without JWT token
    Given I have the API endpoint "/employees/create/"
    When I send a POST request to create employee without an authorization token with the following JSON body
      """
      {
        "name": "John Doe",
        "mobile_number": "1234567890",
        "dob": "2024-11-10",
        "shop_access": ["shop_1", "shop_2"],
        "email_id": "john.doe@example.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "permissions": {}
      }
      """
    Then the create response status code without an authorization token should be 401
    And the create response without an authorization token should contain
      | status | message            |
      | false  | Authentication Error |

  Scenario: Create an employee with invalid JWT token
    Given I have the API endpoint "/employees/create/"
    And I have an invalid JWT token "invalid.jwt.token" to create employee
    When I send a POST request to create employee with invalid token with the following JSON body
      """
      {
        "name": "John Doe",
        "mobile_number": "1234567890",
        "dob": "2024-11-10",
        "shop_access": ["shop_1", "shop_2"],
        "email_id": "john.doe@example.com",
        "state": "California",
        "country": "USA",
        "street": "123 Main St",
        "profile_photo_url": "http://example.com/photo.jpg",
        "permissions": {}
      }
      """
    Then the create response status code with invalid token should be 401
    And the create response with invalid token should contain
      | status | message            |
      | false  | Authentication Error |

  Scenario: Create an employee with invalid email ID format
    Given I have the API endpoint "/employees/create/"
    And I have a valid JWT token "valid.jwt.token" to create employee
    When I send a POST request to create employee with invalid email id with the following JSON body
      """
      {
        "name": "Alice Smith",
        "mobile_number": "9876543210",
        "dob": "2024-11-10",
        "shop_access": ["shop_1"],
        "email_id": "invalid_email_format",
        "state": "New York",
        "country": "USA",
        "street": "456 Elm St",
        "permissions": {}
      }
      """
    Then the create response status code with invalid email id should be 400
    And the create response with invalid email should contain
      | status | message          |
      | false  | Validation Error |

  Scenario: Create an employee without providing permissions
    Given I have the API endpoint "/employees/create/"
    And I have a valid JWT token "valid.jwt.token" to create employee
    When I send a POST request to create employee without permissions with the following JSON body
      """
      {
        "name": "Charlie Brown",
        "mobile_number": "5551234567",
        "dob": "2024-11-10",
        "shop_access": ["shop_1"],
        "email_id": "charlie.brown@example.com",
        "state": "Texas",
        "country": "USA",
        "street": "789 Pine St"
      }
      """
    Then the create response status code without permissions should be 400
    And the create response without permissions should contain
      | status | message          |
      | false  | Validation Error |
