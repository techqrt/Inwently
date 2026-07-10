Feature: Delete multiple brands

    Scenario: Delete many brands using a valid JWT token and valid body
      When scenario 1 I send a PATCH request with valid jwt token and the following JSON body
      Then scenario 1 delete many the response status code should be 200
      And scenario 1 delete many the response should contain:
        | status  | true                        |
        | message | "Brand delete successfully" |
#
#    Scenario: Delete many brands using an invalid JWT token
#      Given I have an API endpoint "/brand/delete_many"
#      When I send a PATCH request with the following JSON body:
#        """
#        {
#          "brand_code": [
#            "T_15",
#            "T_14"
#          ]
#        }
#        """
#      Then the response status code should be 401
#      And the response should contain:
#        | status  | false                                      |
#        | message | "'NoneType' object is not subscriptable"   |
#        | error   | ["'NoneType' object is not subscriptable"] |
#
#    Scenario: Delete many brands without a JWT token
#      Given I have an API endpoint "/brand/delete_many"
#      When I send a PATCH request with the following JSON body:
#        """
#        {
#          "brand_code": [
#            "T_15",
#            "T_14"
#          ]
#        }
#        """
#      Then the response status code should be 401
#      And the response should contain:
#        | status  | false                          |
#        | message | "Invalid authorization header" |
#        | error   | ["Invalid authorization header"] |
#
#    Scenario: Delete many brands with random text as token
#      Given I have an API endpoint "/brand/delete_many"
#      When I send a PATCH request with the following JSON body:
#        """
#        {
#          "brand_code": [
#            "T_15",
#            "T_14"
#          ]
#        }
#        """
#      Then the response status code should be 401
#      And the response should contain:
#        | status  | false                                                                                             |
#        | message | "Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 3: invalid start byte"   |
#        | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 3: invalid start byte"] |
#
#    Scenario: Delete many brands without brand code
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#          """
#          {
#            "brand_code": []
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                        |
#          | message | "Exception Error 'brand_id'" |
#          | error   | ["Database Error"]           |
#
#    Scenario: Delete many brands with empty JSON body
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#          """
#          {
#            // empyt body
#          }
#          """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                   |
#          | message | "Validation Error"                     |
#          | error   | [{"brand_code": ["This field is required."]}]
#    Scenario: Delete many brand with extra fields in JSON body
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#        """
#        {
#        "brand_code":[
#            "T_2",
#            "T_3"
#        ],
#        "name":[
#            "lulu2",
#            "lulu3"
#        ]
#        }
#        """
#        Then the response status code should be 200
#        And the response should contain:
#          | status  | true                        |
#          | message | "Brand delete successfully"
#    Scenario: Delete many Brand with brand code containing integer
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#        """
#        {
#            "brand_code":[
#                0,
#                1
#            ]
#        }
#        """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |
#
#    Scenario: Delete many Brand with brand code list consisting null value
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#        """
#        {
#            "brand_code":[
#                "T_26",
#                null
#            ]
#        }
#        """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |
#
#    Scenario: Delete many Brand with brand code list consisting special characters
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#        """
#        {
#            "brand_code":[
#                "!##"
#            ]
#        }
#        """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |
#
#
#
#    Scenario: Delete many Brand with brand code list consisting wrong brand_code
#        Given I have an API endpoint "/brand/delete_many"
#        When I send a PATCH request with the following JSON body:
#        """
#        {
#            "brand_code":[
#                "T_26",
#                "T_100"
#            ]
#        }
#        """
#        Then the response status code should be 400
#        And the response should contain:
#          | status  | false                                 |
#          | message | "Value Error No matching brand found" |
#          | error   | ["No matching brand found"]           |