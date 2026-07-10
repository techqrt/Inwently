Feature: Retrieve Employee Details

  Scenario Outline: Retrieve employee details with specified fields
    Given I have the API endpoint "/employees/get/"
    And I have the employee code "employee_code"
    And I specify the expected response fields as "value"
    When I send a GET request to retrieve employees with specified fields to the endpoint
    Then the get response with specified field status should be 200
    And the get response with specified field should contain the field "status" with the value true
    And the get response with specified field should contain the field "message" with a string
    And the get response with specified field should contain the "data" object with specified fields
    And the get response with specified field "data" object should contain the "permissions" structure with appropriate permissions

    Examples:
      | employee_code | value                                                                                     |
      | E1234         | ["name", "mobileNumber", "dob", "emailId", "permissions"]                                |
      | E5678         | ["state", "country", "street", "organisationName", "profile_photo_url", "employeeCode"]  |

  Scenario: Retrieve employee details with all available fields
    Given I have the API endpoint "/employees/get/"
    And I have the employee code "xxxx"
    And I specify the expected response fields as empty so all fields should be returned
    When I send a GET request to the endpoint
    Then the get response with all available fields status code should be 200
    And the get response with all available fields should contain the field "status" with the value true
    And the get response with all available fields should contain the field "message" with a string
    And the get response with all available fields should contain all fields in the "data" object including
      | name              |
      | mobileNumber      |
      | dob               |
      | state             |
      | country           |
      | street            |
      | organisationName  |
      | isActive          |
      | emailId           |
      | emailVerified     |
      | profile_photo_url |
      | employeeCode      |
    And the get response with all available fields "permissions" structure should include
      | master          |
      | inventory       |
      | billing         |
      | reports         |
      | printer_templates |
      | dashboard       |
      | stock           |
      | quotations      |

  Scenario: Retrieve employee details with non-existing employee code
    Given I have the API endpoint "/employees/get/"
    And I use a non-existing employee code "E0000"
    And I specify no expected response fields
    When I send a GET request to the endpoint with non-existing employee code
    Then the get response status with non-existing employee code should be 400
    And the get response with non-existing employee code should contain the field "status" with the value false
    And the get response with non-existing employee code should contain the field "message" with the value "Value Error No matching employee found"
    And the get response with non-existing employee code should contain an "error" field with the message
      | No matching employee found |

  Scenario: Retrieve employee details without providing an employee code
    Given I have the API endpoint "/employees/get/"
    And I do not provide an employee code
    When I send a GET request to the endpoint without employee code
    Then the get response without employee code status should be 400
    And the get response without employee code should contain the field "status" with the value false
    And the get response without employee code should contain the field "message" with the value "Validation Error"
    And the get response without employee code should contain an "error" field with the following structure
      | employee_code | This field is required. |

  Scenario: Retrieve employee details with invalid employee code format
    Given I have the API endpoint "/employees/get/"
    And I use an invalid employee code "!@#123"
    When I send a GET request to the endpoint with invalid employee code format
    Then the get response with invalid employee code status should be 400
    And the get response with invalid employee code should contain the field "status" with the value false
    And the get response with invalid employee code should contain the field "message" with the value "Validation Error"
    And the get response with invalid employee code should contain an "error" field with the following structure
      | No matching employee found |

  Scenario: Retrieve employee details with an empty employee code
    Given I have the API endpoint "/employees/get/"
    And I set the employee code as an empty string
    When I send a GET request to the endpoint with empty employee code
    Then the response status with empty employee code should be 400
    And the get response with empty employee code should contain the field "status" with the value false
    And the get response with empty employee code should contain the field "message" with the value "Validation Error"
    And the get response with empty employee code should contain an "error" field with the following structure
      | employee_code | This field may not be blank. |
#
#  Scenario: Retrieve employee details with a false values parameter
#    Given I have the API endpoint "/employees/get/"
#    And I set the values parameter to "names,named"
#    When I send a GET request to the endpoint
#    Then the response status should be 400
#    And the response should contain the field "status" with the value false
#    And the response should contain the field "message" with the value "Value Error named not a proper column names"
#    And the response should contain an "error" field with the following structure:
#      | error | named not a proper column names |

  Scenario: Call "/employees/get/" api with wrong jwt token in header
    Given create jwt token manualy for employees get api
      When Call the employees get api with wrong jwt token
      Then Check the response of employees get status with invalid jwt token is 401 and should be a dict type
      And the get response content with wrong jwt token should contain Authentication Error message

  Scenario: Call "/employees/get/" api with no jwt token in header
    Given Prepare a employee code 'T_1' to call get api
      When Call the employees get api with given employee code
      Then Check the response of employees get status with no jwt token is 401 and should be a dict type
      And the get response content with no jwt token should contain Authentication Error message