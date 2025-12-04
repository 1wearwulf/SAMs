import React from 'react';
import { View, StyleSheet, Text, ScrollView, SafeAreaView } from 'react-native';
import { useSelector } from 'react-redux';

export default function HomeScreen() {
  const { user } = useSelector((state) => state.auth);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <Text style={styles.greeting}>Welcome, {user?.name || 'Student'}!</Text>
          <Text style={styles.id}>ID: {user?.id || 'N/A'}</Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Today's Classes</Text>
          <Text style={styles.classItem}>• CS101: 10:00 AM (Room 201)</Text>
          <Text style={styles.classItem}>• MATH202: 2:00 PM (Room 104)</Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Quick Actions</Text>
          <Text style={styles.actionItem}>📷 Scan QR Code</Text>
          <Text style={styles.actionItem}>📊 View Attendance</Text>
          <Text style={styles.actionItem}>📚 My Courses</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: 'white',
    marginBottom: 15,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  id: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  card: {
    backgroundColor: 'white',
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 15,
    borderRadius: 10,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#6200ee',
    marginBottom: 15,
  },
  classItem: {
    fontSize: 16,
    color: '#333',
    marginBottom: 8,
  },
  actionItem: {
    fontSize: 16,
    color: '#333',
    marginBottom: 10,
  },
});
