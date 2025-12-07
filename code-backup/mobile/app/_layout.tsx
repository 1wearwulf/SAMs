import { Stack } from "expo-router";
import { useStore } from "./store/useStore";
import { ActivityIndicator, View } from "react-native";
import { useEffect, useState } from "react";

export default function RootLayout() {
  const { user } = useStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading check
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#6200ee" />
      </View>
    );
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      {!user ? (
        <Stack.Screen name="login" />
      ) : (
        <>
          <Stack.Screen name="(tabs)" />
          <Stack.Screen 
            name="attendance" 
            options={{ 
              title: "Attendance Records",
              presentation: "modal"
            }} 
          />
        </>
      )}
    </Stack>
  );
}
