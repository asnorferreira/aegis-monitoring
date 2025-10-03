import { create } from 'zustand';
import { login as apiLogin } from '../api/authApi';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('authToken'),
  isAuthenticated: !!localStorage.getItem('authToken'),
  login: async (email, password) => {
    const { token } = await apiLogin(email, password);
    localStorage.setItem('authToken', token);
    set({ token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('authToken');
    set({ token: null, isAuthenticated: false });
  },
}));
