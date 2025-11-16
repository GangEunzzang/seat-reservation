import {useState} from 'react';
import type {FC} from 'react';
import type {Seat} from '../../types';
import './ReservationModal.css';

interface ReservationModalProps {
    seat: Seat;
    onReserve: (name: string) => void;
    onCancel: () => void;
    onClose: () => void;
}

export const ReservationModal: FC<ReservationModalProps> = ({
                                                                seat,
                                                                onReserve,
                                                                onCancel,
                                                                onClose,
                                                            }) => {
    const [name, setName] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (name.trim()) {
            onReserve(name.trim());
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div className="modal__header">
                    <h3>좌석 {seat.seatNumber}</h3>
                    <button className="modal__close" onClick={onClose}>✕</button>
                </div>

                {seat.isReserved ? (
                    <div className="modal__content">
                        <p>현재 예약자: <strong>{seat.reservedBy}</strong></p>
                        <button className="modal__cancel-btn" onClick={onCancel}>
                            예약 취소
                        </button>
                    </div>
                ) : (
                    <form className="modal__content" onSubmit={handleSubmit}>
                        <label htmlFor="name">예약자 이름</label>
                        <input
                            id="name"
                            type="text"
                            value={name}
                            onChange={e => setName(e.target.value)}
                            placeholder="이름을 입력하세요"
                            autoFocus
                        />
                        <button type="submit" className="modal__reserve-btn">
                            예약하기
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};
