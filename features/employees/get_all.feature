# Created by josep at 30-09-2024
Feature: /employees/get_all/ functionality testing
  test results of get all api of employees

  Scenario: Call get all api without parameters
    Given A sample response is present in folder steps/common/sample_response/employees_get_all json
      When Call the employees get_all api
      Then Check the response of employees get_all status is 200
      And the response content type should be dict for employees get_all
      And the response body should contain the keys mentioned in employees_get_all json file without next page url

  Scenario: Call get all api without parameters with wrong jwt token in header
    Given create jwt token manualy for employees get all api
      When Call the employees get_all api with wrong jwt token
      Then Check the response of employees get_all status is 401 and should be a dict type
      And the response content should contain Authentication Error message

  Scenario: Get all employees with invalid query parameter scenario 1
    Given I have the API endpoint "/employees/get_all/"
    When I send a GET request with query parameters with scenario 1
      | limit    | -1     |
      | page_num | 0                |
      | sort_by  | name             |
      | sort_order| unknown          |
    Then the get response status code should be 400
    And the get response should contain value error
      | status | message                       |
      | false  | "Value Error The given page number is greater than maximum available limit"     |

  Scenario: Get all employees with invalid query parameter scenario 2
    Given I have the API endpoint "/employees/get_all/"
    When I send a GET request with query parameters with scenario 2
      | limit    | 1     |
      | page_num | 0                |
      | sort_by  | name             |
      | sort_order| unknown          |
    Then the get response status code should be 400
    And the get response should contain exception error
      | status | message                       |
      | false  | "Exception Error That page number is less than 1"     |

  Scenario: Get all employees with unsupported sorting order
    Given I have the API endpoint "/employees/get_all/"
    And I have a valid JWT token "valid.jwt.token"
    When I send a GET request with query parameters
      | limit        | 20               |
      | page_num     | 1                |
      | sort_by      | name             |
      | sort_order   | unsupported       |
    Then the get response status code should be 400
    And the get response should contain validation error
      | status | message                       |
      | false  | "Validation Error"     |