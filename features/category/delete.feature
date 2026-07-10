Feature: Delete a Category

  Scenario: Delete a Category with valid data
    When scenario 1 category I send a DELETE request with a valid JWT token and the following JSON body:
      """
      {
          "category_code": "CAT_123"
      }
      """
    Then scenario 1 category delete the response status code should be 200
    And scenario 1 category delete the response should contain:
      | status  | true                           |
      | message | "Category deleted successfully" |



#  Scenario: Delete a Category with valid JWT and valid data
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_6 |
#    Then the response status code should be 200
#    And the response should contain:
#      | status  | true                             |
#      | message | "Category delete successfully"   |
#
#  Scenario: Delete a Category with invalid JWT token
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_6 |
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                                      |
#      | message | "'NoneType' object is not subscriptable"   |
#      | error   | ["'NoneType' object is not subscriptable"] |
#
#  Scenario: Delete a Category without JWT token
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_6 |
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                            |
#      | message | "Invalid authorization header"   |
#      | error   | ["Invalid authorization header"] |
#
#  Scenario: Delete a Category with random text as JWT token
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_6 |
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                                                                                             |
#      | message | "Invalid header string: 'utf-8' codec can't decode byte 0x86 in position 0: invalid start byte"   |
#      | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x86 in position 0: invalid start byte"] |
#
#  Scenario: Delete a Category with wrong category code
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_100 |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                              |
#      | message | "Value Error No matching category found" |
#      | error   | ["No matching category found"]     |
#
#  Scenario: Delete a Category without required parameters
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request without parameters
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                   |
#      | message | "Validation Error"                     |
#      | error   | [{"category_code": ["This field is required."]}] |
#
#  Scenario: Delete a Category with extra parameters
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | T_6 |
#      | name          | A   |
#    Then the response status code should be 200
#    And the response should contain:
#      | status  | true                             |
#      | message | "Category delete successfully"   |
#
#  Scenario: Delete a Category with category code value as empty
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code |  |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                   |
#      | message | "Validation Error"                     |
#      | error   | [{"category_code": ["This field may not be blank."]}] |
#
#  Scenario: Delete a Category with category code value as integer
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | 0 |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                              |
#      | message | "Value Error No matching category found" |
#      | error   | ["No matching category found"]     |
#
#  Scenario: Delete a Category with category code value as special characters
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | !? |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                              |
#      | message | "Value Error No matching category found" |
#      | error   | ["No matching category found"]     |
#
#  Scenario: Delete a Category with category code value exceeding 10 digits
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                              |
#      | message | "Value Error No matching category found" |
#      | error   | ["No matching category found"]     |
#
#  Scenario: Delete a Category with category code value as invalid data type other than integer
#    Given I have an API endpoint "/category/create/"
#    When I send a DELETE request with the following parameters:
#      | category_code | [] |
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                              |
#      | message | "Value Error No matching category found" |
#      | error   | ["No matching category found"]     |
