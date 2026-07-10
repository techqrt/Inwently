Feature: Search a category

    Scenario: Search a category with valid JWT token and valid key
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
        Then the response status code should be 200
        And the response should contain:
          | status  | true                                    |
          | message | "Data fetched successfully"            |
          | data    | {"data": [{"name": "sweet", "categoryCode": "T_14"}, {"name": "spicy", "categoryCode": "T_15"}], "presentPage": 1, "totalPage": 1, "totalCount": 2} |
    

    Scenario: Search a category with invalid JWT token 
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
        Then the response status code should be 401
        And the response should contain:
          | status  | false                      |
          | message | "Signature verification failed" |
          | error   | ["Signature verification failed"] |

    
    Scenario: Search a category without JWT token
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
        Then the response status code should be 401
        And the response should contain:
          | status  | false                           |
          | message | "Invalid authorization header"  |
          | error   | ["Invalid authorization header"] |


    Scenario: Search a category with random text as  JWT token
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
        Then the response status code should be 401
        And the response should contain:   
          | status  | false                                                                 |
          | message | "Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte" |
          | error   | ["Invalid header string: 'utf-8' codec can't decode byte 0x85 in position 0: invalid start byte"] |

    Scenario: Search a category without required parameters
        Given I have a API endpoint "/category/search"
        When I send a GET request without required parameters
        Then the response status code should be 400
        And the response should contain:
          | status  | false                                                                 |
          | message | Validation Error                                                      |
          | error   | [ { key: [ This field is required. ] } ]                              |
    
    Scenario: Search a category with value of key empty
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key |  |
        Then the response status code should be 400
        And the response should contain:
          | status  | false                                                                 |
          | message | Validation Error                                                      |
          | error   | [ { key: [ This field may not be blank. ] } ]                         |

    Scenario: Search a category with value of key empty
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key |  |
        Then the response status code should be 400
        And the response should contain:
          | status  | false                                                                 |
          | message | Validation Error                                                      |
          | error   | [ { key: [ This field may not be blank. ] } ]                         |


    Scenario: Search a category with wrong value for key
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | helloworld |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [], presentPage: 1, totalPage: 0, totalCount: 0 }             |



    Scenario: Search a category with integer value for key
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | 0 |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [], presentPage: 1, totalPage: 0, totalCount: 0 }             |

    Scenario: Search a category with integer value for key
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | 0 |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [], presentPage: 1, totalPage: 0, totalCount: 0 }             |

  Scenario: Search a category with key value as question mark 
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | ? |
        Then the response status code should be 400
        And the response should contain:
          | status  | false                                                                 |
          | message | Validation Error                                                      |
          | error   | [ { key: [ This field may not be blank. ] } ]                         |


    Scenario: Search a category with key value as special characters
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | !#*? |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [], presentPage: 1, totalPage: 0, totalCount: 0 }             |


  Scenario: Search a category with key value as equal to sign
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | = |
        Then the response status code should be 400
        And the response should contain:
          | status  | false                                                                 |
          | message | Validation Error                                                      |
          | error   | [ { key: [ This field may not be blank. ] } ]                         |

     Scenario: Search a category with a limit value
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
          |limit| 1 |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [ { name: sweet, categoryCode: T_14 } ], presentPage: 1, totalPage: 2, totalCount: 2, nextPageUrl: http://api.caddayn.in/category/search/?key=s&limit=1&pageNum=2 } |
    

     Scenario: Search a category with a limit value as zero
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
          |limit| 0 |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                           |
          | message  | Exception Error division by zero|
          | error    | [ Database Error ]              |


    Scenario: Search a category with limit parameter empty 
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
          |limit|   |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                          |
          | message  | Validation Error                               |
          | error    | [ { limit: [ A valid integer is required. ] } ]|



    Scenario: Search a category with limit value as string
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
          |limit| "" |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                      |
          | message  | Validation Error                               |
          | error    | [ { limit: [ A valid integer is required. ] } ]|


    Scenario: Search a category with special characters as limit value
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key | s |
          |limit| !? |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                                                 |
          | message  | Validation Error                                                      |
          | error    | [ { limit: [ A valid integer is required. ] } ]                       |

    Scenario: Search a category with page number
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s |
          |limit   | 1 |
          |page_num| 2 |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [ { name: spicy, categoryCode: T_15 } ], presentPage: 2, totalPage: 2, totalCount: 2 } |

    Scenario: Search a category with page number parameter empty
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s |
          |limit   | 1 |
          |page_num|   |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                                                 |
          | message  | Validation Error                                                      |
          | error    | [ { page_num: [ A valid integer is required. ] } ]                    |

    Scenario: Search a category with page number parameter value as string
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s  |
          |limit   | 1  |
          |page_num| "" |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                                                 |
          | message  | Validation Error                                                      |
          | error    | [ { page_num: [ A valid integer is required. ] } ]                    |

    Scenario: Search a category with page number parameter value as special characters
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s  |
          |limit   | 1  |
          |page_num| !?? |
        Then the response status code should be 400
        And the response should contain:
          | status   | false                                                                 |
          | message  | Validation Error                                                      |
          | error    | [ { page_num: [ A valid integer is required. ] } ]                    |

    Scenario: Search a category with page number parameter value as zero
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s  |
          |limit   | 1  |
          |page_num| 0  |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [], presentPage: 0, totalPage: 2, totalCount: 2, nextPageUrl: http://api.caddayn.in/category/search/?key=s&limit=1&page_num=0&pageNum=1 } |
          
    Scenario: Search a category with extra parameters
        Given I have a API endpoint "/category/search"
        When I send a GET request with following parameters:
          | key    | s  |
          |limit   | 1  |
          |page_num| 1  |
          |id      | 5  |
        Then the response status code should be 200
        And the response should contain:
          | status   | true                                                                  |
          | message  | Data fetched successfully                                             |
          | data     | { data: [ { name: sweet, categoryCode: T_14 } ], presentPage: 1, totalPage: 2, totalCount: 2, nextPageUrl: http://api.caddayn.in/category/search/?key=s&limit=1&page_num=1&id=5&pageNum=2 } |
