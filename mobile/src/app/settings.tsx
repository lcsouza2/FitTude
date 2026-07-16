import { View, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function SettingsScreen() {
  return (
    <SafeAreaView edges={['bottom', 'left', 'right']} className="flex-1 justify-center items-center bg-appBackground dark:bg-appBackground-dark">
      <Text className="text-2xl font-bold text-appText dark:text-appText-dark mb-4">
        Settings Screen
      </Text>
      <Text className="text-appTextSecondary dark:text-appTextSecondary-dark text-center px-8">
        Customize your theme, dashboard layout, and other application configurations.
      </Text>
    </SafeAreaView>
  );
}
