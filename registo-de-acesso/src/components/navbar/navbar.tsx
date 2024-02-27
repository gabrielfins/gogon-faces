import { Link } from 'react-router-dom';
import styles from './navbar.module.scss';

export default function Navbar() {
  return (
    <nav className={styles['navbar']}>
      <Link to="/" className={styles['link']}>
        <h1>Controle de Acesso</h1>
      </Link>
    </nav>
  );
}
