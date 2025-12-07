import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  Alert,
  ActivityIndicator,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { api } from '../app/services/api';

const LoginScreen = ({ navigation }: any) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  React.useEffect(() => {
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const isHealthy = await api.healthCheck();
      setBackendStatus(isHealthy ? 'online' : 'offline');
    } catch {
      setBackendStatus('offline');
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter username and password');
      return;
    }

    if (backendStatus === 'offline') {
      Alert.alert(
        'Backend Offline',
        'Cannot connect to server. Using demo mode.',
        [{ text: 'OK', onPress: handleDemoLogin }]
      );
      return;
    }

    setIsLoading(true);

    try {
      const data = await api.login(username, password);
      
      Alert.alert('Success', 'Login successful!');
      navigation.reset({
        index: 0,
        routes: [{ name: 'Home' }],
      });
    } catch (error: any) {
      Alert.alert('Login Failed', error.message || 'Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    
    // Demo mode - simulate API delay
    setTimeout(() => {
      Alert.alert('Demo Mode', 'Logged in with demo account');
      navigation.reset({
        index: 0,
        routes: [{ name: 'Home' }],
      });
      setIsLoading(false);
    }, 1000);
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.card}>
        <View style={styles.header}>
          <Text style={styles.title}>SAMS Login</Text>
          <Text style={styles.subtitle}>QR Scanner System</Text>
          
          <View style={[
            styles.statusBadge,
            backendStatus === 'online' && styles.statusOnline,
            backendStatus === 'offline' && styles.statusOffline,
          ]}>
            <Text style={styles.statusText}>
              {backendStatus === 'checking' ? 'Checking connection...' : 
               backendStatus === 'online' ? '✅ Backend Connected' : '⚠️ Offline Mode'}
            </Text>
          </View>
        </View>
        
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
          editable={!isLoading}
        />
        
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={!isLoading}
        />
        
        {isLoading ? (
          <ActivityIndicator size="large" color="#007AFF" style={styles.loader} />
        ) : (
          <>
            <TouchableOpacity 
              style={styles.loginButton} 
              onPress={handleLogin}
              disabled={backendStatus === 'checking'}
            >
              <Text style={styles.loginButtonText}>
                {backendStatus === 'offline' ? 'Login (Offline Mode)' : 'Login'}
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.demoButton}
              onPress={handleDemoLogin}
            >
              <Text style={styles.demoButtonText}>Use Demo Account</Text>
            </TouchableOpacity>
          </>
        )}
        
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            {backendStatus === 'online' 
              ? 'Connected to backend server'
              : 'Running in offline demo mode'}
          </Text>
          <Text style={styles.serverInfo}>
            Server: {backendStatus === 'online' ? '10.42.0.1:8000' : 'Not available'}
          </Text>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 15,
  },
  statusBadge: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    marginTop: 10,
  },
  statusOnline: {
    backgroundColor: '#d4edda',
  },
  statusOffline: {
    backgroundColor: '#f8d7da',
  },
  statusText: {
    fontSize: 14,
    fontWeight: '600',
  },
  input: {
    height: 55,
    borderWidth: 1.5,
    borderColor: '#e0e0e0',
    borderRadius: 12,
    paddingHorizontal: 20,
    marginBottom: 20,
    fontSize: 16,
    backgroundColor: '#fafafa',
  },
  loginButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    height: 55,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
    shadowColor: '#007AFF',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 3,
  },
  loginButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  demoButton: {
    height: 55,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 15,
    borderWidth: 2,
    borderColor: '#007AFF',
    borderRadius: 12,
  },
  demoButtonText: {
    color: '#007AFF',
    fontSize: 16,
    fontWeight: '600',
  },
  loader: {
    marginVertical: 30,
  },
  infoBox: {
    marginTop: 25,
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#6c757d',
  },
  infoText: {
    fontSize: 14,
    color: '#495057',
    marginBottom: 5,
  },
  serverInfo: {
    fontSize: 12,
    color: '#6c757d',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
});

export default LoginScreen;
