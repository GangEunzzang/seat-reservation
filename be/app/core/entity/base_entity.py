from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Timestamp:
	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		nullable=False,
		default=datetime.now,
		comment="생성 일시"
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime,
		nullable=False,
		default=datetime.now,
		onupdate=datetime.now,
		comment="수정 일시"
	)
