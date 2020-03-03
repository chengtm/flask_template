# -*- coding: utf-8 -*-

"""Database module, including the SQLAlchemy database object and DB-related utilities."""

import datetime as dt

from sqlalchemy.orm import relationship, backref

from ..extensions import db

Column = db.Column
Index = db.Index
relationship = relationship
backref = backref


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        if commit:
            return instance.save()
        else:
            db.session.add(instance)
            return instance

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


db.Model_RW = db.make_declarative_base()
class ModelCRM(CRUDMixin, db.Model_RW):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if isinstance(record_id, (int, float)):
            return cls.query.get(int(record_id))
        return None

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Object(id: {})>'.format(self.id)


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
