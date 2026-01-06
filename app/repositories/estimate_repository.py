from sqlalchemy.orm import Session
from app.models.estimate import Estimate


def update_estimate(db: Session, estimate_id: int, status_value: str, amount: float) -> None:
    db.query(Estimate).filter(Estimate.id == estimate_id).update(
        {"status": status_value, "amount": amount}, synchronize_session=False
    )
    db.commit()


def create_estimate(db: Session, estimate: Estimate) -> Estimate:
    db.add(estimate)
    db.commit()
    db.refresh(estimate)
    return estimate


