Feature: Add tax rates

    Scenario: Create tax rates with valid JWT token and valid data
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "second_tax",
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        }
    }
    """
    Then the response status code should be 201
    And the response should contain:
    | status  | true                          |
    | message | "Taxes added successfully"    |

    Scenario: Create tax rates with invalid JWT token
    Given I have an API endpoint "/taxes/create"
    And I have an invalid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "second_tax",
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        }
    }
    """
    Then the response status code should be 401
    And the response should contain:
    | status  | false                          |
    | message | "Signature verification failed" |

    Scenario: Create tax rates without a JWT token
    Given I have an API endpoint "/taxes/create"
    And I do not provide a JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "second_tax",
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        }
    }
    """
    Then the response status code should be 401
    And the response should contain:
    | status  | false                          |
    | message | "Invalid authorization header" |

    Scenario: Create tax rates with empty request body
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with an empty JSON body:
    """
    {}
    """
    Then the response status code should be 400
    And the response should contain:
    | status  | false                                   |
    | message | "Validation Error"                     |
    | error   | [{"name": ["This field is required."]}] |

    Scenario: Create tax rates with extra fields in the body
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "second_tax",
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        },
        "extra_field": 100
    }
    """
    Then the response status code should be 400
    And the response should contain:
    | status  | false                                |
    | message | "Invalid field: extra_field"         |

    Scenario: Create tax rates with invalid name field
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": null,
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        }
    }
    """
    Then the response status code should be 400
    And the response should contain:
    | status  | false                                   |
    | message | "Validation Error"                     |
    | error   | [{"name": ["This field may not be null."]}] |

    Scenario: Create tax rates with name field exceeding 100 characters
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "A".repeat(101),
        "total_tax": 0,
        "taxSplits": {
            "cgst": 0.0,
            "sgst": 0.0
        }
    }
    """
    Then the response status code should be 400
    And the response should contain:
    | status  | false                                                    |
    | message | "Validation Error"                                       |
    | error   | [{"name": ["Ensure this field has no more than 100 characters."]}] |

    Scenario: Create tax rates with valid taxSplits key-value pairs
    Given I have an API endpoint "/taxes/create"
    And I have a valid JWT token
    When I send a POST request with the following JSON body:
    """
    {
        "name": "second_tax",
        "total_tax": 0,
        "taxSplits": {
            "cgst": 5.0,
            "sgst": 5.0
        }
    }
    """
    Then the response status code should be 201
    And the response should contain:
    | status  | true                          |
    | message | "Taxes added successfully"    |
