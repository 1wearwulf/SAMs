import React, { useState, useEffect } from 'react';
import { Text, View, Button, Alert, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';

export default function SimpleQRScanner() {
  const [result, setResult] = useState('');

  const pickImage = async () => {
    // Pick an image from gallery
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      // For now, just show the image URI
      setResult(`Image selected: ${result.assets[0].uri}`);
      Alert.alert('Image Selected', 'In production, this would scan QR from image');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>QR Code Scanner</Text>
      <Text style={styles.subtitle}>
        Note: Camera scanning requires APK build{'\n'}
        For testing, use image picker or mock data
      </Text>
      
      <Button title="Pick Image to Scan QR" onPress={pickImage} />
      
      <View style={styles.mockSection}>
        <Text style={styles.mockTitle}>Test QR Codes:</Text>
        <Text style={styles.mockCode}>• https://your-app.com/auth?token=123</Text>
        <Text style={styles.mockCode}>• {"{\"product\":\"123\",\"name\":\"Test\"}"}</Text>
        <Text style={styles.mockCode}>• PAYMENT:UPI1234567890</Text>
      </View>

      {result ? (
        <View style={styles.resultBox}>
          <Text style={styles.resultText}>Scanned: {result}</Text>
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 10 },
  subtitle: { textAlign: 'center', color: '#666', marginBottom: 30 },
  mockSection: { marginTop: 40, padding: 20, backgroundColor: '#f5f5f5', borderRadius: 10 },
  mockTitle: { fontSize: 18, fontWeight: '600', marginBottom: 10 },
  mockCode: { fontFamily: 'monospace', marginVertical: 5 },
  resultBox: { marginTop: 30, padding: 15, backgroundColor: '#e8f5e8', borderRadius: 8 },
  resultText: { fontFamily: 'monospace', color: '#2e7d32' },
});
