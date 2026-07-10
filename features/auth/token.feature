## Created by josep at 16-10-2024
#Feature: /auth/token/ functionality testing
#  # Enter feature description here
#
#  Scenario: generating new token based on real token
#    Given call login api with correct username and password
#      When Call the token endpoint with recived refresh token after login
#      Then Check the response status is 200 and return type is dict
#      And the response body should contain the keys "access_token"
#
#  Scenario: false token validation
#    Given create a jwt token manually
#      When Call the token endpoint with created token
#      Then Check the response status is 401 and return type is dict
#      And the response body should not contain the keys "access_token"
#      And the response body should contain the message key and Authentication Error message
#
#  Scenario: false token validation with correct payload
#    Given create a jwt token manually with correct payload
#      When Call the token endpoint with created token contain correct payload
#      Then Check the response after calling token api with status is 401 and return type is dict
#      And the response body should not contain the keys "access_token" and return type should be dict
#      And the response body should contain the message key and Authentication Error message with status, mesage and erros as keys