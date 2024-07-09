import { useState, useEffect } from 'react';

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface DjangoContext {
  user?: User;
  devices?: any[];
  categories?: any[];
}

let djangoContext: DjangoContext | null = null;

export function initializeDjangoContext(): void {
  if (typeof window !== 'undefined') {
    const storedContext = sessionStorage.getItem('djangoContext');
    if (storedContext) {
      try {
        djangoContext = JSON.parse(storedContext);
      } catch (error) {
        console.error('Error parsing Django context from sessionStorage:', error);
      }
    }
  }
}

export function useDjangoContext<T extends keyof DjangoContext>(key: T): DjangoContext[T] | undefined {
  const [value, setValue] = useState<DjangoContext[T] | undefined>(undefined);

  useEffect(() => {
    if (!djangoContext) {
      initializeDjangoContext();
    }
    setValue(djangoContext ? djangoContext[key] : undefined);
  }, [key]);

  return value;
}
