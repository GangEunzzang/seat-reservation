import {useState} from 'react';
import type {Seat, Attendee} from './types';
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

    const [selectedTableId, setSelectedTableId] = useState<number | null>(null);
    const [selectedSeat, setSelectedSeat] = useState<Seat | null>(null);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [showReservationPanel, setShowReservationPanel] = useState(false);
    const [showExcelUpload, setShowExcelUpload] = useState(false);
    const [currentZoneId, setCurrentZoneId] = useState<string | null>(null);

    const selectedTable = tables.find(t => t.id === selectedTableId);

    const handleDeleteTable = async () => {
        if (selectedTableId) {
            await deleteTable(selectedTableId);
            setSelectedTableId(null);
        }
    };

    const handleSeatClick = (seat: Seat) => {
        setSelectedSeat(seat);
    };

    const handleReserveSeat = async (attendeeId: number, password: string) => {
        if (selectedSeat) {
            await reserveSeat(selectedSeat.id, attendeeId, password);
            setSelectedSeat(null);
        }
    };

    const handleUploadSuccess = (attendees: Attendee[]) => {
        addAttendees(attendees);
        setShowExcelUpload(false);
    };

    const handleCancelReservation = async (password: string) => {
        if (selectedSeat?.reservationId) {
            await cancelReservation(selectedSeat.reservationId, password);
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
                    getAttendeeById={getAttendeeById}
                    onClose={() => setShowReservationPanel(false)}
                />
            )}

            {showExcelUpload && currentEpisodeId && (
                <ExcelUpload
                    episodeId={currentEpisodeId}
                    onUploadSuccess={handleUploadSuccess}
                    onClose={() => setShowExcelUpload(false)}
                />
            )}
        </div>
    );
}

export default App;
