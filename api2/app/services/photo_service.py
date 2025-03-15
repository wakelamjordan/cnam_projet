from flask import jsonify
from app.models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.photo_model import Photo
from app.errors.service_error import ResultEmpty


def select_all():
    db: Session = next(get_db())
    try:
        photos: list[Photo] = db.query(Photo).filter().all()

        def to_dict(photo: Photo) -> dict:
            return photo.to_dict()

        photos = map(to_dict, photos)

        return list(photos)
    finally:
        db.close()


def insert(data: dict):
    db: Session = next(get_db())
    try:
        check: Photo = db.query(Photo).filter_by(or_(_name=data['name'], ))

        photo: Photo = Photo(name=data['name'],
                             description=data['description'])
        db.add(photo)
        db.commit()
    finally:
        db.close()


def select_one(data: dict):
    db: Session = next(get_db())
    try:
        photo: Photo = db.query(Photo).filter_by(_name=data['name']).first()
        if not photo:
            raise ResultEmpty()
        return photo.to_dict()
    except ResultEmpty as e:
        db.rollback()
        return jsonify({'error': str(e)}), 404
    finally:
        db.close()
