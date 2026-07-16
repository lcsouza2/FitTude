import { View, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView edges={['bottom', 'left', 'right']} className="flex-1 justify-center items-center bg-appBackground dark:bg-appBackground-dark">
      <Text className="text-2xl font-bold text-appText dark:text-appText-dark mb-4">
        Welcome to Overload!
      </Text>
      <View className="px-6 py-3 rounded-xl bg-button dark:bg-button-dark">
        <Text className="font-semibold text-buttonText dark:text-buttonText-dark">
          Get Started
        </Text>
      </View>
    </SafeAreaView>
  );
}