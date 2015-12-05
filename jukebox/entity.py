""":mod:`jukebox.entity` --- jukebox entity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Unicode
from sqlalchemy_utils.types import UUIDType

from .orm import Base


class Artist(Base):
    """Store artist, it borrows structure of last.fm artist

    .. seealso::

       `last.fm artist.getInfo API documents`__
           Show information that artist has

    __ http://www.last.fm/api/show/artist.getInfo

    """

    #: (:class:`uuid.UUID`) primary key for entity :class:`~.Artist`
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)

    #: (:class:`uuid.UUID`) music brainz identifier
    #: :class:`~.Artist`\ .
    #:
    #: .. seealso::
    #:
    #:    `Musicbrainz identifier`__
    #:        Documentation for musicbrainz identifier
    #:
    #: __ https://musicbrainz.org/doc/MusicBrainz_Identifier
    mbid = Column(UUIDType(binary=False), nullable=True)

    #: (:class:`str`) name of :class:`Artist`
    name = Column(Unicode, nullable=False)

    #: (:class:`datetime.datetime`) date time when entity is created
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        default=datetime.now(timezone.utc))

    #: table name of :class:`~.Artist`
    __tablename__ = 'artist'
