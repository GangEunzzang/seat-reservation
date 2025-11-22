import {type FC, useRef, useState} from 'react';
import * as XLSX from 'xlsx';
import {X, Upload, AlertCircle} from 'lucide-react';
import type {Attendee} from '../../types';
import {userApi, type UserRegisterRequest} from '../../api';
import './ExcelUpload.css';

interface ExcelUploadProps {
    episodeId: number;
    onUploadSuccess: () => void;
    onClose: () => void;
}

export const ExcelUpload: FC<ExcelUploadProps> = ({episodeId, onUploadSuccess, onClose}) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [error, setError] = useState<string | null>(null);
    const [preview, setPreview] = useState<Attendee[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setIsLoading(true);
        setError(null);

        try {
            const data = await file.arrayBuffer();
            const workbook = XLSX.read(data);
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json<{
                지점명?: string;
                이름?: string;
                포지션?: string;
                직책?: string;
                직급?: string;
                핸드폰번호?: string;
                핸드폰?: string;
                전화번호?: string;
                연락처?: string;
                [key: string]: unknown;
            }>(worksheet);

            if (jsonData.length === 0) {
                setError('엑셀 파일이 비어있습니다.');
                setIsLoading(false);
                return;
            }

            const attendees: Attendee[] = [];
            const errors: string[] = [];

            jsonData.forEach((row, index) => {
                const branchName = row['지점명'] || row['지점'] || '';
                const name = row['이름'] || '';
                const position = row['포지션'] || row['직책'] || row['직급'] || '';
                const phoneNumber = row['핸드폰번호'] || row['핸드폰'] || row['전화번호'] || row['연락처'] || '';

                if (!branchName || !name) {
                    errors.push(`${index + 2}번째 행: 지점명 또는 이름이 누락되었습니다.`);
                    return;
                }

                if (!position) {
                    errors.push(`${index + 2}번째 행: 포지션(직책)이 누락되었습니다.`);
                    return;
                }

                if (!phoneNumber) {
                    errors.push(`${index + 2}번째 행: 핸드폰번호가 누락되었습니다.`);
                    return;
                }

                attendees.push({
                    id: `${Date.now()}-${index}`,
                    branchName: String(branchName).trim(),
                    name: String(name).trim(),
                    position: String(position).trim(),
                    phoneNumber: String(phoneNumber).trim(),
                });
            });

            if (errors.length > 0) {
                setError(`데이터 오류:\n${errors.slice(0, 5).join('\n')}${errors.length > 5 ? `\n외 ${errors.length - 5}건` : ''}`);
            }

            if (attendees.length > 0) {
                setPreview(attendees);
            } else {
                setError('유효한 참석자 데이터가 없습니다.');
            }
        } catch (err) {
            setError('엑셀 파일을 읽는 중 오류가 발생했습니다.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpload = async () => {
        if (preview.length === 0) return;

        setIsUploading(true);
        setError(null);

        try {
            const requests: UserRegisterRequest[] = preview.map(attendee => ({
                name: attendee.name,
                department: attendee.branchName,
                position: attendee.position,
                phone_number: attendee.phoneNumber,
                episode_id: episodeId,
            }));

            await userApi.registerBulk(requests);
            onUploadSuccess();
            onClose();
        } catch (err) {
            if (err instanceof Error) {
                setError(`업로드 실패: ${err.message}`);
            } else {
                setError('업로드 중 오류가 발생했습니다.');
            }
            console.error(err);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="excel-upload-overlay" onClick={onClose}>
            <div className="excel-upload-modal" onClick={(e) => e.stopPropagation()}>
                <div className="excel-upload-modal__header">
                    <h2>참석자 명단 업로드</h2>
                    <button className="excel-upload-modal__close" onClick={onClose}>
                        <X size={20}/>
                    </button>
                </div>

                <div className="excel-upload-modal__body">
                    <div className="excel-upload-modal__info">
                        <p>엑셀 파일에 다음 컬럼이 포함되어야 합니다:</p>
                        <ul>
                            <li><strong>지점명</strong>: 참석자의 지점</li>
                            <li><strong>이름</strong>: 참석자 이름</li>
                            <li><strong>포지션</strong>: 직책 또는 직급</li>
                            <li><strong>핸드폰번호</strong>: 연락처</li>
                        </ul>
                    </div>

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".xlsx,.xls"
                        onChange={handleFileChange}
                        style={{display: 'none'}}
                    />

                    <button
                        className="excel-upload-modal__button"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={isLoading || isUploading}
                    >
                        <Upload size={18}/>
                        {isLoading ? '읽는 중...' : '엑셀 파일 선택'}
                    </button>

                    {error && (
                        <div className="excel-upload-modal__error">
                            <AlertCircle size={16}/>
                            <span>{error}</span>
                        </div>
                    )}

                    {preview.length > 0 && (
                        <div className="excel-upload-modal__preview">
                            <h3>미리보기 ({preview.length}명)</h3>
                            <div className="excel-upload-modal__preview-list">
                                {preview.slice(0, 10).map((attendee) => (
                                    <div key={attendee.id} className="excel-upload-modal__preview-item">
                                        <div className="excel-upload-modal__preview-main">
                                            <span className="branch">{attendee.branchName}</span>
                                            <span className="name">{attendee.name}</span>
                                            <span className="position">{attendee.position}</span>
                                        </div>
                                        <span className="phone">{attendee.phoneNumber}</span>
                                    </div>
                                ))}
                                {preview.length > 10 && (
                                    <div className="excel-upload-modal__preview-more">
                                        외 {preview.length - 10}명
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                <div className="excel-upload-modal__footer">
                    <button onClick={onClose} disabled={isUploading}>취소</button>
                    <button
                        onClick={handleUpload}
                        disabled={preview.length === 0 || isUploading}
                        className="excel-upload-modal__footer-submit"
                    >
                        {isUploading ? '업로드 중...' : `업로드 (${preview.length}명)`}
                    </button>
                </div>
            </div>
        </div>
    );
};
