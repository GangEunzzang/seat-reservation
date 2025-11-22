import type {FC} from 'react';
import {X, User} from 'lucide-react';
import type {Table, Attendee} from '../../types';
import './ReservationPanel.css';

interface ReservationPanelProps {
    tables: Table[];
    getAttendeeById: (id: number) => Attendee | undefined;
    onClose: () => void;
}

export const ReservationPanel: FC<ReservationPanelProps> = ({tables, getAttendeeById, onClose}) => {
    const reservations = tables.flatMap(table =>
        table.seats
            .filter(seat => seat.isReserved && seat.attendeeId)
            .map(seat => {
                const attendee = getAttendeeById(seat.attendeeId!);
                return {
                    tableName: table.name,
                    seatNumber: seat.seatNumber,
                    reservedBy: attendee ? `${attendee.branchName} - ${attendee.name}` : '알 수 없음',
                };
            })
    );

    return (
        <div className="reservation-panel">
            <div className="reservation-panel__header">
                <h3 className="reservation-panel__title">예약 내역</h3>
                <button className="reservation-panel__close" onClick={onClose}>
                    <X size={18}/>
                </button>
            </div>

            <div className="reservation-panel__content">
                {reservations.length === 0 ? (
                    <div className="reservation-panel__empty">
                        예약된 좌석이 없습니다
                    </div>
                ) : (
                    <div className="reservation-panel__list">
                        {reservations.map((reservation, index) => (
                            <div key={index} className="reservation-panel__item">
                                <div className="reservation-panel__item-icon">
                                    <User size={14}/>
                                </div>
                                <div className="reservation-panel__item-info">
                                    <div className="reservation-panel__item-name">
                                        {reservation.reservedBy}
                                    </div>
                                    <div className="reservation-panel__item-seat">
                                        {reservation.tableName} - {reservation.seatNumber}번 좌석
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="reservation-panel__footer">
                <div className="reservation-panel__count">
                    총 {reservations.length}건
                </div>
            </div>
        </div>
    );
};
