# This file was auto-generated by Fern from our API Definition.

import typing

from .event_body_identify import EventBodyIdentify
from .event_body_track import EventBodyTrack

EventBody = typing.Union[EventBodyTrack, EventBodyIdentify]
