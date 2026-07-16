import { useColorScheme } from 'react-native';

export const Colors = {
  light: {
    primary: '#7C3AED', // Vibrant Purple
    background: '#F8FAFC', // Slate-50 (off-white for eye comfort)
    text: '#0F172A', // Slate-900 (high contrast)
    textSecondary: '#475569', // Slate-600
    button: '#FF6B00', // Neon Orange
    buttonText: '#FFFFFF',
    border: '#E2E8F0', // Slate-200
    card: '#FFFFFF', // Pure White for widgets to pop from background
    accent: '#84CC16', // Neon Lime Green
  },
  dark: {
    primary: '#6C4FB3', // Muted Purple
    background: '#0B0F19', // Deep Blue-Black Slate (extremely soft on eyes)
    text: '#E2E8F0', // Soft White (reduces glare)
    textSecondary: '#94A3B8', // Muted Slate Grey
    button: '#D25D12', // Muted Burnt Orange
    buttonText: '#F1F5F9',
    border: '#1E293B', // Slate-800
    card: '#131C2E', // Elevated Slate-Blue (helps widget traceability)
    accent: '#557A1E', // Muted Lime Green
  },
} as const;

export function useAppColors() {
  const scheme = useColorScheme();
  const theme = scheme === 'dark' ? 'dark' : 'light';
  return Colors[theme];
}
