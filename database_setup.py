#!/usr/bin/python3
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(String, primary_key=True)
    items = relationship('CatalogItem')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.id,
            'items': [i.serialize for i in self.items]
        }


class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    id = Column(String, primary_key=True)
    description = Column(String(255))
    catalog_id = Column(String, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.id,
            "description": self.description,
            "catalog_id": self.catalog_id
        }

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.create_all(engine)
