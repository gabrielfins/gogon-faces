import { useEffect, useContext, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { onValue } from 'firebase/database';
import { AccessService } from '../../services/access-service';
import styles from './home.module.scss';
import { formatDate, formatMethod, formatTime, formatType } from '../../helpers/access';
import { AccessContext } from '../../contexts/access-context';

export default function Home() {
  const { access, setAccess } = useContext(AccessContext);

  const navigate = useNavigate();

  const accessService = useMemo(() => new AccessService(), []);

  useEffect(() => {
    const unsubscribe = onValue(accessService.watch(), (snapshot) => {
      setAccess(snapshot.val());
    });

    return unsubscribe;
  }, [accessService, setAccess]);

  return (
    <main className={styles['main']}>
      <div className={styles['table-container']}>
        <table className={styles['table']}>
          <thead>
            <tr className={styles['tr']}>
              <th>Data</th>
              <th>Hora</th>
              <th>Método</th>
              <th>Sala</th>
              <th>Tipo</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(access).map(([key, value]) => (
              <tr key={key} className={styles['tr']} onClick={() => navigate(`access/${key}`, { state: value })}>
                <td>{formatDate(value.date)}</td>
                <td>{formatTime(value.date)}</td>
                <td>{formatMethod(value.method)}</td>
                <td>{value.room}</td>
                <td>{formatType(value.type)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
