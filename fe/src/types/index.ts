export interface Attendee {
    id: string;
    branchName: string;
    name: string;
    position: string;
    phoneNumber: string;
}

export interface Seat {
    id: string;
    tableId: string;
    seatNumber: number;
    isReserved: boolean;
    attendeeId?: string;
}

export interface ZoneInfo {
    id: string;
    name: string;
}

export interface Table {
    id: string;
    x: number;
    y: number;
    seatCount: number;
    name: string;
    seats: Seat[];
    zoneId: string;
}

export interface Episode {
    id: string;
    name: string;
    tables: Table[];
    zones: ZoneInfo[];
    attendees: Attendee[];
}
