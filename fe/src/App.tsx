import { useState } from 'react';
import type { Seat } from './types';
import { useEpisodes } from './hooks/useEpisodes';
import { Sidebar } from './components/Sidebar';
import { Stage } from './components/Stage';
import { Floor } from './components/Floor';
import { TableSettings } from './components/TableSettings';
import { ReservationModal } from './components/ReservationModal';
import './App.css';

function App() {
  const {
    episodes,
    currentEpisodeId,
    setCurrentEpisodeId,
    tables,
    addEpisode,
    addTable,
    updateTablePosition,
    updateTableSeatCount,
    deleteTable,
    reserveSeat,
    cancelReservation,
  } = useEpisodes();

  const [selectedTableId, setSelectedTableId] = useState<string | null>(null);
  const [selectedSeat, setSelectedSeat] = useState<Seat | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

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

  const handleReserveSeat = (name: string) => {
    if (selectedSeat) {
      reserveSeat(selectedSeat.tableId, selectedSeat.id, name);
      setSelectedSeat(null);
    }
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
        onAddTable={addTable}
        isCollapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      <main className={`main-content ${sidebarCollapsed ? 'main-content--sidebar-collapsed' : ''}`}>
        <Stage />
        <Floor
          tables={tables}
          selectedTableId={selectedTableId}
          onSelectTable={setSelectedTableId}
          onTableDragStop={updateTablePosition}
          onSeatClick={handleSeatClick}
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
          onReserve={handleReserveSeat}
          onCancel={handleCancelReservation}
          onClose={() => setSelectedSeat(null)}
        />
      )}
    </div>
  );
}

export default App;
