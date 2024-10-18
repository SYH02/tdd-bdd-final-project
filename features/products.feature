Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description     | price   | available | category   |
        | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field

Scenario: User reads a product successfully

    Given I am on the home page
    When I enter "Hat" in the name field
    And I click the "Search" button
    Then I should see a success message
    When I copy the ID of the first product
    And I clear the name field
    And I paste the copied ID into the name field
    And I click the "Retrieve" button
    Then I should see a success message
    And the product name should be "Hat"
    And the product description should be "A red fedora"
    And the product availability should be "True"
    And the product category should be "Clothes"
    And the product price should be "59.95"

Scenario: User successfully updates a product
    Given I am on the home page
    When I enter "Hat" in the name field
    And I click the "Search" button
    Then I should see a success message
    And I should see a product with the name "Hat"

    When I click the "Edit" button for the first product
    And I change the name to "Fedora"
    And I click the "Save" button
    Then I should see a success message

    When I clear the search field
    And I enter "Fedora" in the name field
    And I click the "Search" button
    Then I should see a success message
    And I should see "Fedora" in the search results
    And I should not see "Hat" in the search results

Scenario: User successfully deletes a product

    Given I am on the home page
    When I enter "Hat" in the name field
    And I click the "Search" button
    Then I should see a success message
    And I should see a product with the name "Hat"

    When I click the "Delete" button for the first product
    Then I should see a message indicating successful deletion

    When I clear the search field
    And I enter "Hat" in the name field
    And I click the "Search" button
    Then I should see a success message
    And I should not see any products in the search results


Scenario: User lists all products successfully

    Given I am on the home page
    When I clear the search field
    And I click the "Search" button
    Then I should see a success message
    And I should see "Hat" in the search results
    And I should see "Shoes" in the search results
    And I should see "Big Mac" in the search results
    And I should see "Sheets" in the search results



Scenario: User successfully filters products by category

    Given I am on the home page
    When I clear the search field
    And I select "Food" in the category dropdown
    And I click the "Search" button
    Then I should see a success message
    And I should see "Big Mac" in the search results
    And I should not see "Hat" in the search results
    And I should not see "Shoes" in the search results
    And I should not see "Sheets" in the search results



Scenario: User successfully filters products by availability

    Given I am on the home page
    When I clear the search field
    And I select "Available" in the availability dropdown
    And I click the "Search" button
    Then I should see a success message
    And I should see "Hat" in the search results
    And I should see "Big Mac" in the search results
    And I should see "Sheets" in the search results
    And I should not see "Shoes" in the search results


Scenario: User successfully searches for a product by name

    Given I am on the home page
    When I enter "Hat" in the name field
    And I click the "Search" button
    Then I should see a success message
    And I should see "Hat" in the results
    And I should see "A red fedora" in the description field


