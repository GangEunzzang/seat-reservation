import {useRef} from 'react';
import type {FC} from 'react';
import Draggable from 'react-draggable';
import type {DraggableData, DraggableEvent} from 'react-draggable';
import type {Table as TableType, Seat, Attendee} from '../../types';
import './Table.css';

interface TableProps {
    table: TableType;
    isSelected: boolean;
    onSelect: () => void;
    onDragStop: (x: number, y: number) => void;
    onSeatClick: (seat: Seat) => void;
    getAttendeeById?: (id: string) => Attendee | undefined;
}

export const Table: FC<TableProps> = ({
                                          table,
                                          isSelected,
                                          onSelect,
                                          onDragStop,
                                          onSeatClick,
                                          getAttendeeById,
                                      }) => {
    const nodeRef = useRef<HTMLDivElement>(null);

    const handleDragStop = (_e: DraggableEvent, data: DraggableData) => {
        onDragStop(data.x, data.y);
    };

    const containerCenter = 75;
    const seatDistance = 55;

    return (
        <Draggable
            nodeRef={nodeRef}
            position={{x: table.x, y: table.y}}
            onStop={handleDragStop}
            bounds="parent"
        >
            <div
                ref={nodeRef}
                className={`table-container ${isSelected ? 'table-container--selected' : ''}`}
                onClick={onSelect}
            >
                <div className="table-circle-outer">
                    <div className="table-circle-inner">
                        <span className="table-circle__number">{table.name.replace('테이블 ', 'T')}</span>
                    </div>
                </div>

                {table.seats.map((seat, index) => {
                    const angle = (index / table.seatCount) * 2 * Math.PI - Math.PI / 2;
                    const x = Math.cos(angle) * seatDistance;
                    const y = Math.sin(angle) * seatDistance;

                    let tooltipText = `좌석 ${seat.seatNumber}`;
                    if (seat.isReserved && seat.attendeeId && getAttendeeById) {
                        const attendee = getAttendeeById(seat.attendeeId);
                        if (attendee) {
                            tooltipText = `${attendee.branchName} - ${attendee.name} (${attendee.position})`;
                        }
                    }

                    return (
                        <div
                            key={seat.id}
                            className={`seat ${seat.isReserved ? 'seat--reserved' : 'seat--available'}`}
                            style={{
                                left: `${containerCenter + x}px`,
                                top: `${containerCenter + y}px`,
                            }}
                            onClick={(e) => {
                                e.stopPropagation();
                                onSeatClick(seat);
                            }}
                            title={tooltipText}
                        >
                            {seat.seatNumber}
                        </div>
                    );
                })}
            </div>
        </Draggable>
    );
};
