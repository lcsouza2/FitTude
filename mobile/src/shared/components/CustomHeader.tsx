import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { useAppColors } from '../../hooks/use-app-colors';

export default function CustomHeader(props: any) {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const colors = useAppColors();

  const isDashboard = props.route.name === 'index';
  const title = props.options.title ?? props.route.name;

  const handleLeftButtonPress = () => {
    if (isDashboard) {
      props.navigation.openDrawer();
    } else {
      router.push('/');
    }
  };

  return (
    <View
      style={{
        paddingTop: insets.top,
        backgroundColor: colors.card,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
      }}
      className="flex-row px-4 pb-3"
    >
      {/* Left Icon Button */}
      <View className="flex-1 items-start flex-row gap-3">
        <TouchableOpacity
          onPress={handleLeftButtonPress}
          className="p-2 rounded-lg bg-appBackground dark:bg-appBackground-dark border border-appBorder dark:border-appBorder-dark"
        >
          {isDashboard ? (
            <Feather name="menu" size={20} color={colors.text} />
          ) : (
            <Feather name="arrow-left" size={20} color={colors.text} />
          )}
        </TouchableOpacity>

        {/* Center Title + Logo */}
        <View>
          <Text className="text-xl font-bold text-appText dark:text-appText-dark">
            {title}
          </Text>
          <Text className="text-xs font-black tracking-wider text-appTextSecondary dark:text-appTextSecondary-dark uppercase opacity-60">
            OVERLOAD
          </Text>
        </View>
      </View>

      {/* Right Placeholder to balance layout */}
      <View className="flex-1 items-end" />
    </View>
  );
}
