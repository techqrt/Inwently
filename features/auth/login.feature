Feature: /auth/login/ functionality testing

  Scenario: Trying to login with correct username and password
     Given Prepare the username and password for login api
      When Call the login api endpoint with given username and password
      Then Check the response status is 200
      And the response content type should be dict
      And the response body should contain the keys "access_token" and "refresh_token"

  Scenario: Trying to login with incorrect username and password
     Given Prepare an incorrect username and password for login api
      When Call the login api endpoint with given incorrect username and password
      Then Check the response status is 400
      And the response body should contain an error message

  Scenario: Trying to login with incorrect username alone
     Given Prepare an incorrect username  for login api
      When Call the login api endpoint with given incorrect username
      Then Check the response status is 400 for incorrect username alone
      And the response body should contain an error message with status false and with mesage key

#  Scenario: Trying to login with incorrect password alone
#     Given Prepare an incorrect password for login api
#      When Call the login api endpoint with given incorrect password
#      Then Check the response status is 400 for incorrect password alone
#      And the response body should contain an error message with status false and with the mesage key