Feature: Magnetosphere Storm Event
  As a Starlink engineer,
  I want to send an alert to starlink satellites to engage thrusters,
  So they do not suffer accelerated orbital decay.

  Scenario Outline: Magnetosphere Storm Event
    Given the Intensity of solar wind has been logged
    And  the Magnetosphere bx_gsm coordinate has been negative

    Then At least 1 storm exists from the last interval
    And the storm database is not empty

    Then I log the intensity of the storm for future research
    And I alert all satellites to engage their thrusters

    Examples:
      |  |

