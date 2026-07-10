Feature: Get All Brands API

  Scenario: Get all brands with valid JWT token
    When Scenario 1 call the get all api with a GET request with query parameters:
      | limit      | 20                |
      | page_num   | 1                 |
      | sort_by    | name              |
      | sort_order  | asc              |
    Then Scenario 1 the response status code should be 200
    And Scenario 1 the response should contain following pattern:
      | status |  true                      |
      | message| "Brands retrieved successfully" |
      | data   | { "presentPage": 1, "totalPage": 1, "totalCount": 1, "data": [{"name": "Brand A", "categoryCode": "CAT_1"}] } |

#  Scenario: Get all brands without JWT token
#    Given I have the API endpoint "/brand/get_all/"
#    When I send a GET request without an authorization token
#    Then the response status code should be 401
#    And the response should contain:
#      | status | false                       |
#      | message| "Authentication Error"    |
#
#  Scenario: Get all brands with invalid JWT token
#    Given I have the API endpoint "/brand/get_all/"
#    And I have an invalid JWT token "invalid.jwt.token"
#    When I send a GET request with query parameters:
#      | limit      | 20                |
#      | page_num   | 1                 |
#    Then the response status code should be 401
#    And the response should contain:
#      | status | message                       |
#      | false  | "Authentication Error"        |
#
#  Scenario: Get all brands with missing required query parameters
#    Given I have the API endpoint "/brand/get_all/"
#    And I have a valid JWT token "valid.jwt.token"
#    When I send a GET request without any query parameters
#    Then the response status code should be 200
#    And the response should contain the below information:
#      | status |  true                      |
#      | message  | "Missing required parameters" |
#      | data   | { "presentPage": 1, "totalPage": 1, "totalCount": 1, "data": [] } |
#
#  Scenario: Get all brands with invalid limit value
#    Given I have the API endpoint "/brand/get_all/"
#    And I have a valid JWT token "valid.jwt.token"
#    When I send a GET request with query parameters:
#      | limit      | invalid_value       |
#      | page_num   | 1                   |
#    Then the response status code should be 400
#    And the response should contain:
#      | status | false                    |
#      |  message | "Validation Error"     |
#
#  Scenario: Get all brands with negative page number
#    Given I have the API endpoint "/brand/get_all/"
#    And I have a valid JWT token "valid.jwt.token"
#    When I send a GET request with query parameters:
#      | limit      | 20                |
#      | page_num   | -1                |
#      | sort_by    | name              |
#      | sort_order  | asc              |
#    Then the response status code should be 400
#    And the response should contain:
#      | status | false                    |
#      |  message | "Validation Error"     |
