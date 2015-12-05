from datetime import datetime
import uuid

from jukebox.entity import Artist


def test_artist(fx_session):
    mbid = uuid.uuid4()
    damien_rice = 'Damien rice'
    artist = Artist(mbid=mbid, name=damien_rice)
    with fx_session.begin():
        fx_session.add(artist)
    artist = fx_session.query(Artist).filter_by(id=artist.id).one()
    assert artist
    assert artist.id
    assert artist.created_at
    assert isinstance(artist.created_at, datetime)
    assert artist.mbid == mbid
    assert artist.name == damien_rice
