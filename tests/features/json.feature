Feature: Dump a model to valid json
    In order to serialize my model
    As a Booby framework user
    I want to dump my model to json

    Scenario: Basic model
        Given I have an User model
        When I create an User instance with the user data
        And I dump the object using the json module
        Then I get a string with the json