from sqlalchemy.orm import Session
from app.models.payment import Payment


def update_payment_status(db: Session, payment_id: int, new_status: str) -> None:
    db.query(Payment).filter(Payment.id == payment_id).update(
        {"status": new_status}, synchronize_session=False
    )
    db.commit()


def update_payment_amount(db: Session, payment_id: int, amount: float) -> None:
    db.query(Payment).filter(Payment.id == payment_id).update(
        {"amount": amount}, synchronize_session=False
    )
    db.commit()


def create_payment(db: Session, payment: Payment) -> Payment:
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


