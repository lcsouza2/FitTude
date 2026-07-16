import { View, Text } from "react-native";

export default function MuscleGroupIndex() {
  return (
    <View className="flex-1 justify-center items-center bg-appBackground dark:bg-appBackground-dark">
      <Text className="text-2xl font-bold text-appText dark:text-appText-dark mb-4">
        Muscle Group Index
      </Text>
      <View className="px-6 py-3 rounded-xl bg-button dark:bg-button-dark">
        <Text className="font-semibold text-buttonText dark:text-buttonText-dark">
          Explore Muscle Groups
        </Text>
      </View>
    </View>
  );
}
