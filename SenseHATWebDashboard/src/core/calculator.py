# -*- coding: utf-8 -*-
"""Core calculation functions for the Sense HAT dashboard."""

# This is a globally accepted average and is suitable as a default.
SEA_LEVEL_PRESSURE_HPA: float = 1013.25
# Reason for change: Moved the magic number for sea level pressure into a named constant
# for better readability and to clarify its meaning.


def pressure_to_altitude(
    pressure: float, sea_level_pressure: float = SEA_LEVEL_PRESSURE_HPA
) -> float:
    """Converts atmospheric pressure to altitude using the barometric formula.

    This formula provides an approximation of altitude based on pressure readings.
    It assumes a standard atmospheric model.

    Args:
        pressure: The current atmospheric pressure in hectopascals (hPa).
        sea_level_pressure: The atmospheric pressure at sea level in hPa.
                            Defaults to the standard average.

    Returns:
        The estimated altitude in meters.

    Raises:
        ValueError: If pressure is non-positive.
    """
    if pressure <= 0:
        raise ValueError("Pressure must be a positive value.")

    # The calculation logic remains unchanged as per the requirements.
    # The formula is 44330 * (1 - (P/P0)^(1/5.255)), where P is pressure and P0 is sea level pressure.
    return 44330.0 * (1.0 - (pressure / sea_level_pressure) ** (1.0 / 5.255))
