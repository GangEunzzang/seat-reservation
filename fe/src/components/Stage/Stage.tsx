import type {FC} from 'react';
import './Stage.css';

interface StageProps {
    label?: string;
}

export const Stage: FC<StageProps> = ({label = '무대 / 모니터'}) => {
    return (
        <div className="stage">
            <div className="stage-label">{label}</div>
        </div>
    );
};
