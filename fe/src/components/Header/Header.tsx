import type {FC} from 'react';
import './Header.css';

interface HeaderProps {
    title: string;
}

export const Header: FC<HeaderProps> = ({title}) => {
    return (
        <header className="header">
            <h1>{title}</h1>
        </header>
    );
};
