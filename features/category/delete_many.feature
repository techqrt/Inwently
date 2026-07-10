Feature: Delete multiple category

  Scenario: Delete multiple category with valid JWT token and valid data
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_7",
        "T_4"
      ]
    }
    """
    Then the response status code should be 200
    And the response should contain:
      | status  | true                             |
      | message | "Category delete successfully"   |

  Scenario: Delete multiple category with invalid JWT token
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_7",
        "T_4"
      ]
    }
    """
    Then the response status code should be 401
    And the response should contain:
      | status  | false                                      |
      | message | "'NoneType' object is not subscriptable"   |
      | error   | ["'NoneType' object is not subscriptable"] |

  Scenario: Delete multiple category without JWT token 
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_7",
        "T_4"
      ]
    }
    """
    Then the response status code should be 401
    And the response should contain:
      | status  | false                            |
      | message | "Invalid authorization header"   |
      | error   | ["Invalid authorization header"] |

  Scenario: Delete multiple category with random text as JWT token
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_7",
        "T_4"
      ]
    }
    """
    Then the response status code should be 401
    And the response should contain:
      | status  | false                                                                                             |
      | message | "Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"   |
      | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"] |

  Scenario: Delete multiple category with empty body
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      //empty body
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                                   |
      | message | "Validation Error"                     |
      | error   | [{"category_code": ["This field is required."]}] |

  Scenario: Delete multiple category with category code list empty
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": []
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                   |
      | message | "Exception Error 'category_id'" |
      | error   | ["Database Error"]      |

  Scenario: Delete multiple category with extra fields in body
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_11",
        "T_12"
      ],
      "names": [
        "sports",
        "education"
      ]
    }
    """
    Then the response status code should be 200
    And the response should contain:
      | status  | true                             |
      | message | "Category delete successfully"   |

  Scenario: Delete multiple category with wrong category codes
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_11",
        "T_12"
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |

  Scenario: Delete multiple category with null in category codes
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_11",
        null
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |

  Scenario: Delete multiple category with category codes exceeding 10 digits
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "T_1335345345353535",
        "T_1335345345353232111"
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |

  Scenario: Delete multiple category with integer in category codes 
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        1,
        2
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |

  Scenario: Delete multiple category with special characters in category codes 
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        "?",
        "!"
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |

  Scenario: Delete multiple category with invalid data types in category codes 
    Given I have an API endpoint "/category/delete_many/"
    When I send a PATCH request with the following JSON body:
    """
    {
      "category_code": [
        [],
        {}
      ]
    }
    """
    Then the response status code should be 400
    And the response should contain:
      | status  | false                              |
      | message | "Value Error No matching category found" |
      | error   | ["No matching category found"]     |
