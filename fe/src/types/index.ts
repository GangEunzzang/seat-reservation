export interface Seat {
    id: string;
    tableId: string;
    seatNumber: number;
    isReserved: boolean;
    reservedBy?: string;
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
}
