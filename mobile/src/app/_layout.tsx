import 'react-native-gesture-handler';
import { Drawer } from 'expo-router/drawer';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { useAppColors } from '../hooks/use-app-colors';
import CustomHeader from '@/shared/components/CustomHeader';
import '../global.css';

export default function RootLayout() {
  const colors = useAppColors();

  return (
    <SafeAreaProvider>
      <Drawer
        screenOptions={{
          header: (props) => <CustomHeader {...props} />,
          drawerStyle: {
            backgroundColor: colors.background,
            width: 280,
          },
          drawerActiveTintColor: colors.primary,
          drawerInactiveTintColor: colors.textSecondary,
          drawerActiveBackgroundColor: colors.card,
          drawerContentContainerStyle: {
            paddingTop: 40,
          },
        }}
      >
        <Drawer.Screen
          name="index"
          options={{
            drawerLabel: 'Home',
            title: 'Home',
          }}
        />
        <Drawer.Screen
          name="settings"
          options={{
            drawerLabel: 'Settings',
            title: 'Settings',
          }}
        />
      </Drawer>
    </SafeAreaProvider>
  );
}
