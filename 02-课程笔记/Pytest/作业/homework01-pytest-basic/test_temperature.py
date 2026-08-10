from temperature import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius
)


def test_celsius_to_fahrenheit():

    result = celsius_to_fahrenheit(0)

    assert result == 32



def test_fahrenheit_to_celsius():

    result = fahrenheit_to_celsius(32)

    assert result == 0