Feature: Update a Brand

    Scenario: Update a Brand using valid JWT token and valid data
        When scenario 1 I send a PUT request with a valid jwt token and the following JSON body:
          """
          {
            "brand_code": "T_26",
            "name": "cloud cocktails"
          }
          """
        Then scenario 1 update the response status code should be 200
        And scenario 1 update the response should contain:
          | status  | true                          |
          | message | "Brand updated successfully"  |

#    Scenario: Update a Brand using invalid JWT token
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_26",
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                            |
#          | message | "Signature verification failed"  |
#          | error   | ["Signature verification failed"] |
#
#    Scenario: Update a Brand without JWT token
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_26",
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                            |
#          | message | "Invalid authorization header"   |
#          | error   | ["Invalid authorization header"] |
#
#    Scenario: Update a Brand with random text as JWT token
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_26",
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                                                                                             |
#          | message | "Invalid header string: 'utf-8' codec can't decode byte 0xb1 in position 0: invalid start byte"   |
#          | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0xb1 in position 0: invalid start byte"] |
#
#    Scenario: Update a Brand without required fields
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            // empty body
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field is required."], "name": ["This field is required."]}] |
#
#    Scenario: Update a Brand with wrong brand code
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_300",
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                              |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]        |
#
#    Scenario: Update a Brand with wrong brand code data type
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": 0,
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 401
#        And the response should contain:
#          | status  | false                              |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]        |
#
#    Scenario: Update a Brand with empty brand code
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "",
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field may not be blank."]}] |
#
#    Scenario: Update a Brand without brand code
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "name": "cloud cocktails"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field may not be blank."]}] |
#
#    Scenario: Update a Brand without name
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_25"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"name": ["This field is required."]}] |
#
#    Scenario: Update a Brand with empty name
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_15",
#            "name": ""
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"name": ["This field may not be blank."]}] |
#
#    Scenario: Update a Brand with name exceeding 100 characters
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_25",
#            "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                                     |
#          | message | "Validation Error"                                        |
#          | error   | [{"name": ["Ensure this field has no more than 100 characters."]}] |
#
#    Scenario: Update a Brand with brand code exceeding 10 characters
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_252342342432423424",
#            "name": "Makers restaurant"
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                                                 |
#          | message | "Validation Error"                                                   |
#          | error   | [{"brand_code": ["Ensure this field has no more than 10 characters."]}] |
#
#    Scenario: Update a Brand name as an integer
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_26",
#            "name": 0
#          }
#          """
#        Then the response status code should be 200
#        And the response should contain:
#          | status  | true                          |
#          | message | "Brand updated successfully"  |
#
#    Scenario: Update a Brand with wrong data type other than integer in name
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#          """
#          {
#            "brand_code": "T_26",
#            "name": []
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                        |
#          | message | "Validation Error"           |
#          | error   | [{"name": ["Not a valid string."]}] |
#
#    Scenario: Update a Brand with wrong data type other than integer in brand code
#        Given I have an API endpoint "/brand/update"
#        When I send a PUT request with the following JSON body:
#        """
#        {
#            "brand_code": [],
#            "name": "cloud cocktails"
#        }
#        """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                        |
#          | message | "Validation Error"           |
#          | error   | [{"brand_code": ["Not a valid string."]}] |
