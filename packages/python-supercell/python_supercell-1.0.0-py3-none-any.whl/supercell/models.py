"""
Various Models.
"""
# Standard Library
import datetime
import random
from typing import Dict, Optional, Union

# Third Party Code
from dateutil.parser import parse
from dateutil.tz import tzutc


class Forecast(object):
    """
    A forecast.
    """
    identifier: int

    def __init__(self,
                 forecast_for_date: Union[datetime.date, str],
                 forecast_for_utc_offset_seconds: int,
                 forecast_made_datetime: Union[datetime.datetime, str],
                 temperature_min: float,
                 temperature_max: float,
                 longitude: float,
                 latitude: float,
                 identifier: Optional[int] = None) -> None:

        if isinstance(forecast_for_date, datetime.date):
            self.forecast_for_date = forecast_for_date
        elif isinstance(forecast_for_date, str):
            self.forecast_for_date = parse(forecast_for_date)

        self.forecast_for_utc_offset_seconds = int(
            forecast_for_utc_offset_seconds)

        if isinstance(forecast_made_datetime, datetime.datetime):
            self.forecast_made_datetime = forecast_made_datetime
        elif isinstance(forecast_made_datetime, str):
            self.forecast_made_datetime = parse(forecast_made_datetime)

        self.temperature_min = temperature_min and float(temperature_min) or None
        self.temperature_max = temperature_max and float(temperature_max) or None
        self.longitude = longitude
        self.latitude = latitude
        self.identifier = identifier or random.getrandbits(60)

    @property
    def forecast_made_date(self) -> datetime.date:
        """The date the forecast was made."""
        return self.forecast_made_datetime.date()

    @property
    def forecast_made_time(self) -> datetime.time:
        """The time the forecast was made"""
        return self.forecast_made_datetime.timetz()

    @property
    def forecast_made_year(self) -> int:
        """The year the forecast was made"""
        return self.forecast_made_date.year

    @property
    def forecast_made_month(self) -> int:
        """The month the forecast was made"""
        return self.forecast_made_date.month

    @property
    def forecast_made_day(self) -> int:
        """The day the forecast was made"""
        return self.forecast_made_date.day

    @property
    def forecast_made_hour(self) -> int:
        """The hour the forecast was made"""
        return self.forecast_made_time.hour

    @property
    def forecast_made_minute(self) -> int:
        """The minute the forecast was made"""
        return self.forecast_made_time.minute

    @property
    def forecast_made_utc_offset_seconds(self) -> int:
        """The UTC offset of the location where the forecast was made."""
        offset = self.forecast_made_datetime.utcoffset()
        if offset:
            return int(offset.total_seconds())
        return 0

    @property
    def forecast_for_year(self) -> int:
        """The year the forecast is for"""
        return self.forecast_for_date.year

    @property
    def forecast_for_month(self) -> int:
        """The month the forecast is for"""
        return self.forecast_for_date.month

    @property
    def forecast_for_day(self) -> int:
        """The day the forecast is for"""
        return self.forecast_for_date.day

    def to_dict(self) -> Dict:
        """A dictionary representation of the forecast"""
        return {
            "identifier": self.identifier,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "forecast_made_str": str(self.forecast_made_datetime),
            "forecast_made": self.forecast_made_datetime.timestamp(),
            "forecast_made_date": datetime.datetime(
                year=self.forecast_made_datetime.year,
                month=self.forecast_made_datetime.month,
                day=self.forecast_made_datetime.day,
                tzinfo=tzutc()
            ).timestamp(),
            "forecast_made_time": (self.forecast_made_datetime.hour * 100) + self.forecast_made_datetime.minute,
            "forecast_made_utc_offset_seconds": self.forecast_made_utc_offset_seconds,

            "forecast_for_date_str": self.forecast_for_date.strftime("%Y-%m-%d"),
            "forecast_for_date": datetime.datetime(
                year=self.forecast_for_date.year,
                month=self.forecast_for_date.month,
                day=self.forecast_for_date.day,
                tzinfo=tzutc()
            ).timestamp(),
            "forecast_for_utc_offset_seconds": self.forecast_for_utc_offset_seconds,

            "temperature_min": self.temperature_min and float(self.temperature_min) or None,
            "temperature_max": self.temperature_max and float(self.temperature_max) or None
        }


class Observation(object):
    """An observation."""

    identifier: int

    def __init__(self,
                 temperature: float,
                 humidity: float,
                 longitude: float,
                 latitude: float,
                 observed_at: str,
                 windchill: Optional[float] = None,
                 windspeed: Optional[float] = None,
                 pressure: Optional[float] = None,
                 windgust: Optional[float] = None,
                 identifier: Optional[int] = None) -> None:
        self.temperature = float(temperature)
        self.humidity = float(humidity)
        self.windchill = windchill and float(windchill) or None
        self.windspeed = windspeed and float(windspeed) or None
        self.pressure = pressure and float(pressure) or None
        self.windgust = windgust and float(windgust) or None
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.observed_at = parse(observed_at)
        self.identifier = identifier or random.getrandbits(60)

    @property
    def observed_at_utc_offset_seconds(self) -> int:
        """The UTC offset of the location where the observation happened."""
        offset = self.observed_at.utcoffset()
        if offset:
            return int(offset.total_seconds())
        return 0

    def to_dict(self) -> Dict:
        """A dictionary representation of the observation"""
        return {
            "identifier": self.identifier,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "observed_at_str": str(self.observed_at),
            "observed_at": self.observed_at.timestamp(),
            "observed_at_utc_offset_seconds": self.observed_at_utc_offset_seconds,
            "observed_at_date": datetime.datetime(
                year=self.observed_at.year,
                month=self.observed_at.month,
                day=self.observed_at.day,
                tzinfo=tzutc()
            ).timestamp(),
            "observed_at_time": (self.observed_at.time().hour * 100) + self.observed_at.time().minute,
            "temperature": self.temperature,
            "humidity": self.humidity,
        }
