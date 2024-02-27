import { createContext, useState, ReactNode } from 'react';
import { Access } from '../interfaces/access';

type AccessContextType = {
  access: Record<string, Access>;
  setAccess: (access: Record<string, Access>) => void;
};

export const AccessContext = createContext<AccessContextType>({} as AccessContextType);

export function AccessContextProvider({ children }: { children: ReactNode }) {
  const [access, setAccess] = useState<Record<string, Access>>({});

  return (
    <AccessContext.Provider value={{ access, setAccess }}>
      {children}
    </AccessContext.Provider>
  );
}
