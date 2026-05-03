from sqlmodel import Session, desc, select

from app.models.features import Feature


class Service:
    def __init__(self, session: Session):
        self._session = session

    def get_features(
        self, page: int = 1, number_of_features: int = 10, mag_type: str | None = None
    ):

        offset: int = (page - 1) * number_of_features
        statement = (
            select(Feature)
            .order_by(desc(Feature.event_date))
            .offset(offset)
            .limit(number_of_features)
        )

        if mag_type is not None:
            statement = (
                select(Feature)
                .where(Feature.mag_type == mag_type)
                .order_by(desc(Feature.event_date))
                .offset(offset)
                .limit(number_of_features)
            )

        features = self._session.exec(statement).all()
        successful = True if features else False
        pagination = {
            "current_page": page,
            "total": len(features),
            "per_page": number_of_features,
        }

        return {"sucessful": successful, "features": features, "pagination": pagination}
