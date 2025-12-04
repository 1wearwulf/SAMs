import React from 'react';
import { View, StyleSheet, Text, Button } from 'react-native';
import { useDispatch } from 'react-redux';
import { login } from '../store/slices/authSlice';

export default function LoginScreen({ navigation }) {
  const dispatch = useDispatch();

  const handleLogin = () => {
    dispatch(login({ name: 'Student', id: '12345' }));
    navigation.navigate('Home');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>�� Student Login</Text>
      <Text style={styles.subtitle}>Attendance System</Text>
      <Button title="Tap to Login (Demo)" onPress={handleLogin} color="#6200ee" />
      <Text style={styles.note}>Demo Mode - No password needed</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 20,
    marginBottom: 40,
    color: '#666',
  },
  note: {
    marginTop: 20,
    color: '#999',
    fontSize: 14,
    fontStyle: 'italic',
  },
});
