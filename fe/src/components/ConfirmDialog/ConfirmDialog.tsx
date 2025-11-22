import type {FC, ReactNode} from 'react';
import './ConfirmDialog.css';

interface ConfirmDialogProps {
    isOpen: boolean;
    title: string;
    message: ReactNode;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void;
    onCancel: () => void;
    type?: 'info' | 'warning' | 'danger';
}

export const ConfirmDialog: FC<ConfirmDialogProps> = ({
    isOpen,
    title,
    message,
    confirmText = '확인',
    cancelText = '취소',
    onConfirm,
    onCancel,
    type = 'info'
}) => {
    if (!isOpen) return null;

    return (
        <div className="confirm-overlay" onClick={onCancel}>
            <div className="confirm-dialog" onClick={e => e.stopPropagation()}>
                <div className={`confirm-dialog__icon confirm-dialog__icon--${type}`}>
                    {type === 'info' && '✓'}
                    {type === 'warning' && '!'}
                    {type === 'danger' && '×'}
                </div>

                <div className="confirm-dialog__content">
                    <h3 className="confirm-dialog__title">{title}</h3>
                    <div className="confirm-dialog__message">{message}</div>
                </div>

                <div className="confirm-dialog__actions">
                    <button
                        className="confirm-dialog__button confirm-dialog__button--cancel"
                        onClick={onCancel}
                    >
                        {cancelText}
                    </button>
                    <button
                        className={`confirm-dialog__button confirm-dialog__button--confirm confirm-dialog__button--${type}`}
                        onClick={onConfirm}
                    >
                        {confirmText}
                    </button>
                </div>
            </div>
        </div>
    );
};
