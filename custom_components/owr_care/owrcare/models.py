"""Models for OWRCare."""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import Any

from awesomeversion import AwesomeVersion

from .exceptions import OWRCareError
import json


class BodyRange(IntEnum):
    """Enumeration representing body range from OWRCare."""

    OUT = 0
    IN = 1

class BodyPresence(IntEnum):
    """Enumeration representing body presence from OWRCare."""

    NOBODY = 0
    SOMEBODY = 1

class BodyMovement(IntEnum):
    """Enumeration representing body movement from OWRCare."""

    NONE = 0
    STATIC = 1
    ACTIVE = 2

@dataclass
class BodyLocation:
    """Object holding body location state in OWRCare."""

    x: int
    y: int
    z: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> BodyLocation:
        """Return Body Location object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Body Location object.
        """
        return BodyLocation(
            x=data.get("x"),
            y=data.get("y"),
            z=data.get("z"),
        )

@dataclass
class Body:
    """Object holding body state in OWRCare."""

    range: BodyRange
    presence: BodyPresence
    energy: int
    movement: BodyMovement
    distance: int
    location: BodyLocation

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Body:
        """Return Body object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Body object.
        """
        return Body(
            range=BodyRange(data.get("range")),
            presence=BodyPresence(data.get("presence")),
            energy=data.get("energy"),
            movement=BodyMovement(data.get("movement")),
            distance=data.get("distance"),
            location=BodyLocation.from_dict(data.get("location")),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Body:
        # print(json.dumps(data, indent=4))
        if _range := data.get("range"):
            self.range = BodyRange(_range)
        if _presence := data.get("presence"):
            self.presence = BodyPresence(_presence)
        if _energy := data.get("energy"):
            self.energy = _energy
        if _movement := data.get("movement"):
            self.movement = BodyMovement(_movement)
        if _distance := data.get("distance"):
            self.distance = _distance
        if _location := data.get("location"):
            self.location = BodyLocation.from_dict(_location)

        return self


@dataclass
class Wave:
    """Object holding wave state in OWRCare."""

    w0: int
    w1: int
    w2: int
    w3: int
    w4: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Wave:
        """Return Wave object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Wave object.
        """
        return Wave(
            w0=data.get("w0"),
            w1=data.get("w1"),
            w2=data.get("w2"),
            w3=data.get("w3"),
            w4=data.get("w4"),
        )

@dataclass
class Heart:
    """Object holding heart state in OWRCare."""

    rate: int
    waves: Wave

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Heart:
        """Return Heart object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Heart object.
        """
        return Heart(
            rate=data.get("rate"),
            waves=Wave.from_dict(data.get("waves")),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Heart:
        if _rate := data.get("rate"):
            self.rate = _rate
        if _waves := data.get("waves"):
            self.waves = Wave.from_dict(_waves)

        return self


class BreathInfo(IntEnum):
    """Enumeration representing breath info from OWRCare."""

    UNSET = 0
    NORMAL = 1
    TOO_HIGH = 2
    TOO_LOW = 3
    NONE = 4

@dataclass
class Breath:
    """Object holding breath state in OWRCare."""

    info: BreathInfo
    rate: int
    waves: Wave

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Breath:
        """Return Breath object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Breath object.
        """
        return Breath(
            info=BreathInfo(data.get("info")),
            rate=data.get("rate"),
            waves=Wave.from_dict(data.get("waves")),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Breath:
        if _info := data.get("info"):
            self.info = BreathInfo(_info)
        if _rate := data.get("rate"):
            self.rate = _rate
        if _waves := data.get("waves"):
            self.waves = Wave.from_dict(_waves)

        return self


class SleepAway(IntEnum):
    """Enumeration representing sleep away from OWRCare."""

    OUT = 0
    IN = 1
    ACTIVE = 2

class SleepStatus(IntEnum):
    """Enumeration representing sleep status from OWRCare."""

    DEEP = 0
    LIGHT = 1
    AWAKE = 2
    NONE = 3

class SleepException(IntEnum):
    """Enumeration representing sleep exception from OWRCare."""

    LESS_4HOUR = 0
    MORE_12HOUR = 1
    LONG_TIME = 2
    NONE = 3

class SleepRating(IntEnum):
    """Enumeration representing sleep rating from OWRCare."""

    NONE = 0
    GOOD = 1
    MEDIAN = 2
    BAD = 3

class SleepStruggle(IntEnum):
    """Enumeration representing sleep struggle from OWRCare."""

    NONE = 0
    NORMAL = 1
    ABNORMAL = 2

class SleepNobody(IntEnum):
    """Enumeration representing sleep nobody from OWRCare."""

    NONE = 0
    NORMAL = 1
    ABNORMAL = 2

@dataclass
class SleepOverview:
    """Object holding sleep overview state in OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A sleep overview object.
    """

    presence: BodyPresence
    status: SleepStatus
    breath: int
    heart: int
    turn: int
    leratio: int
    seratio: int
    pause: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SleepOverview:
        """Return SleepOverview object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An SleepOverview object.
        """
        return SleepOverview(
            presence=BodyPresence(data.get("presence")),
            status=SleepStatus(data.get("status")),
            heart=data.get("heart"),
            breath=data.get("breath"),
            turn=data.get("turn"),
            leratio=data.get("leratio"),
            seratio=data.get("seratio"),
            pause=data.get("pause"),
        )

@dataclass
class SleepQuality:
    """Object holding sleep quality state in OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A sleep quality object.
    """

    score: int
    duration: int
    awake: int
    light: int
    deep: int
    aduration: int
    away: int
    turn: int
    breath: int
    heart: int
    pause: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SleepQuality:
        """Return SleepQuality object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An SleepQuality object.
        """
        return SleepQuality(
            score=data.get("score"),
            duration=data.get("duration"),
            awake=data.get("awake"),
            light=data.get("light"),
            deep=data.get("deep"),
            aduration=data.get("aduration"),
            away=data.get("away"),
            turn=data.get("turn"),
            breath=data.get("breath"),
            heart=data.get("heart"),
            pause=data.get("pause"),
        )

@dataclass
class Sleep:
    """Object holding sleep state in OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A sleep object.
    """

    away: SleepAway
    status: SleepStatus
    awake: int
    light: int
    deep: int
    score: int
    overview: SleepOverview
    quality: SleepQuality
    exception: SleepException
    rating: SleepRating
    struggle: SleepStruggle
    nobody: SleepNobody

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Sleep:
        """Return Sleep object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Sleep object.
        """
        return Sleep(
            away=data.get("away"),
            status=data.get("status"),
            awake=data.get("awake"),
            light=data.get("light"),
            deep=data.get("deep"),
            score=data.get("score"),
            overview=SleepOverview.from_dict(data.get("overview")),
            quality=SleepQuality.from_dict(data.get("quality")),
            exception=SleepException(data.get("exception")),
            rating=SleepRating(data.get("rating")),
            struggle=SleepStruggle(data.get("struggle")),
            nobody=SleepNobody(data.get("nobody")),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Sleep:
        if _away := data.get("away"):
            self.away = SleepAway(_away)
        if _status := data.get("status"):
            self.status = _status
        if _awake := data.get("awake"):
            self.awake = _awake
        if _light := data.get("light"):
            self.light = _light
        if _deep := data.get("deep"):
            self.deep = _deep
        if _score := data.get("score"):
            self.score = _score
        if _overview := data.get("overview"):
            self.overview = SleepOverview.from_dict(_overview)
        if _quality := data.get("quality"):
            self.quality = SleepQuality.from_dict(_quality)
        if _exception := data.get("exception"):
            self.exception = SleepException(_exception)
        if _rating := data.get("rating"):
            self.rating = SleepRating(_rating)
        if _struggle := data.get("struggle"):
            self.struggle = SleepStruggle(_struggle)
        if _nobody := data.get("nobody"):
            self.nobody = SleepNobody(_nobody)

        return self

@dataclass
class State:
    """Object holding State Infomation from OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A State object.
    """

    timestamp: int
    body: Body
    heart: Heart
    breath: Breath
    sleep: Sleep

    @staticmethod
    def from_dict(data: dict[str, Any]) -> State:
        """Return State object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An State object.
        """
        return State(
            timestamp=data.get("timestamp", None),
            body=Body.from_dict(data.get("body")),
            heart=Heart.from_dict(data.get("heart")),
            breath=Breath.from_dict(data.get("breath")),
            sleep=Sleep.from_dict(data.get("sleep")),
        )

    def update_from_dict(self, data: dict[str, Any]) -> State:
        if _timestamp := data.get("timestamp"):
            self.timestamp = _timestamp
        if _body := data.get("body"):
            self.body.update_from_dict(_body)
        if _breath := data.get("breath"):
            self.breath.update_from_dict(_breath)
        if _heart := data.get("heart"):
            self.heart.update_from_dict(_heart)
        if _sleep := data.get("sleep"):
            self.sleep.update_from_dict(_sleep)

        return self


@dataclass
class Info:
    """Object holding device infomation from OWRCare."""

    model: str
    id: str
    hardware: str
    firmware: str
    version: str
    free_heap: int
    ip: str
    mac_addr: str
    name: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Info:
        """Return Device information object from OWRCare API response.

        Args:
        ----
            data: The data from the OWRCare device API.

        Returns:
        -------
            A Device information object.
        """
        return Info(
            model=data.get("model", None),
            id=data.get("id", None),
            hardware=data.get("hardware", None),
            firmware=data.get("firmware", None),
            version=data.get("version", None),
            free_heap=data.get("free_heap", None),
            ip=data.get("ip", None),
            mac_addr=data.get("mac_addr", None),
            name=data.get("name", None),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Info:
        if _model := data.get("model"):
            self.model = _model
        if _id := data.get("id"):
            self.id = _id
        if _hardware := data.get("hardware"):
            self.hardware = _hardware
        if _firmware := data.get("firmware"):
            self.firmware = _firmware
        if _version := data.get("version"):
            self.version = _version
        if _free_heap := data.get("free_heap"):
            self.free_heap = _free_heap
        if _ip := data.get("ip"):
            self.ip = _ip
        if _mac := data.get("mac"):
            self.mac = _mac
        if _name := data.get("name"):
            self.name = _name

        return self


class SettingSwitch(IntEnum):
    """Enumeration representing body range from OWRCare."""

    OFF = 0
    ON = 1

@dataclass
class Setting:
    """Object holding Setting information from OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A Setting object.
    """

    binding_count: int
    binding: SettingSwitch
    realtime_ws: SettingSwitch
    realtime_mq: SettingSwitch
    body: SettingSwitch
    heart: SettingSwitch
    breath: SettingSwitch
    sleep: SettingSwitch
    mode: SettingSwitch
    nobody: SettingSwitch
    nobody_duration: int
    struggle: SettingSwitch
    stop_duration: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Setting:
        """Return Setting object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Setting object.
        """
        return Setting(
            binding_count=data.get("binding_count", None),
            binding=data.get("binding", None),
            realtime_ws=data.get("realtime_ws", None),
            realtime_mq=data.get("realtime_mq", None),
            body=data.get("body", None),
            heart=data.get("heart", None),
            breath=data.get("breath", None),
            sleep=data.get("sleep", None),
            mode=data.get("mode", None),
            nobody=data.get("nobody", None),
            nobody_duration=data.get("nobody_duration", None),
            struggle=data.get("struggle", None),
            stop_duration=data.get("stop_duration", None),
        )

    def update_from_dict(self, data: dict[str, Any]) -> Setting:
        if _binding_count := data.get("binding_count"):
            self.binding_count = _binding_count
        if _binding := data.get("binding"):
            self.binding = _binding
        if _realtime_ws := data.get("realtime_ws"):
            self.realtime_ws = _realtime_ws
        if _realtime_mq := data.get("realtime_mq"):
            self.realtime_mq = _realtime_mq
        if _body := data.get("body"):
            self.body = _body
        if _heart := data.get("heart"):
            self.heart = _heart
        if _breath := data.get("breath"):
            self.breath = _breath
        if _sleep := data.get("sleep"):
            self.sleep = _sleep
        if _mode := data.get("mode"):
            self.mode = _mode
        if _nobody := data.get("nobody"):
            self.nobody = _nobody
        if _nobody_duration := data.get("nobody_duration"):
            self.nobody_duration = _nobody_duration
        if _struggle := data.get("struggle"):
            self.struggle = _struggle
        if _stop_duration := data.get("stop_duration"):
            self.stop_duration = _stop_duration

        return self


@dataclass
class Device:
    """Object holding Device Infomation from OWRCare.

    Args:
    ----
        data: The data from the OWRCare device API.

    Returns:
    -------
        A Device object.
    """

    setting: Setting
    info: Info
    state: State


    @staticmethod
    def from_dict(data: dict[str, Any]) -> Device:
        """Return Device object form OWRCare API response.

        Args:
        ----
            data: The response from the OWRCare API.

        Returns:
        -------
            An Device object.
        """
        return Device(
            setting=Setting.from_dict(data.get("setting")),
            info=Info.from_dict(data.get("info")),
            state=State.from_dict(data.get("states")[0]),
        )

    # def __init__(self, data: dict[str, Any]) -> None:
    #     """Initialize an empty OWRCare device class.

    #     Args:
    #     ----
    #         data: The full API response from a OWRCare device.

    #     Raises:
    #     ------
    #         OWRCareError: In case the given API response is incomplete in a way
    #             that a Device object cannot be constructed from it.
    #     """
    #     # Check if all elements are in the passed dict, else raise an Error
    #     # if any(
    #     #     k not in data and data[k] is not None
    #     #     for k in ("setting","info", "state")
    #     # ):
    #     #     msg = "OWRCare data is incomplete, cannot construct device object"
    #     #     raise OWRCareError(msg)
    #     self.update_from_dict(data)

    def update_from_dict(self, data: dict[str, Any]) -> Device:
        """Return Device object from OWRCare API response.

        Args:
        ----
            data: Update the device object with the data received from a
                OWRCare device API.

        Returns:
        -------
            The updated Device object.
        """
        if _setting := data.get("setting"):
            self.setting.update_from_dict(_setting)
        if _info := data.get("info"):
            self.info.update_from_dict(_info)
        if _states := data.get("states"):
            # extract first item as the lastest state in list of states
            self.state.update_from_dict(_states[0])

        return self
