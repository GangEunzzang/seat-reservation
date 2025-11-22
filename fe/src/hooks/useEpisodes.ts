import {useState} from 'react';
import type {Episode, Table, Seat, ZoneInfo, Attendee} from '../types';

const createSeats = (tableId: string, count: number): Seat[] => {
    return Array.from({length: count}, (_, i) => ({
        id: `${tableId}-seat-${i + 1}`,
        tableId,
        seatNumber: i + 1,
        isReserved: false,
    }));
};

const defaultZones: ZoneInfo[] = [
    {id: 'A', name: 'A'},
    {id: 'B', name: 'B'},
    {id: 'C', name: 'C'},
    {id: 'D', name: 'D'},
];

export const useEpisodes = () => {
    const [episodes, setEpisodes] = useState<Episode[]>([
        {id: '1', name: '2024 연말 총회', tables: [], zones: defaultZones, attendees: []}
    ]);
    const [currentEpisodeId, setCurrentEpisodeId] = useState('1');

    const currentEpisode = episodes.find(ep => ep.id === currentEpisodeId);
    const tables = currentEpisode?.tables || [];
    const zones = currentEpisode?.zones || [];
    const attendees = currentEpisode?.attendees || [];

    const addEpisode = (name: string) => {
        if (!name.trim()) return;
        const newEpisode: Episode = {
            id: Date.now().toString(),
            name,
            tables: [],
            zones: defaultZones,
            attendees: []
        };
        setEpisodes(prev => [...prev, newEpisode]);
        setCurrentEpisodeId(newEpisode.id);
    };

    const addZone = (name: string) => {
        if (!name.trim()) return;
        const newZone: ZoneInfo = {
            id: Date.now().toString(),
            name: name.toUpperCase(),
        };
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {...ep, zones: [...ep.zones, newZone]}
                : ep
        ));
    };

    const deleteZone = (zoneId: string) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    zones: ep.zones.filter(z => z.id !== zoneId),
                    tables: ep.tables.filter(t => t.zoneId !== zoneId)
                }
                : ep
        ));
    };

    const addTable = (zoneId: string = 'A') => {
        const tableId = Date.now().toString();
        const seatCount = 8;
        const zone = zones.find(z => z.id === zoneId);
        const zoneName = zone?.name || zoneId;
        const zoneTableCount = tables.filter(t => t.zoneId === zoneId).length;
        const newTable: Table = {
            id: tableId,
            x: 100 + (zoneTableCount % 5) * 180,
            y: 50 + Math.floor(zoneTableCount / 5) * 180,
            seatCount,
            name: `${zoneName}-${zoneTableCount + 1}`,
            seats: createSeats(tableId, seatCount),
            zoneId,
        };
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {...ep, tables: [...ep.tables, newTable]}
                : ep
        ));
    };

    const updateTablePosition = (id: string, x: number, y: number) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    tables: ep.tables.map(t => t.id === id ? {...t, x, y} : t)
                }
                : ep
        ));
    };

    const updateTableSeatCount = (id: string, seatCount: number) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    tables: ep.tables.map(t => {
                        if (t.id !== id) return t;
                        return {
                            ...t,
                            seatCount,
                            seats: createSeats(id, seatCount),
                        };
                    })
                }
                : ep
        ));
    };

    const deleteTable = (id: string) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {...ep, tables: ep.tables.filter(t => t.id !== id)}
                : ep
        ));
    };

    const reserveSeat = (tableId: string, seatId: string, attendeeId: string) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    tables: ep.tables.map(t => {
                        if (t.id !== tableId) return t;
                        return {
                            ...t,
                            seats: t.seats.map(s =>
                                s.id === seatId
                                    ? {...s, isReserved: true, attendeeId}
                                    : s
                            )
                        };
                    })
                }
                : ep
        ));
    };

    const cancelReservation = (tableId: string, seatId: string) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    tables: ep.tables.map(t => {
                        if (t.id !== tableId) return t;
                        return {
                            ...t,
                            seats: t.seats.map(s =>
                                s.id === seatId
                                    ? {...s, isReserved: false, attendeeId: undefined}
                                    : s
                            )
                        };
                    })
                }
                : ep
        ));
    };

    const addAttendees = (newAttendees: Attendee[]) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {...ep, attendees: [...ep.attendees, ...newAttendees]}
                : ep
        ));
    };

    const getAttendeeById = (attendeeId: string) => {
        return attendees.find(a => a.id === attendeeId);
    };

    const getAvailableAttendees = () => {
        const reservedAttendeeIds = new Set(
            tables.flatMap(t => t.seats)
                .filter(s => s.isReserved && s.attendeeId)
                .map(s => s.attendeeId!)
        );
        return attendees.filter(a => !reservedAttendeeIds.has(a.id));
    };

    return {
        episodes,
        currentEpisodeId,
        setCurrentEpisodeId,
        currentEpisode,
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
    };
};
