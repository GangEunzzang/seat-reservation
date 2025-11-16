import type {FC} from 'react';
import type {Table} from '../../types';
import './TableSettings.css';

interface TableSettingsProps {
    table: Table;
    onUpdateSeats: (seats: number) => void;
    onDelete: () => void;
    onClose: () => void;
}

export const TableSettings: FC<TableSettingsProps> = ({
                                                          table,
                                                          onUpdateSeats,
                                                          onDelete,
                                                          onClose,
                                                      }) => {
    return (
        <div className="table-settings">
            <div className="table-settings__header">
                <h3>테이블 설정</h3>
                <button className="table-settings__close" onClick={onClose}>
                    ✕
                </button>
            </div>

            <div className="table-settings__content">
                <div className="table-settings__field">
                    <label>테이블 이름</label>
                    <span>{table.name}</span>
                </div>

                <div className="table-settings__field">
                    <label htmlFor="seats">좌석 수</label>
                    <input
                        id="seats"
                        type="number"
                        min="1"
                        max="20"
                        value={table.seatCount}
                        onChange={e => onUpdateSeats(parseInt(e.target.value) || 1)}
                    />
                </div>

                <div className="table-settings__field">
                    <label>위치</label>
                    <span>X: {Math.round(table.x)}, Y: {Math.round(table.y)}</span>
                </div>
            </div>

            <button className="table-settings__delete" onClick={onDelete}>
                테이블 삭제
            </button>
        </div>
    );
};
