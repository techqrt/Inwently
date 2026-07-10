Feature: Update a Category

    Scenario: Update a Category with valid JWT token and valid data
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "personal"
        }
        """
        Then the response status code should be 200
        And the response should contain:
        | status  | true                              |
        | message | "Category updated successfully"   |

    Scenario: Update a Category with invalid JWT token
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "personal"
        }
        """
        Then the response status code should be 401
        And the response should contain:
        | status  | false                            |
        | message | "Signature verification failed"  |
        | error   | ["Signature verification failed"] |

    Scenario: Update a Category without JWT token
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "personal"
        }
        """
        Then the response status code should be 401
        And the response should contain:
        | status  | false                            |
        | message | "Invalid authorization header"   |
        | error   | ["Invalid authorization header"] |

    Scenario: Update a Category with random text as JWT token
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "personal"
        }
        """
        Then the response status code should be 401
        And the response should contain:
        | status  | false                                                                                             |
        | message | "Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"   |
        | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"] |

    Scenario: Update a Category with empty body
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            // empty body
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"category_code": ["This field is required."], "name": ["This field is required."]}] |

    Scenario: Update a Category without required field category code
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"category_code": ["This field is required."]}] |

    Scenario: Update a Category without required field name
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_9"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"name": ["This field is required."]}] |

    Scenario: Update a Category with extra fields in body
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "personal",
            "location": "chalakudy"
        }
        """
        Then the response status code should be 200
        And the response should contain:
        | status  | true                              |
        | message | "Category updated successfully"   |

    Scenario: Update a Category with wrong category code
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8002",
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                              |
        | message | "Value Error No matching category found" |
        | error   | ["No matching category found"]     |

    Scenario: Update a Category with name exceeding 100 characters
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8002",
            "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                                      |
        | message | "Validation Error"                                         |
        | error   | [{"name": ["Ensure this field has no more than 100 characters."]}] |

    Scenario: Update a Category with name value as null
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8002",
            "name": null
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"name": ["This field may not be null."]}] |

    Scenario: Update a Category with name as empty
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8002",
            "name": ""
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"name": ["This field may not be blank."]}] |

    Scenario: Update a Category name with value as a integer
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": 0
        }
        """
        Then the response status code should be 200
        And the response should contain:
        | status  | true                              |
        | message | "Category updated successfully"   |

    Scenario: Update a Category name with value as special characters
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8",
            "name": "!??"
        }
        """
        Then the response status code should be 200
        And the response should contain:
        | status  | true                              |
        | message | "Category updated successfully"   |

    Scenario: Update a Category name with value not as a valid string
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "T_8002",
            "name": []
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"name": ["Not a valid string."]}]    |

    Scenario: Update a Category with category code value as null
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": null,
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"category_code": ["This field may not be null."]}] |

    Scenario: Update a Category with category code as empty
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "",
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"category_code": ["This field may not be blank."]}] |

    Scenario: Update a Category with category code value as a integer
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": 0,
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                              |
        | message | "Value Error No matching category found" |
        | error   | ["No matching category found"]     |

    Scenario: Update a Category with category code value as special characters
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": "!??",
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                              |
        | message | "Value Error No matching category found" |
        | error   | ["No matching category found"]     |

    Scenario: Update a Category with category code value not as a valid string
        Given I have a API endpoint "/category/update/"
        When I send a PUT request with following JSON body:
        """
        {
            "category_code": [],
            "name": "personal"
        }
        """
        Then the response status code should be 400
        And the response should contain:
        | status  | false                                   |
        | message | "Validation Error"                     |
        | error   | [{"category_code": ["Not a valid string."]}] |
