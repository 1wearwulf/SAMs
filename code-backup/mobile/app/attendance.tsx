import { View, Text, StyleSheet, ScrollView } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function AttendanceScreen() {
  const attendanceRecords = [
    { date: "2024-01-15", course: "CS101", status: "Present", time: "10:00 AM" },
    { date: "2024-01-15", course: "MATH202", status: "Present", time: "2:00 PM" },
    { date: "2024-01-14", course: "PHY101", status: "Absent", time: "9:00 AM" },
    { date: "2024-01-13", course: "ENG201", status: "Present", time: "11:00 AM" },
    { date: "2024-01-12", course: "CS101", status: "Present", time: "10:00 AM" },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Attendance Records</Text>
        <Text style={styles.subtitle}>Spring 2024 Semester</Text>
      </View>

      <View style={styles.summaryCard}>
        <Text style={styles.summaryTitle}>Attendance Summary</Text>
        <View style={styles.summaryStats}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryNumber}>85%</Text>
            <Text style={styles.summaryLabel}>Overall</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryNumber}>42</Text>
            <Text style={styles.summaryLabel}>Present</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryNumber}>7</Text>
            <Text style={styles.summaryLabel}>Absent</Text>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Records</Text>
        {attendanceRecords.map((record, index) => (
          <View key={index} style={styles.recordCard}>
            <View style={styles.recordHeader}>
              <Text style={styles.courseCode}>{record.course}</Text>
              <View style={[
                styles.statusBadge,
                { backgroundColor: record.status === "Present" ? "#4CAF50" : "#F44336" }
              ]}>
                <Ionicons 
                  name={record.status === "Present" ? "checkmark-circle" : "close-circle"} 
                  size={16} 
                  color="white" 
                />
                <Text style={styles.statusText}>{record.status}</Text>
              </View>
            </View>
            <Text style={styles.recordDate}>{record.date} • {record.time}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  header: {
    padding: 20,
    backgroundColor: "white",
    marginBottom: 15,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#333",
  },
  subtitle: {
    fontSize: 16,
    color: "#666",
    marginTop: 5,
  },
  summaryCard: {
    backgroundColor: "white",
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 20,
    borderRadius: 10,
    elevation: 2,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 15,
    color: "#333",
  },
  summaryStats: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  summaryItem: {
    alignItems: "center",
  },
  summaryNumber: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#6200ee",
  },
  summaryLabel: {
    fontSize: 14,
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
  recordCard: {
    backgroundColor: "white",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    elevation: 2,
  },
  recordHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 5,
  },
  courseCode: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#333",
  },
  statusBadge: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
  },
  statusText: {
    color: "white",
    fontSize: 14,
    fontWeight: "600",
    marginLeft: 5,
  },
  recordDate: {
    fontSize: 14,
    color: "#666",
  },
});
