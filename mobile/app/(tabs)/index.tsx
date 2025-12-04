import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator, RefreshControl } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { useStore } from "../store/useStore";

export default function HomeScreen() {
  const router = useRouter();
  const { user, courses, attendanceRecords, isLoading, loadCourses, loadAttendance } = useStore();
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadCourses();
    loadAttendance();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([loadCourses(), loadAttendance()]);
    setRefreshing(false);
  };

  const quickActions = [
    { title: "Scan QR", icon: "qr-code", screen: "scan", color: "#6200ee" },
    { title: "My Courses", icon: "book", screen: "courses", color: "#03dac6" },
    { title: "Attendance", icon: "calendar", screen: "attendance", color: "#ff0266" },
    { title: "Profile", icon: "person", screen: "profile", color: "#3700b3" },
  ];

  const overallAttendance = courses.length > 0 
    ? Math.round(courses.reduce((sum, course) => sum + course.attendance, 0) / courses.length)
    : 0;

  const today = new Date().toISOString().split('T')[0];
  const todayAttendance = attendanceRecords.filter(r => r.date === today && r.status === 'Present').length;

  if (isLoading && courses.length === 0 && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#6200ee" />
        <Text style={styles.loadingText}>Loading your data...</Text>
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#6200ee" />
      }
    >
      <View style={styles.header}>
        <Text style={styles.greeting}>Welcome back,</Text>
        <Text style={styles.name}>{user?.name || 'Student'}</Text>
        <Text style={styles.id}>ID: {user?.studentId || 'N/A'}</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{overallAttendance}%</Text>
          <Text style={styles.statLabel}>Overall</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{courses.length}</Text>
          <Text style={styles.statLabel}>Courses</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{todayAttendance}</Text>
          <Text style={styles.statLabel}>Today</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={styles.actionCard}
              onPress={() => router.push('/(tabs)/' + action.screen)}
            >
              <View style={[styles.iconContainer, { backgroundColor: action.color }]}>
                <Ionicons name={action.icon as any} size={30} color="white" />
              </View>
              <Text style={styles.actionTitle}>{action.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Attendance</Text>
        {attendanceRecords.slice(0, 3).map((record, index) => (
          <View key={index} style={styles.attendanceCard}>
            <View style={styles.attendanceHeader}>
              <Text style={styles.attendanceCourse}>{record.course}</Text>
              <View style={[
                styles.attendanceStatus,
                { backgroundColor: record.status === 'Present' ? '#4CAF50' : '#F44336' }
              ]}>
                <Text style={styles.attendanceStatusText}>{record.status}</Text>
              </View>
            </View>
            <Text style={styles.attendanceDate}>{record.date}</Text>
          </View>
        ))}
        {attendanceRecords.length === 0 && (
          <Text style={styles.noDataText}>No attendance records yet</Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Today's Classes</Text>
        <View style={styles.classCard}>
          <Text style={styles.classTitle}>Computer Science 101</Text>
          <Text style={styles.classTime}>10:00 AM - 11:30 AM</Text>
          <Text style={styles.classRoom}>Room: CS-201</Text>
        </View>
        <View style={styles.classCard}>
          <Text style={styles.classTitle}>Mathematics 202</Text>
          <Text style={styles.classTime}>2:00 PM - 3:30 PM</Text>
          <Text style={styles.classRoom}>Room: MATH-104</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  loadingText: {
    marginTop: 10,
    color: "#666",
  },
  header: {
    padding: 20,
    backgroundColor: "white",
    marginBottom: 15,
  },
  greeting: {
    fontSize: 16,
    color: "#666",
  },
  name: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#333",
    marginTop: 5,
  },
  id: {
    fontSize: 14,
    color: "#999",
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: "row",
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: "white",
    padding: 15,
    marginHorizontal: 5,
    borderRadius: 10,
    alignItems: "center",
    elevation: 2,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#6200ee",
  },
  statLabel: {
    fontSize: 12,
    color: "#666",
    marginTop: 5,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 15,
    color: "#333",
  },
  actionsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
  },
  actionCard: {
    width: "48%",
    backgroundColor: "white",
    padding: 20,
    borderRadius: 10,
    alignItems: "center",
    marginBottom: 15,
    elevation: 2,
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 10,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#333",
  },
  attendanceCard: {
    backgroundColor: "white",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    elevation: 2,
  },
  attendanceHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 5,
  },
  attendanceCourse: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#333",
  },
  attendanceStatus: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
  },
  attendanceStatusText: {
    color: "white",
    fontSize: 12,
    fontWeight: "600",
  },
  attendanceDate: {
    fontSize: 14,
    color: "#666",
  },
  noDataText: {
    textAlign: "center",
    color: "#999",
    fontStyle: "italic",
    padding: 20,
  },
  classCard: {
    backgroundColor: "white",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    elevation: 2,
  },
  classTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#333",
    marginBottom: 5,
  },
  classTime: {
    fontSize: 14,
    color: "#666",
    marginBottom: 3,
  },
  classRoom: {
    fontSize: 14,
    color: "#666",
  },
});
