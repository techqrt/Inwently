# Created by josep at 24-10-2024
@admin_workflow
Feature: Admin accesses and manages services
  # This feature describes the workflow and permission verification of an admin user accessing services

  Background:
    Given Prepare all endpoints, admin username, and password
    And Admin successfully logs in at /auth/login and retrieves an access token
    And Decode the access token to confirm all permissions are set to true

  @shop_management
  Scenario: Admin performs CRUD operations on shops
    When Admin creates 4 shops via /shops/create endpoint and verifies each response has a 200 status code
    Then Verify /shops/get_all returns a 200 status code and matches the Swagger schema
    And Admin retrieves a shop by shop_code using /shops/get, confirming 200 status and schema accuracy
    And Admin searches shops via /shops/search, confirming 200 status and schema accuracy with Swagger
    And Admin deletes a single shop by shop_code via /shops/delete with a 200 status code in response
    And Admin deletes multiple shops by providing shop_codes via /shops/delete_many with a 200 status code

  @employee_management
  Scenario: Admin performs CRUD operations on employees
    When Admin retrieves employee details via /employees/get, using employee_code from access token with a 200 status code
    Then Verify /employees/get_all endpoint returns a 200 status code and matches Swagger schema
    And Admin searches employees with /employees/search, confirming 200 status and schema validity
    And Admin creates 2 new admins via /employees/create and checks each returns a 200 status code
    And Admin updates parameters of the first employee via /employees/update and verifies the 200 response
    And Admin deletes a specific employee via /employees/delete using employee_code
    And Admin deletes multiple employees using /employees/delete_many with a 200 response code
