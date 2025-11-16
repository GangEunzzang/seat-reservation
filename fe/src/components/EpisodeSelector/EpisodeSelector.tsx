import {type FC, useState} from 'react';
import type {Episode} from '../../types';
import './EpisodeSelector.css';

interface EpisodeSelectorProps {
    episodes: Episode[];
    currentEpisodeId: string;
    onEpisodeChange: (id: string) => void;
    onAddEpisode: (name: string) => void;
}

export const EpisodeSelector: FC<EpisodeSelectorProps> = ({
                                                              episodes,
                                                              currentEpisodeId,
                                                              onEpisodeChange,
                                                              onAddEpisode,
                                                          }) => {
    const [newEpisodeName, setNewEpisodeName] = useState('');

    const handleAdd = () => {
        if (newEpisodeName.trim()) {
            onAddEpisode(newEpisodeName);
            setNewEpisodeName('');
        }
    };

    return (
        <div className="episode-selector">
            <select
                value={currentEpisodeId}
                onChange={e => onEpisodeChange(e.target.value)}
            >
                {episodes.map(ep => (
                    <option key={ep.id} value={ep.id}>{ep.name}</option>
                ))}
            </select>
            <input
                type="text"
                placeholder="새 에피소드 이름"
                value={newEpisodeName}
                onChange={e => setNewEpisodeName(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleAdd()}
            />
            <button onClick={handleAdd}>에피소드 추가</button>
        </div>
    );
};
