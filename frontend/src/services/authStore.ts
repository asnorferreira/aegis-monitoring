import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { login as apiLogin } from '../api/authApi';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// Usamos o middleware 'persist' para salvar o token no localStorage automaticamente.
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      isAuthenticated: false,
      login: async (email, password) => {
        const { token } = await apiLogin(email, password);
        set({ token, isAuthenticated: true });
      },
      logout: () => {
        set({ token: null, isAuthenticated: false });
      },
    }),
    {
      name: 'auth-storage', // nome da chave no localStorage
      onRehydrateStorage: () => (state) => {
        // Garante que isAuthenticated seja atualizado quando o estado é carregado do storage
        if (state) {
          state.isAuthenticated = !!state.token;
        }
      },
    }
  )
);

