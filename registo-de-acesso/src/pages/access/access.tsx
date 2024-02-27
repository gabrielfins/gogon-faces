import { useEffect, useState, useMemo } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { AccessService } from '../../services/access-service';
import { Access } from '../../interfaces/access';
import { formatDate, formatMethod, formatTime, formatType } from '../../helpers/access';
import styles from './access.module.scss';

export default function Access() {
  const { state } = useLocation();

  const [access, setAccess] = useState<Access | null>(state);
  
  const params = useParams<{ id: string }>();

  const accessService = useMemo(() => new AccessService(), []);

  useEffect(() => {
    if (access) {
      return;
    }

    if (!params.id) {
      return;
    }

    accessService.get(params.id).then((access) => {
      setAccess(access);
    });
  }, [params.id, accessService, access]);

  if (!access) {
    return null;
  }
  
  return (
    <main className={styles['main']}>
      <h2>Acesso</h2>
      <div className={styles['form-container']}>
        <div className={styles['form-input']}>
          <label htmlFor="date">Data</label>
          <input id="date" type="text" readOnly value={formatDate(access.date)} />
        </div>
        <div className={styles['form-input']}>
          <label htmlFor="date">Hora</label>
          <input id="date" type="text" readOnly value={formatTime(access.date)} />
        </div>
        <div className={styles['form-input']}>
          <label htmlFor="date">Método</label>
          <input id="date" type="text" readOnly value={formatMethod(access.method)} />
        </div>
        <div className={styles['form-input']}>
          <label htmlFor="date">Sala</label>
          <input id="date" type="text" readOnly value={access.room} />
        </div>
        <div className={styles['form-input']}>
          <label htmlFor="date">Tipo</label>
          <input id="date" type="text" readOnly value={formatType(access.type)} />
        </div>
      </div>
    </main>
  );
}
