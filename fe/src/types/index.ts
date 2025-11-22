export interface Attendee {
    id: number;                // 백엔드 User ID
    branchName: string;
    name: string;
    position: string;
    phoneNumber: string;
}

export interface Seat {
    id: number;                // 백엔드 Seat ID
    tableId: number;           // 백엔드 Table ID
    seatNumber: number;
    isReserved: boolean;
    attendeeId?: number;       // 예약한 Attendee의 백엔드 User ID
    reservationId?: number;    // 백엔드 Reservation ID
}

export interface ZoneInfo {
    id: string;                // UI용 Zone ID (A, B, C, D)
    name: string;
}

export interface Table {
    id: number;                // 백엔드 Table ID
    x: number;
    y: number;
    seatCount: number;
    name: string;
    seats: Seat[];
    zoneId: string;            // UI용 Zone ID
}

export interface Episode {
    id: number;                // 백엔드 Episode ID
    name: string;
    year: number;
    startDate: string;
    endDate: string;
    tables: Table[];
    zones: ZoneInfo[];
    attendees: Attendee[];
}
