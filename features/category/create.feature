Feature: Category API

  Scenario: Create a Category with a valid JWT token and valid data
    When scenario 1 category I send a POST request with a valid JWT token and the following JSON body
      """
      {
          "name": "Electronics"
      }
      """
    Then scenario 1 category the response status code should be 201
    And scenario 1 category response should contain:
      | status  | true                          |
      | message | "Category added successfully" |

  Scenario: Create a Category with invalid or missing authentication
    When scenario 2 category I send a POST request with an invalid JWT token and the proper JSON body
    Then scenario 2 category the response status code should be 401
    And scenario 2 category response should contain:
      | status  | false                    |
      | message | "<message>"               |
      | error   | ["<error>"]               |

  Scenario: Create a Category with an invalid or missing name
    When scenario 3 category I send a POST request with the following JSON body:
      """
      {
          "name": null
      }
      """
    Then scenario 3 category the response status code should be 400
    And scenario 3 response should contain:
      | status  | false               |
      | message | "Validation Error"   |
      | error   | <error>              |

#
#  Scenario: Create a Category with valid JWT token and valid data
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "sports"
#    }
#    """
#    Then the response status code should be 201
#    And the response should contain:
#      | status  | true                          |
#      | message | "Category added successfully" |
#
#  Scenario: Create a Category with invalid JWT token
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "sports"
#    }
#    """
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                                     |
#      | message | "'NoneType' object is not subscriptable"  |
#      | error   | ["'NoneType' object is not subscriptable"]|
#
#  Scenario: Create a Category without JWT token
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "sports"
#    }
#    """
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                          |
#      | message | "Invalid authorization header" |
#      | error   | ["Invalid authorization header"]|
#
#  Scenario: Create a Category with random text as JWT token
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "sports"
#    }
#    """
#    Then the response status code should be 401
#    And the response should contain:
#      | status  | false                                                                                             |
#      | message | "Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"   |
#      | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"] |
#
#  Scenario: Create a Category with empty body
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      //empty body
#    }
#    """
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                   |
#      | message | "Validation Error"                     |
#      | error   | [{"name": ["This field is required."]}] |
#
#  Scenario: Create a Category with extra field in body
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "entertainment",
#      "color": "red"
#    }
#    """
#    Then the response status code should be 201
#    And the response should contain:
#      | status  | true                          |
#      | message | "Category added successfully" |
#
#  Scenario: Create a Category with name exceeding 100 characters
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
#    }
#    """
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                                     |
#      | message | "Validation Error"                                        |
#      | error   | [{"name": ["Ensure this field has no more than 100 characters."]}] |
#
#  Scenario: Create a Category with empty name
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": ""
#    }
#    """
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                   |
#      | message | "Validation Error"                     |
#      | error   | [{"name": ["This field may not be blank."]}] |
#
#  Scenario: Create a Category with name as null value
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": null
#    }
#    """
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                                   |
#      | message | "Validation Error"                     |
#      | error   | [{"name": ["This field may not be null."]}] |
#
#  Scenario: Create a Category with name as integer
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": 0
#    }
#    """
#    Then the response status code should be 201
#    And the response should contain:
#      | status  | true                          |
#      | message | "Category added successfully" |
#
#  Scenario: Create a Category with name as array
#    Given I have an API endpoint "/category/brand"
#    When I send a POST request with the following JSON body:
#    """
#    {
#      "name": []
#    }
#    """
#    Then the response status code should be 400
#    And the response should contain:
#      | status  | false                        |
#      | message | "Validation Error"           |
#      | error   | [{"name": ["Not a valid string."]}] |
