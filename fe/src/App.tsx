import {useState} from 'react';
import type {Seat} from './types';
import {useEpisodes} from './hooks/useEpisodes';
import {Sidebar} from './components/Sidebar';
import {Stage} from './components/Stage';
import {Floor} from './components/Floor';
import {TableSettings} from './components/TableSettings';
import {ReservationModal} from './components/ReservationModal';
import {ReservationPanel} from './components/ReservationPanel';
import {ExcelUpload} from './components/ExcelUpload';
import './App.css';

function App() {
    const {
        episodes,
        currentEpisodeId,
        setCurrentEpisodeId,
        tables,
        zones,
        attendees,
        addEpisode,
        addZone,
        deleteZone,
        addTable,
        updateTablePosition,
        updateTableSeatCount,
        deleteTable,
        reserveSeat,
        cancelReservation,
        addAttendees,
        getAttendeeById,
        getAvailableAttendees,
    } = useEpisodes();

    const [selectedTableId, setSelectedTableId] = useState<string | null>(null);
    const [selectedSeat, setSelectedSeat] = useState<Seat | null>(null);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [showReservationPanel, setShowReservationPanel] = useState(false);
    const [showExcelUpload, setShowExcelUpload] = useState(false);
    const [currentZoneId, setCurrentZoneId] = useState<string | null>(null);

    const selectedTable = tables.find(t => t.id === selectedTableId);

    const handleDeleteTable = () => {
        if (selectedTableId) {
            deleteTable(selectedTableId);
            setSelectedTableId(null);
        }
    };

    const handleSeatClick = (seat: Seat) => {
        setSelectedSeat(seat);
    };

    const handleReserveSeat = (attendeeId: string) => {
        if (selectedSeat) {
            reserveSeat(selectedSeat.tableId, selectedSeat.id, attendeeId);
            setSelectedSeat(null);
        }
    };

    const handleUploadSuccess = () => {
        // TODO: 백엔드에서 참석자 목록을 다시 가져오기
        setShowExcelUpload(false);
    };

    const handleCancelReservation = () => {
        if (selectedSeat) {
            cancelReservation(selectedSeat.tableId, selectedSeat.id);
            setSelectedSeat(null);
        }
    };

    return (
        <div className="app">
            <Sidebar
                episodes={episodes}
                currentEpisodeId={currentEpisodeId}
                onEpisodeChange={setCurrentEpisodeId}
                onAddEpisode={addEpisode}
                onAddTable={() => addTable(currentZoneId || 'A')}
                isCollapsed={sidebarCollapsed}
                onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
                onShowReservations={() => setShowReservationPanel(true)}
                onUploadExcel={() => setShowExcelUpload(true)}
            />

            <main className={`main-content ${sidebarCollapsed ? 'main-content--sidebar-collapsed' : ''}`}>
                <Stage/>
                <Floor
                    tables={tables}
                    zones={zones}
                    selectedTableId={selectedTableId}
                    onSelectTable={setSelectedTableId}
                    onTableDragStop={updateTablePosition}
                    onSeatClick={handleSeatClick}
                    currentZoneId={currentZoneId}
                    onZoneChange={setCurrentZoneId}
                    onAddZone={addZone}
                    onDeleteZone={deleteZone}
                    getAttendeeById={getAttendeeById}
                />
            </main>

            {selectedTable && (
                <TableSettings
                    table={selectedTable}
                    onUpdateSeats={(seats) => updateTableSeatCount(selectedTable.id, seats)}
                    onDelete={handleDeleteTable}
                    onClose={() => setSelectedTableId(null)}
                />
            )}

            {selectedSeat && (
                <ReservationModal
                    seat={selectedSeat}
                    attendees={attendees}
                    availableAttendees={getAvailableAttendees()}
                    getAttendeeById={getAttendeeById}
                    onReserve={handleReserveSeat}
                    onCancel={handleCancelReservation}
                    onClose={() => setSelectedSeat(null)}
                />
            )}

            {showReservationPanel && (
                <ReservationPanel
                    tables={tables}
                    onClose={() => setShowReservationPanel(false)}
                />
            )}

            {showExcelUpload && currentEpisodeId && (
                <ExcelUpload
                    episodeId={parseInt(currentEpisodeId)}
                    onUploadSuccess={handleUploadSuccess}
                    onClose={() => setShowExcelUpload(false)}
                />
            )}
        </div>
    );
}

export default App;
