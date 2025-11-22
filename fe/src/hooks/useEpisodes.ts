import {useState, useEffect} from 'react';
import type {Episode, Table, Seat, ZoneInfo, Attendee} from '../types';
import {tableApi, seatApi, reservationApi, episodeApi, zoneApi} from '../api';

export const useEpisodes = () => {
    const [episodes, setEpisodes] = useState<Episode[]>([]);
    const [currentEpisodeId, setCurrentEpisodeId] = useState<number | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // 백엔드에서 Episode와 Zone 정보 불러오기
    useEffect(() => {
        const loadEpisodes = async () => {
            try {
                const episodeList = await episodeApi.list();

                const episodesWithZones = await Promise.all(
                    episodeList.map(async (ep) => {
                        const zones = await zoneApi.listByEpisode(ep.id);
                        const zoneInfos: ZoneInfo[] = zones.map(z => ({
                            id: z.code,           // 'A', 'B', 'C', 'D'
                            backendId: z.id,      // 1, 2, 3, 4
                            name: z.name,         // 'A구역', 'B구역', ...
                        }));

                        return {
                            id: ep.id,
                            name: ep.name,
                            year: ep.year,
                            startDate: ep.start_date,
                            endDate: ep.end_date,
                            tables: [],
                            zones: zoneInfos,
                            attendees: []
                        };
                    })
                );

                setEpisodes(episodesWithZones);
                if (episodesWithZones.length > 0) {
                    setCurrentEpisodeId(episodesWithZones[0].id);
                }
            } catch (error) {
                console.error('Episode 로딩 실패:', error);
            } finally {
                setIsLoading(false);
            }
        };

        loadEpisodes();
    }, []);

    const currentEpisode = episodes.find(ep => ep.id === currentEpisodeId);
    const tables = currentEpisode?.tables || [];
    const zones = currentEpisode?.zones || [];
    const attendees = currentEpisode?.attendees || [];

    const addEpisode = async (name: string, year: number, startDate: string, endDate: string) => {
        try {
            // 백엔드에 Episode 생성 (Zone이 자동으로 생성됨)
            const newEpisode = await episodeApi.create({
                name,
                year,
                start_date: startDate,
                end_date: endDate,
            });

            // 생성된 Episode의 Zone 정보 불러오기
            const zones = await zoneApi.listByEpisode(newEpisode.id);
            const zoneInfos: ZoneInfo[] = zones.map(z => ({
                id: z.code,
                backendId: z.id,
                name: z.name,
            }));

            // Episode 목록에 추가
            const episodeWithZones: Episode = {
                id: newEpisode.id,
                name: newEpisode.name,
                year: newEpisode.year,
                startDate: newEpisode.start_date,
                endDate: newEpisode.end_date,
                tables: [],
                zones: zoneInfos,
                attendees: []
            };

            setEpisodes(prev => [...prev, episodeWithZones]);
            setCurrentEpisodeId(newEpisode.id);
        } catch (error) {
            console.error('Episode 생성 실패:', error);
            throw error;
        }
    };

    const addZone = (_name: string) => {
        // TODO: 백엔드 Zone API 연동 필요
        console.warn('Zone 생성은 아직 백엔드와 연동되지 않았습니다. Episode 생성 시 기본 Zone(A,B,C,D)이 자동 생성됩니다.');
    };

    const deleteZone = (_zoneId: string) => {
        // TODO: 백엔드 Zone API 연동 필요
        console.warn('Zone 삭제는 아직 백엔드와 연동되지 않았습니다.');
    };

    const addTable = async (zoneId: string = 'A') => {
        const episode = episodes.find(ep => ep.id === currentEpisodeId);
        if (!episode) {
            console.error('현재 Episode를 찾을 수 없습니다.');
            return;
        }

        try {
            const seatCount = 8;
            const zone = zones.find(z => z.id === zoneId);
            const zoneName = zone?.name || zoneId;
            const zoneTableCount = tables.filter(t => t.zoneId === zoneId).length;

            // Zone이 없으면 에러
            if (!zone) {
                console.error(`Zone ${zoneId}를 찾을 수 없습니다.`);
                return;
            }

            // 테이블 초기 위치 계산
            const x = 100 + (zoneTableCount % 5) * 180;
            const y = 50 + Math.floor(zoneTableCount / 5) * 180;
            const name = `${zoneName}-${zoneTableCount + 1}`;

            // 백엔드에 테이블 생성 (zone_id, x, y, name 포함)
            const tableResponse = await tableApi.create({
                episode_id: episode.id,
                zone_id: zone.backendId,
                x,
                y,
                name,
            });

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
                x: tableResponse.x,
                y: tableResponse.y,
                seatCount,
                name: tableResponse.name,
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

    const updateTablePosition = async (id: number, x: number, y: number) => {
        try {
            // 백엔드에 테이블 위치 업데이트
            await tableApi.updatePosition(id, {x, y});

            // 프론트엔드 상태 업데이트
            setEpisodes(prev => prev.map(ep =>
                ep.id === currentEpisodeId
                    ? {
                        ...ep,
                        tables: ep.tables.map(t => t.id === id ? {...t, x, y} : t)
                    }
                    : ep
            ));
        } catch (error) {
            console.error('테이블 위치 업데이트 실패:', error);
            throw error;
        }
    };

    const updateTableSeatCount = async (_id: number, _seatCount: number) => {
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
        isLoading,
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
