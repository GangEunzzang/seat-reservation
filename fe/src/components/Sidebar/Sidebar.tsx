import {useState} from 'react';
import type {FC} from 'react';
import type {Episode} from '../../types';
import {
    PanelLeftClose,
    PanelLeftOpen,
    Calendar,
    Plus,
    Table2,
    ChevronRight,
    ClipboardList,
    Upload
} from 'lucide-react';
import './Sidebar.css';

interface SidebarProps {
    episodes: Episode[];
    currentEpisodeId: number;
    onEpisodeChange: (id: number) => void;
    onAddEpisode: (name: string, year: number, startDate: string, endDate: string) => void;
    onAddTable: () => void;
    isCollapsed: boolean;
    onToggle: () => void;
    onShowReservations: () => void;
    onUploadExcel: () => void;
}

export const Sidebar: FC<SidebarProps> = ({
                                              episodes,
                                              currentEpisodeId,
                                              onEpisodeChange,
                                              onAddEpisode,
                                              onAddTable,
                                              isCollapsed,
                                              onToggle,
                                              onShowReservations,
                                              onUploadExcel,
                                          }) => {
    const [newEpisodeName, setNewEpisodeName] = useState('');
    const [newEpisodeYear, setNewEpisodeYear] = useState(new Date().getFullYear());
    const [newEpisodeStartDate, setNewEpisodeStartDate] = useState('');
    const [newEpisodeEndDate, setNewEpisodeEndDate] = useState('');
    const [showAddEpisode, setShowAddEpisode] = useState(false);

    const handleAddEpisode = () => {
        if (newEpisodeName.trim() && newEpisodeStartDate && newEpisodeEndDate) {
            onAddEpisode(newEpisodeName, newEpisodeYear, newEpisodeStartDate, newEpisodeEndDate);
            setNewEpisodeName('');
            setNewEpisodeYear(new Date().getFullYear());
            setNewEpisodeStartDate('');
            setNewEpisodeEndDate('');
            setShowAddEpisode(false);
        }
    };

    return (
        <>
        <aside className={`sidebar ${isCollapsed ? 'sidebar--collapsed' : ''}`}>
            <div className="sidebar__header">
                <div className="sidebar__logo">
                    {!isCollapsed && <span>좌석 예약</span>}
                </div>
                <button
                    className="sidebar__toggle"
                    onClick={onToggle}
                >
                    {isCollapsed ? <PanelLeftOpen size={20}/> : <PanelLeftClose size={20}/>}
                </button>
            </div>

            <nav className="sidebar__nav">
                <div className="sidebar__section">
                    {!isCollapsed && <div className="sidebar__section-title">에피소드</div>}

                    <ul className="sidebar__menu">
                        {episodes.map(ep => (
                            <li key={ep.id}>
                                <button
                                    className={`sidebar__menu-item ${ep.id === currentEpisodeId ? 'sidebar__menu-item--active' : ''}`}
                                    onClick={() => onEpisodeChange(ep.id)}
                                    title={isCollapsed ? ep.name : undefined}
                                >
                                    <Calendar size={18}/>
                                    {!isCollapsed && (
                                        <>
                                            <span className="sidebar__menu-text">{ep.name}</span>
                                            {ep.id === currentEpisodeId &&
                                                <ChevronRight size={16} className="sidebar__menu-indicator"/>}
                                        </>
                                    )}
                                </button>
                            </li>
                        ))}

                        <li>
                            <button
                                className="sidebar__menu-item sidebar__menu-item--add"
                                onClick={() => !isCollapsed && setShowAddEpisode(!showAddEpisode)}
                                title={isCollapsed ? '에피소드 추가' : undefined}
                            >
                                <Plus size={18}/>
                                {!isCollapsed && <span className="sidebar__menu-text">새 에피소드</span>}
                            </button>
                        </li>
                    </ul>

                </div>

                <div className="sidebar__section">
                    {!isCollapsed && <div className="sidebar__section-title">도구</div>}

                    <ul className="sidebar__menu">
                        <li>
                            <button
                                className="sidebar__menu-item sidebar__menu-item--tool"
                                onClick={onAddTable}
                                title={isCollapsed ? '테이블 추가' : undefined}
                            >
                                <Table2 size={18}/>
                                {!isCollapsed && <span className="sidebar__menu-text">테이블 추가</span>}
                            </button>
                        </li>
                        <li>
                            <button
                                className="sidebar__menu-item sidebar__menu-item--tool"
                                onClick={onUploadExcel}
                                title={isCollapsed ? '참석자 업로드' : undefined}
                            >
                                <Upload size={18}/>
                                {!isCollapsed && <span className="sidebar__menu-text">참석자 업로드</span>}
                            </button>
                        </li>
                        <li>
                            <button
                                className="sidebar__menu-item sidebar__menu-item--tool"
                                onClick={onShowReservations}
                                title={isCollapsed ? '예약 내역' : undefined}
                            >
                                <ClipboardList size={18}/>
                                {!isCollapsed && <span className="sidebar__menu-text">예약 내역</span>}
                            </button>
                        </li>
                    </ul>
                </div>
            </nav>
        </aside>

        {showAddEpisode && (
            <div className="modal-overlay" onClick={() => setShowAddEpisode(false)}>
                <div className="modal episode-modal" onClick={e => e.stopPropagation()}>
                    <div className="modal__header">
                        <h3>새 에피소드 추가</h3>
                        <button className="modal__close" onClick={() => setShowAddEpisode(false)}>✕</button>
                    </div>
                    <div className="modal__content">
                        <div>
                            <label htmlFor="episode-name">에피소드 이름</label>
                            <input
                                id="episode-name"
                                type="text"
                                placeholder="예: 2025 신년회"
                                value={newEpisodeName}
                                onChange={e => setNewEpisodeName(e.target.value)}
                                autoFocus
                            />
                        </div>
                        <div className="episode-modal__row">
                            <div className="episode-modal__col">
                                <label htmlFor="episode-year">연도</label>
                                <input
                                    id="episode-year"
                                    type="number"
                                    placeholder={new Date().getFullYear().toString()}
                                    value={newEpisodeYear}
                                    onChange={e => setNewEpisodeYear(parseInt(e.target.value) || new Date().getFullYear())}
                                />
                            </div>
                        </div>
                        <div className="episode-modal__row">
                            <div className="episode-modal__col">
                                <label htmlFor="episode-start">시작일</label>
                                <input
                                    id="episode-start"
                                    type="date"
                                    value={newEpisodeStartDate}
                                    onChange={e => setNewEpisodeStartDate(e.target.value)}
                                />
                            </div>
                            <div className="episode-modal__col">
                                <label htmlFor="episode-end">종료일</label>
                                <input
                                    id="episode-end"
                                    type="date"
                                    value={newEpisodeEndDate}
                                    onChange={e => setNewEpisodeEndDate(e.target.value)}
                                />
                            </div>
                        </div>
                        <button
                            className="modal__reserve-btn"
                            onClick={handleAddEpisode}
                            disabled={!newEpisodeName.trim() || !newEpisodeStartDate || !newEpisodeEndDate}
                        >
                            추가하기
                        </button>
                    </div>
                </div>
            </div>
        )}
        </>
    );
};
