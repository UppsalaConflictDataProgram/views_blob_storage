from typing import Optional

from contextlib import closing
from hashlib import md5
from storage import FileStorage
from db import Blob,Session
from storage import ExistsError,NotFoundError
from exceptions import DbCorruptionError

storage_backend = FileStorage()

def withsession(fn):
    def inner(sess=None,*args,**kwargs):
        if sess is None:
            with closing(Session()) as sess:
                return fn(sess = sess,*args,**kwargs)
        else:
            fn(sess,*args,**kwargs)
    return inner

@withsession
def store(data: bytes,sess: Optional[Session] = None):
    if sess is not None:
        data_id = md5(data).hexdigest()

        existing = sess.query(Blob).get(data_id)
        if existing is not None:
            raise ExistsError

        blob = Blob(id=data_id)
        sess.add(blob)

        storage_backend.store(data,data_id)

        sess.commit()
        return data_id
    else: 
        return None

@withsession
def retrieve(did: str, sess: Optional[Session] = None):
    blob_entry = sess.query(Blob).get(did)
    if blob_entry is None:
        raise NotFoundError
    try:
        storage_backend.retrieve(blob_entry.id)
    except NotFoundError:
        sess.delete(blob_entry)
        sess.commit()
        raise DbCorruptionError(f"{blob_entry.id}"
                " was not associated with a file")
    return storage_backend.retrieve(blob_entry.id)

@withsession
def getlist(sess: Optional[Session] = None):
    blobs = sess.query(Blob).all()
    ids = [b.id for b in blobs]
    return ids

