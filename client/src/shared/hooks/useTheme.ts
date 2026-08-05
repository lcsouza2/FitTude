import { useState, useEffect, useCallback } from 'react';

export interface ThemeColors {
  background: string;
  surface: string;
  primary: string;
  primaryHover: string;
  secondary: string;
  text: string;
  textSecondary: string;
  border: string;
  button: string;
  buttonHover: string;
  buttonText: string;
  card: string;
  cardBorder: string;
  success: string;
  error: string;
  warning: string;
}

export type ThemeMode = 'light' | 'dark' | 'system';

export const lightTheme: ThemeColors = {
  background: '#F8FAFC',
  surface: '#FFFFFF',
  primary: '#2563EB',
  primaryHover: '#1D4ED8',
  secondary: '#4F46E5',
  text: '#0F172A',
  textSecondary: '#64748B',
  border: '#E2E8F0',
  button: '#2563EB',
  buttonHover: '#1D4ED8',
  buttonText: '#FFFFFF',
  card: '#FFFFFF',
  cardBorder: '#E2E8F0',
  success: '#16A34A',
  error: '#DC2626',
  warning: '#D97706',
};

export const darkTheme: ThemeColors = {
  background: '#0F172A',
  surface: '#1E293B',
  primary: '#3B82F6',
  primaryHover: '#60A5FA',
  secondary: '#6366F1',
  text: '#F8FAFC',
  textSecondary: '#94A3B8',
  border: '#334155',
  button: '#3B82F6',
  buttonHover: '#60A5FA',
  buttonText: '#FFFFFF',
  card: '#1E293B',
  cardBorder: '#334155',
  success: '#22C55E',
  error: '#EF4444',
  warning: '#F59E0B',
};

const THEME_STORAGE_KEY = 'overload_theme_mode';

function getSystemIsDark(): boolean {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

function getStoredTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'system';
  const stored = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode | null;
  if (stored && ['light', 'dark', 'system'].includes(stored)) {
    return stored;
  }
  return 'system';
}

function applyThemeVariables(colors: ThemeColors, isDark: boolean) {
  if (typeof document === 'undefined') return;

  const root = document.documentElement;

  if (isDark) {
    root.classList.add('dark');
  } else {
    root.classList.remove('dark');
  }

  // Injeta variáveis CSS no :root (ex: --color-background, --color-text-secondary)
  Object.entries(colors).forEach(([key, value]) => {
    const cssVarName = `--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
    root.style.setProperty(cssVarName, value);
  });
}

export function useTheme() {
  const [theme, setThemeState] = useState<ThemeMode>(getStoredTheme);
  const [systemIsDark, setSystemIsDark] = useState<boolean>(getSystemIsDark);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      setSystemIsDark(e.matches);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const isDark = theme === 'system' ? systemIsDark : theme === 'dark';

  const setTheme = useCallback((newTheme: ThemeMode) => {
    setThemeState(newTheme);
    localStorage.setItem(THEME_STORAGE_KEY, newTheme);
  }, []);

  const toggleTheme = useCallback(() => {
    setThemeState((prev) => {
      const nextTheme: ThemeMode =
        prev === 'light'
          ? 'dark'
          : prev === 'dark'
          ? 'light'
          : getSystemIsDark()
          ? 'light'
          : 'dark';
      localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
      return nextTheme;
    });
  }, []);

  useEffect(() => {
    const activePalette = isDark ? darkTheme : lightTheme;
    applyThemeVariables(activePalette, isDark);
  }, [isDark]);

  return {
    light: lightTheme,
    dark: darkTheme,
    theme,
    setTheme,
    toggleTheme,
  };
}
