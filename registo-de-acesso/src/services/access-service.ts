import { get, push, query, ref } from 'firebase/database';
import { database } from './firebase-service';
import { Access } from '../interfaces/access';

export class AccessService {
  private readonly path: string = 'access';

  async add(access: Access): Promise<void> {
    await push(ref(database, this.path), access);
  }

  async get(id: string): Promise<Access> {
    const snapshot = await get(query(ref(database, `${this.path}/${id}`)));
    return snapshot.val();
  }

  watch() {
    return ref(database, this.path);
  }
}
