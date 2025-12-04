#!/bin/bash

# ============================================================================
#  SAMS Mobile App - APK Build Script (Improved)
# ============================================================================

set -e  # Exit on any error

GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"

echo -e "${BLUE}🚀 Building SAMS Mobile App APK...${RESET}"

# ----------------------------------------------------------------------------
# 1️⃣ Verify Flutter installation
# ----------------------------------------------------------------------------
if ! command -v flutter &>/dev/null; then
    echo -e "${RED}❌ Flutter is not installed!${RESET}"
    echo "Install Flutter: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# ----------------------------------------------------------------------------
# 2️⃣ Check Android SDK / Install if missing
# ----------------------------------------------------------------------------
if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo -e "${YELLOW}⚠️  Android SDK not found — setting up Android SDK...${RESET}"

    SDK_DIR="$HOME/Android/Sdk"
    mkdir -p "$SDK_DIR"

    export ANDROID_HOME="$SDK_DIR"
    export ANDROID_SDK_ROOT="$SDK_DIR"
    export PATH="$PATH:$SDK_DIR/cmdline-tools/latest/bin:$SDK_DIR/platform-tools"

    echo -e "${BLUE}📥 Downloading Android cmdline-tools...${RESET}"
    cd "$SDK_DIR"
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
    unzip -q cmdline-tools.zip
    rm cmdline-tools.zip
    mkdir -p "$SDK_DIR/cmdline-tools"
    mv cmdline-tools "$SDK_DIR/cmdline-tools/latest"

    echo -e "${BLUE}📦 Installing Android platform-tools & build-tools...${RESET}"
    yes | "$SDK_DIR/cmdline-tools/latest/bin/sdkmanager" --licenses >/dev/null

    "$SDK_DIR/cmdline-tools/latest/bin/sdkmanager" \
        "platform-tools" \
        "platforms;android-34" \
        "build-tools;34.0.0"

    echo -e "${GREEN}✅ Android SDK installed successfully.${RESET}"
fi

# ----------------------------------------------------------------------------
# 3️⃣ Navigate to script directory
# ----------------------------------------------------------------------------
cd "$(dirname "$0")"

# ----------------------------------------------------------------------------
# 4️⃣ Get Flutter dependencies
# ----------------------------------------------------------------------------
echo -e "${BLUE}📦 Installing Flutter dependencies...${RESET}"
flutter pub get

# ----------------------------------------------------------------------------
# 5️⃣ Flutter doctor check
# ----------------------------------------------------------------------------
echo -e "${BLUE}🔧 Checking Flutter setup...${RESET}"
flutter doctor

# ----------------------------------------------------------------------------
# 6️⃣ Run tests only if the test/ folder exists
# ----------------------------------------------------------------------------
echo -e "${BLUE}🧪 Running tests...${RESET}"

if [ -d "test" ]; then
    flutter test || {
        echo -e "${RED}❌ Tests failed. Fix issues before building.${RESET}"
        exit 1
    }
else
    echo -e "${YELLOW}⚠️  No test directory found — skipping tests.${RESET}"
fi

# ----------------------------------------------------------------------------
# 7️⃣ Build APK
# ----------------------------------------------------------------------------
echo -e "${BLUE}🏗️  Building APK...${RESET}"

flutter build apk --release

APK_PATH="build/app/outputs/flutter-apk/app-release.apk"

if [ ! -f "$APK_PATH" ]; then
    echo -e "${RED}❌ APK build failed — file not found.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ APK built successfully!${RESET}"
echo -e "📱 APK location: ${YELLOW}$APK_PATH${RESET}"
echo -e "📊 APK size: ${GREEN}$(du -h "$APK_PATH" | cut -f1)${RESET}"

# ----------------------------------------------------------------------------
# 8️⃣ Copy APK to project root
# ----------------------------------------------------------------------------
DEST="../../sams-mobile-v1.0.0.apk"
cp "$APK_PATH" "$DEST"

echo -e "📋 APK copied to: ${GREEN}$DEST${RESET}"

echo -e "\n${GREEN}🎉 Build complete!${RESET}"
echo "📋 Next steps:"
echo "   1. Transfer the APK to your Android device"
echo "   2. Enable 'Install from unknown sources'"
echo "   3. Install the APK"
echo "   4. Launch SAMS and configure API endpoint"

