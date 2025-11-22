import {useState} from 'react';
import type {Episode, Table, Seat, ZoneInfo, Attendee} from '../types';
import {tableApi, seatApi, reservationApi} from '../api';

const defaultZones: ZoneInfo[] = [
    {id: 'A', name: 'A'},
    {id: 'B', name: 'B'},
    {id: 'C', name: 'C'},
    {id: 'D', name: 'D'},
];

export const useEpisodes = () => {
    // TODO: 백엔드에서 Episode 조회하여 초기화
    const [episodes, setEpisodes] = useState<Episode[]>([
        {
            id: 1,
            name: '2024 연말 총회',
            year: 2024,
            startDate: '2024-12-01',
            endDate: '2024-12-31',
            tables: [],
            zones: defaultZones,
            attendees: []
        }
    ]);
    const [currentEpisodeId, setCurrentEpisodeId] = useState(1);

    const currentEpisode = episodes.find(ep => ep.id === currentEpisodeId);
    const tables = currentEpisode?.tables || [];
    const zones = currentEpisode?.zones || [];
    const attendees = currentEpisode?.attendees || [];

    const addEpisode = (name: string) => {
        // TODO: 백엔드 Episode API 연동 필요
        console.warn('Episode 생성은 아직 백엔드와 연동되지 않았습니다.');
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

    const addTable = async (zoneId: string = 'A') => {
        const episode = episodes.find(ep => ep.id === currentEpisodeId);
        if (!episode) {
            console.error('현재 Episode를 찾을 수 없습니다.');
            return;
        }

        try {
            // 백엔드에 테이블 생성
            const tableResponse = await tableApi.create({episode_id: episode.id});

            const seatCount = 8;
            const zone = zones.find(z => z.id === zoneId);
            const zoneName = zone?.name || zoneId;
            const zoneTableCount = tables.filter(t => t.zoneId === zoneId).length;

            // 백엔드에 좌석들 생성
            const seatPromises = Array.from({length: seatCount}, (_, i) =>
                seatApi.create({
                    table_id: tableResponse.id,
                    seat_number: i + 1
                })
            );
            const seatResponses = await Promise.all(seatPromises);

            // 좌석 데이터 생성
            const seats: Seat[] = seatResponses.map(seatRes => ({
                id: seatRes.id,
                tableId: tableResponse.id,
                seatNumber: seatRes.seat_number,
                isReserved: false,
            }));

            const newTable: Table = {
                id: tableResponse.id,
                x: 100 + (zoneTableCount % 5) * 180,
                y: 50 + Math.floor(zoneTableCount / 5) * 180,
                seatCount,
                name: `${zoneName}-${zoneTableCount + 1}`,
                seats,
                zoneId,
            };

            setEpisodes(prev => prev.map(ep =>
                ep.id === currentEpisodeId
                    ? {...ep, tables: [...ep.tables, newTable]}
                    : ep
            ));
        } catch (error) {
            console.error('테이블 생성 실패:', error);
            throw error;
        }
    };

    const updateTablePosition = (id: number, x: number, y: number) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {
                    ...ep,
                    tables: ep.tables.map(t => t.id === id ? {...t, x, y} : t)
                }
                : ep
        ));
    };

    const updateTableSeatCount = async (id: number, seatCount: number) => {
        // TODO: 좌석 수 변경은 복잡함 (기존 좌석 삭제, 새 좌석 생성)
        console.warn('좌석 수 변경은 아직 구현되지 않았습니다.');
    };

    const deleteTable = async (id: number) => {
        try {
            // 백엔드에서 테이블 삭제 (좌석도 cascade 삭제됨)
            await tableApi.delete(id);

            setEpisodes(prev => prev.map(ep =>
                ep.id === currentEpisodeId
                    ? {...ep, tables: ep.tables.filter(t => t.id !== id)}
                    : ep
            ));
        } catch (error) {
            console.error('테이블 삭제 실패:', error);
            throw error;
        }
    };

    const reserveSeat = async (seatId: number, attendeeId: number, password: string) => {
        try {
            // 백엔드에 예약 생성
            const reservation = await reservationApi.create({
                user_id: attendeeId,
                seat_id: seatId,
                password,
            });

            // 프론트엔드 상태 업데이트
            setEpisodes(prev => prev.map(ep =>
                ep.id === currentEpisodeId
                    ? {
                        ...ep,
                        tables: ep.tables.map(t => ({
                            ...t,
                            seats: t.seats.map(s =>
                                s.id === seatId
                                    ? {
                                        ...s,
                                        isReserved: true,
                                        attendeeId,
                                        reservationId: reservation.id
                                    }
                                    : s
                            )
                        }))
                    }
                    : ep
            ));
        } catch (error) {
            console.error('예약 생성 실패:', error);
            throw error;
        }
    };

    const cancelReservation = async (reservationId: number, password: string) => {
        try {
            // 백엔드에 예약 취소
            await reservationApi.cancel(reservationId, password);

            // 프론트엔드 상태 업데이트
            setEpisodes(prev => prev.map(ep =>
                ep.id === currentEpisodeId
                    ? {
                        ...ep,
                        tables: ep.tables.map(t => ({
                            ...t,
                            seats: t.seats.map(s =>
                                s.reservationId === reservationId
                                    ? {
                                        ...s,
                                        isReserved: false,
                                        attendeeId: undefined,
                                        reservationId: undefined
                                    }
                                    : s
                            )
                        }))
                    }
                    : ep
            ));
        } catch (error) {
            console.error('예약 취소 실패:', error);
            throw error;
        }
    };

    const addAttendees = (newAttendees: Attendee[]) => {
        setEpisodes(prev => prev.map(ep =>
            ep.id === currentEpisodeId
                ? {...ep, attendees: [...ep.attendees, ...newAttendees]}
                : ep
        ));
    };

    const getAttendeeById = (attendeeId: number) => {
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
