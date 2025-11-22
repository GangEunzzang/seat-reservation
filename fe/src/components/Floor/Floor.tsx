import type {FC} from 'react';
import {ArrowLeft, Plus, Trash2} from 'lucide-react';
import {useState} from 'react';
import type {Table as TableType, Seat, ZoneInfo, Attendee} from '../../types';
import {Table} from './Table';
import './Floor.css';

interface FloorProps {
    tables: TableType[];
    zones: ZoneInfo[];
    selectedTableId: string | null;
    onSelectTable: (id: string) => void;
    onTableDragStop: (id: string, x: number, y: number) => void;
    onSeatClick: (seat: Seat) => void;
    currentZoneId: string | null;
    onZoneChange: (zoneId: string | null) => void;
    onAddZone: (name: string) => void;
    onDeleteZone: (zoneId: string) => void;
    getAttendeeById?: (id: string) => Attendee | undefined;
}

export const Floor: FC<FloorProps> = ({
                                          tables,
                                          zones,
                                          selectedTableId,
                                          onSelectTable,
                                          onTableDragStop,
                                          onSeatClick,
                                          currentZoneId,
                                          onZoneChange,
                                          onAddZone,
                                          onDeleteZone,
                                          getAttendeeById,
                                      }) => {
    const [showAddZone, setShowAddZone] = useState(false);
    const [newZoneName, setNewZoneName] = useState('');

    const getZoneStats = (zoneId: string) => {
        const zoneTables = tables.filter(t => t.zoneId === zoneId);
        const totalSeats = zoneTables.reduce((sum, t) => sum + t.seatCount, 0);
        const reservedSeats = zoneTables.reduce((sum, t) =>
            sum + t.seats.filter(s => s.isReserved).length, 0);
        return {total: totalSeats, reserved: reservedSeats, tableCount: zoneTables.length};
    };

    const getGridStyle = () => {
        const count = zones.length + 1;
        if (count <= 2) return {gridTemplateColumns: '1fr', gridTemplateRows: '1fr 1fr'};
        if (count <= 4) return {gridTemplateColumns: '1fr 1fr', gridTemplateRows: '1fr 1fr'};
        if (count <= 6) return {gridTemplateColumns: '1fr 1fr 1fr', gridTemplateRows: '1fr 1fr'};
        if (count <= 9) return {gridTemplateColumns: '1fr 1fr 1fr', gridTemplateRows: '1fr 1fr 1fr'};
        return {gridTemplateColumns: 'repeat(4, 1fr)', gridTemplateRows: 'repeat(auto-fill, 1fr)'};
    };

    const handleAddZone = () => {
        if (newZoneName.trim()) {
            onAddZone(newZoneName);
            setNewZoneName('');
            setShowAddZone(false);
        }
    };

    if (currentZoneId === null) {
        return (
            <div className="floor">
                <div className="floor__zone-overview" style={getGridStyle()}>
                    {zones.map(zone => {
                        const stats = getZoneStats(zone.id);
                        return (
                            <div key={zone.id} className="floor__zone-block-wrapper">
                                <button
                                    className="floor__zone-block"
                                    onClick={() => onZoneChange(zone.id)}
                                >
                                    <span className="floor__zone-block-label">{zone.name}구역</span>
                                    <span className="floor__zone-block-tables">{stats.tableCount}개 테이블</span>
                                    <span className="floor__zone-block-stats">
                                        {stats.reserved}/{stats.total} 예약
                                    </span>
                                </button>
                                <button
                                    className="floor__zone-delete"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDeleteZone(zone.id);
                                    }}
                                    title="구역 삭제"
                                >
                                    <Trash2 size={14}/>
                                </button>
                            </div>
                        );
                    })}
                    <button
                        className="floor__zone-add"
                        onClick={() => setShowAddZone(true)}
                    >
                        <Plus size={24}/>
                        <span>구역 추가</span>
                    </button>
                </div>
                {showAddZone && (
                    <div className="floor__add-zone-modal">
                        <div className="floor__add-zone-content">
                            <h3>새 구역 추가</h3>
                            <input
                                type="text"
                                placeholder="구역 이름 (예: E, VIP)"
                                value={newZoneName}
                                onChange={e => setNewZoneName(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleAddZone()}
                                autoFocus
                            />
                            <div className="floor__add-zone-actions">
                                <button onClick={() => setShowAddZone(false)}>취소</button>
                                <button onClick={handleAddZone}>추가</button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    const currentZone = zones.find(z => z.id === currentZoneId);
    const filteredTables = tables.filter(t => t.zoneId === currentZoneId);

    const getMinimapGridStyle = () => {
        const count = zones.length;
        if (count <= 2) return {gridTemplateColumns: '1fr', gridTemplateRows: '1fr 1fr'};
        if (count <= 4) return {gridTemplateColumns: '1fr 1fr', gridTemplateRows: '1fr 1fr'};
        if (count <= 6) return {gridTemplateColumns: '1fr 1fr 1fr', gridTemplateRows: '1fr 1fr'};
        return {gridTemplateColumns: '1fr 1fr 1fr', gridTemplateRows: '1fr 1fr 1fr'};
    };

    return (
        <div className="floor">
            <div className="floor__header">
                <button className="floor__back-btn" onClick={() => onZoneChange(null)}>
                    <ArrowLeft size={18}/>
                    <span>구역 선택</span>
                </button>
                <div className="floor__zone-title">{currentZone?.name || currentZoneId}구역</div>
                <div className="floor__zone-info">
                    {getZoneStats(currentZoneId).reserved}/{getZoneStats(currentZoneId).total} 예약됨
                </div>
                <div className="floor__minimap" style={getMinimapGridStyle()}>
                    {zones.map(zone => (
                        <button
                            key={zone.id}
                            className={`floor__minimap-zone ${zone.id === currentZoneId ? 'floor__minimap-zone--active' : ''}`}
                            onClick={() => onZoneChange(zone.id)}
                            title={`${zone.name}구역`}
                        >
                            {zone.name}
                        </button>
                    ))}
                </div>
            </div>

            <div className="floor__area">
                {filteredTables.length === 0 && (
                    <div className="floor__empty">
                        {currentZone?.name || currentZoneId}구역에 테이블을 추가하세요
                    </div>
                )}
                {filteredTables.map(table => (
                    <Table
                        key={table.id}
                        table={table}
                        isSelected={selectedTableId === table.id}
                        onSelect={() => onSelectTable(table.id)}
                        onDragStop={(x, y) => onTableDragStop(table.id, x, y)}
                        onSeatClick={onSeatClick}
                        getAttendeeById={getAttendeeById}
                    />
                ))}
            </div>
        </div>
    );
};
