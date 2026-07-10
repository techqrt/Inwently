Feature: Add a Brand

  Scenario: Create a Brand with a valid JWT token and valid data
    When scenario 1 I send a POST request with a valid JWT token and the following JSON body
      """
      {
          "name": "cafe"
      }
      """
    Then scenario 1 the response status code should be 201
    And scenario 1 response should contain:
      | status  | true                       |
      | message | "Brand added successfully" |

  Scenario: Create a Brand with invalid or missing authentication
    When scenario 2 I send a POST request with an invalid JWT token and the proper JSON body
    Then scenario 2 the response status code should be 401
    And scenario 2 response should contain:
      | status  | false                     |
      | message | "<message>"               |
      | error   | ["<error>"]               |



  Scenario: Create a Brand with a valid name
    When scenario 3 I send a POST request with the following JSON body:
      """
      {
          "name": "cloud cafe"
      }
      """
    Then scenario 3 the response status code should be 201
    And scenario 3 response should contain:
      | status  | true                       |
      | message | "Brand added successfully" |

  Scenario: Create a Brand with invalid or missing name
    When scenario 4 I send a POST request with the following JSON body:
      """
      {
          "name": null
      }
      """
    Then scenario 4 the response status code should be 400
    And scenario 4 response should contain:
      | status  | false       |
      | message | "Validation Error" |
      | error   | <error>     |