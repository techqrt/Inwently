Feature: Delete a Brand

    Scenario: Delete a Brand with valid data
        When scenario 1 I send a DELETE request with valid jwt the following query parameters
        Then scenario 1 the response status code should be 200
        And scenario 1 the response should contain:
          | status  | true                        |
          | message | "Brand delete successfully" |
#
#    Scenario: Delete a Brand with invalid JWT token
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | T_22 |
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                                      |
#          | message | "'NoneType' object is not subscriptable"   |
#          | error   | ["'NoneType' object is not subscriptable"] |
#
#    Scenario: Delete a Brand without a token
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | T_22 |
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                          |
#          | message | "Invalid authorization header" |
#          | error   | ["Invalid authorization header"]|
#
#    Scenario: Delete a Brand with random text as token
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | T_22 |
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                                                                                             |
#          | message | "Invalid header string: 'utf-8' codec can't decode byte 0xb1 in position 0: invalid start byte"   |
#          | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0xb1 in position 0: invalid start byte"] |
#
#    Scenario: Delete a Brand with brand code as blank
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code |  |
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                  |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field may not be blank."]}]|
#
#    Scenario: Delete a Brand with wrong brand code
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | t_2 |
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |
#
#    Scenario: Delete a Brand with brand code containing integer
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | 0 |
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |
#
#    Scenario: Delete a Brand with brand code containing special characters
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | ?#@ |
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                  |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field may not be blank."]}]|
#
#    Scenario: Delete a Brand with brand code value exceeding 10 characters
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                                                  |
#          | message | "Validation Error"                                                     |
#          | error   | [{"brand_code": ["Ensure this field has no more than 10 characters."]}]|
#
#    Scenario: Delete a Brand with extra parameters
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | T_10      |
#          | name       | cloud cafe |
#        Then the response status code should be 200
#        And the response should contain:
#          | status  | true                        |
#          | message | "Brand delete successfully" |
#
#    Scenario: Delete a Brand with no parameters
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with no query parameters
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                      |
#          | message | "Validation Error"                         |
#          | error   | [{"brand_code": ["This field is required."]}]|
#
#    Scenario: Delete a Brand with valid brand code and invalid body
#        Given I have the API endpoint "/brand/delete/"
#        When I send a DELETE request with the following query parameters:
#          | brand_code | T_13 |
#        And with the following JSON body:
#          """
#          {
#              "brand_code": "T_13"
#          }
#          """
#        Then the response status code should be 200
#        And the response should contain:
#          | status  | true                        |
#          | message | "Brand delete successfully" |
