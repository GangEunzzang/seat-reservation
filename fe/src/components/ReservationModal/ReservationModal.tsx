import {useState, useMemo, useRef, useEffect} from 'react';
import type {FC} from 'react';
import type {Seat, Attendee} from '../../types';
import {ConfirmDialog} from '../ConfirmDialog';
import './ReservationModal.css';

interface ReservationModalProps {
    seat: Seat;
    attendees: Attendee[];
    availableAttendees: Attendee[];
    getAttendeeById: (id: string) => Attendee | undefined;
    onReserve: (attendeeId: string) => void;
    onCancel: () => void;
    onClose: () => void;
}

export const ReservationModal: FC<ReservationModalProps> = ({
                                                                seat,
                                                                attendees,
                                                                availableAttendees,
                                                                getAttendeeById,
                                                                onReserve,
                                                                onCancel,
                                                                onClose,
                                                            }) => {
    const [selectedAttendeeId, setSelectedAttendeeId] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [showResults, setShowResults] = useState(false);
    const [focusedIndex, setFocusedIndex] = useState(-1);
    const [showConfirm, setShowConfirm] = useState(false);
    const [confirmType, setConfirmType] = useState<'reserve' | 'cancel'>('reserve');
    const searchWrapperRef = useRef<HTMLDivElement>(null);
    const resultRefs = useRef<(HTMLButtonElement | null)[]>([]);

    // 외부 클릭 시 결과창 닫기
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (searchWrapperRef.current && !searchWrapperRef.current.contains(event.target as Node)) {
                setShowResults(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    // 검색어로 필터링
    const filteredAttendees = useMemo(() => {
        if (!searchQuery.trim()) {
            return []; // 검색 전에는 결과 안 보여줌
        }

        const query = searchQuery.toLowerCase().trim();
        return availableAttendees.filter(attendee => {
            const branchMatch = attendee.branchName.toLowerCase().includes(query);
            const nameMatch = attendee.name.toLowerCase().includes(query);
            const positionMatch = attendee.position.toLowerCase().includes(query);
            return branchMatch || nameMatch || positionMatch;
        }).slice(0, 8); // 검색 결과는 최대 8개만
    }, [searchQuery, availableAttendees]);

    const selectedAttendee = selectedAttendeeId ? getAttendeeById(selectedAttendeeId) : null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (selectedAttendeeId && selectedAttendee) {
            setConfirmType('reserve');
            setShowConfirm(true);
        }
    };

    const handleConfirmReserve = () => {
        if (selectedAttendeeId) {
            onReserve(selectedAttendeeId);
            setShowConfirm(false);
        }
    };

    const handleConfirmCancel = () => {
        onCancel();
        setShowConfirm(false);
    };

    const handleSelectAttendee = (attendee: Attendee) => {
        setSelectedAttendeeId(attendee.id);
        setSearchQuery(`${attendee.branchName} - ${attendee.name}`);
        setShowResults(false);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // 한글 입력 조합 중일 때는 무시
        if (e.nativeEvent.isComposing) return;

        if (!showResults || filteredAttendees.length === 0) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                setFocusedIndex(prev => {
                    const nextIndex = prev < filteredAttendees.length - 1 ? prev + 1 : 0;
                    // 스크롤 처리
                    setTimeout(() => {
                        resultRefs.current[nextIndex]?.scrollIntoView({
                            block: 'nearest',
                            behavior: 'smooth'
                        });
                    }, 0);
                    return nextIndex;
                });
                break;

            case 'ArrowUp':
                e.preventDefault();
                setFocusedIndex(prev => {
                    const nextIndex = prev > 0 ? prev - 1 : filteredAttendees.length - 1;
                    // 스크롤 처리
                    setTimeout(() => {
                        resultRefs.current[nextIndex]?.scrollIntoView({
                            block: 'nearest',
                            behavior: 'smooth'
                        });
                    }, 0);
                    return nextIndex;
                });
                break;

            case 'Enter':
                e.preventDefault();
                if (focusedIndex >= 0 && focusedIndex < filteredAttendees.length) {
                    handleSelectAttendee(filteredAttendees[focusedIndex]);
                }
                break;

            case 'Escape':
                e.preventDefault();
                setShowResults(false);
                setFocusedIndex(-1);
                break;
        }
    };

    // 검색어 변경 시 포커스 인덱스 초기화 및 자동 선택
    useEffect(() => {
        if (searchQuery.trim() && filteredAttendees.length > 0) {
            setFocusedIndex(0);
        } else {
            setFocusedIndex(-1);
        }
    }, [searchQuery, filteredAttendees.length]);

    const reservedAttendee = seat.attendeeId ? getAttendeeById(seat.attendeeId) : null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={e => e.stopPropagation()}>
                <div className="modal__header">
                    <h3>좌석 {seat.seatNumber}</h3>
                    <button className="modal__close" onClick={onClose}>✕</button>
                </div>

                {seat.isReserved ? (
                    <div className="modal__content">
                        {reservedAttendee ? (
                            <>
                                <p>현재 예약자</p>
                                <div className="modal__reserved-info">
                                    <span className="modal__branch">{reservedAttendee.branchName}</span>
                                    <span className="modal__name">{reservedAttendee.name}</span>
                                    <span className="modal__position">{reservedAttendee.position}</span>
                                </div>
                            </>
                        ) : (
                            <p>예약 정보를 찾을 수 없습니다.</p>
                        )}
                        <button
                            className="modal__cancel-btn"
                            onClick={() => {
                                setConfirmType('cancel');
                                setShowConfirm(true);
                            }}
                        >
                            예약 취소
                        </button>
                    </div>
                ) : (
                    <form className="modal__content" onSubmit={handleSubmit}>
                        <label htmlFor="attendee">참석자 검색</label>
                        {attendees.length === 0 ? (
                            <div className="modal__no-attendees">
                                <p>등록된 참석자가 없습니다.</p>
                                <p className="modal__hint">사이드바에서 참석자 명단을 먼저 업로드해주세요.</p>
                            </div>
                        ) : availableAttendees.length === 0 ? (
                            <div className="modal__no-attendees">
                                <p>예약 가능한 참석자가 없습니다.</p>
                                <p className="modal__hint">모든 참석자가 이미 예약되었습니다.</p>
                            </div>
                        ) : (
                            <>
                                <div className="modal__search-wrapper" ref={searchWrapperRef}>
                                    <input
                                        id="attendee"
                                        type="text"
                                        placeholder="이름 또는 지점으로 검색"
                                        value={searchQuery}
                                        onChange={e => {
                                            setSearchQuery(e.target.value);
                                            setShowResults(true);
                                            if (!e.target.value.trim()) {
                                                setSelectedAttendeeId('');
                                            }
                                        }}
                                        onFocus={() => setShowResults(true)}
                                        onKeyDown={handleKeyDown}
                                        autoFocus
                                        autoComplete="off"
                                    />

                                    {selectedAttendee && !showResults && (
                                        <div className="modal__selected-preview">
                                            <span className="modal__selected-branch">{selectedAttendee.branchName}</span>
                                            <span className="modal__selected-name">{selectedAttendee.name}</span>
                                            <span className="modal__selected-position">{selectedAttendee.position}</span>
                                        </div>
                                    )}

                                    {showResults && filteredAttendees.length > 0 && (
                                        <div className="modal__search-results">
                                            {filteredAttendees.map((attendee, index) => (
                                                <button
                                                    key={attendee.id}
                                                    ref={el => resultRefs.current[index] = el}
                                                    type="button"
                                                    className={`modal__search-result-item ${index === focusedIndex ? 'modal__search-result-item--focused' : ''}`}
                                                    onClick={() => handleSelectAttendee(attendee)}
                                                    onMouseEnter={() => setFocusedIndex(index)}
                                                >
                                                    <div className="modal__result-main">
                                                        <span className="modal__result-branch">{attendee.branchName}</span>
                                                        <span className="modal__result-name">{attendee.name}</span>
                                                        <span className="modal__result-position">{attendee.position}</span>
                                                    </div>
                                                </button>
                                            ))}
                                        </div>
                                    )}

                                    {showResults && searchQuery.trim() && filteredAttendees.length === 0 && (
                                        <div className="modal__no-results">
                                            검색 결과가 없습니다.
                                        </div>
                                    )}
                                </div>

                                <button type="submit" className="modal__reserve-btn" disabled={!selectedAttendeeId}>
                                    예약하기
                                </button>
                            </>
                        )}
                    </form>
                )}

                <ConfirmDialog
                    isOpen={showConfirm}
                    title={confirmType === 'reserve' ? '좌석 예약' : '예약 취소'}
                    message={
                        confirmType === 'reserve' && selectedAttendee ? (
                            <>
                                <div>좌석 {seat.seatNumber}번을 예약하시겠습니까?</div>
                                <div className="confirm-dialog__message-detail">
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">지점</span>
                                        <span className="confirm-dialog__message-badge">{selectedAttendee.branchName}</span>
                                    </div>
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">이름</span>
                                        <span className="confirm-dialog__message-value">{selectedAttendee.name}</span>
                                    </div>
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">포지션</span>
                                        <span className="confirm-dialog__message-value">{selectedAttendee.position}</span>
                                    </div>
                                </div>
                            </>
                        ) : reservedAttendee ? (
                            <>
                                <div>예약을 취소하시겠습니까?</div>
                                <div className="confirm-dialog__message-detail">
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">지점</span>
                                        <span className="confirm-dialog__message-badge">{reservedAttendee.branchName}</span>
                                    </div>
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">이름</span>
                                        <span className="confirm-dialog__message-value">{reservedAttendee.name}</span>
                                    </div>
                                    <div className="confirm-dialog__message-row">
                                        <span className="confirm-dialog__message-label">좌석</span>
                                        <span className="confirm-dialog__message-value">{seat.seatNumber}번</span>
                                    </div>
                                </div>
                            </>
                        ) : (
                            '정보를 찾을 수 없습니다.'
                        )
                    }
                    confirmText={confirmType === 'reserve' ? '예약하기' : '취소하기'}
                    cancelText="돌아가기"
                    type={confirmType === 'reserve' ? 'info' : 'danger'}
                    onConfirm={confirmType === 'reserve' ? handleConfirmReserve : handleConfirmCancel}
                    onCancel={() => setShowConfirm(false)}
                />
            </div>
        </div>
    );
};
