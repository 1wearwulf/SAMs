#!/bin/bash
echo "Building APK..."
cd android

# Disable all problematic plugins temporarily
find ../node_modules -name "build.gradle" -type f -exec sed -i 's/apply plugin: "expo-module-gradle-plugin"//g' {} \;
find ../node_modules -name "build.gradle" -type f -exec sed -i 's/apply plugin: "expo-dev-launcher-gradle-plugin"//g' {} \;

# Build
./gradlew clean
./gradlew :app:assembleDebug 2>&1 | tee build.log

if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
    echo "✅ APK created: $(pwd)/app/build/outputs/apk/debug/app-debug.apk"
    echo "📱 Install with: adb install app/build/outputs/apk/debug/app-debug.apk"
else
    echo "❌ Build failed. Check build.log"
    grep -A5 -B5 "error\|FAILED" build.log
fi
