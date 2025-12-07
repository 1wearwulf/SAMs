import { View, Text, StyleSheet, ScrollView } from "react-native";

export default function CoursesScreen() {
  const courses = [
    { code: "CS101", name: "Computer Science 101", instructor: "Dr. Smith" },
    { code: "MATH202", name: "Mathematics 202", instructor: "Prof. Johnson" },
    { code: "PHY101", name: "Physics 101", instructor: "Dr. Williams" },
    { code: "ENG201", name: "Engineering 201", instructor: "Prof. Brown" },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>My Courses</Text>
        <Text style={styles.subtitle}>Spring 2024 Semester</Text>
      </View>

      {courses.map((course, index) => (
        <View key={index} style={styles.courseCard}>
          <View style={styles.courseHeader}>
            <Text style={styles.courseCode}>{course.code}</Text>
            <View style={styles.statusBadge}>
              <Text style={styles.statusText}>Active</Text>
            </View>
          </View>
          <Text style={styles.courseName}>{course.name}</Text>
          <Text style={styles.instructor}>Instructor: {course.instructor}</Text>
          <View style={styles.statsRow}>
            <Text style={styles.stat}>Attendance: 92%</Text>
            <Text style={styles.stat}>Next: Mon 10:00 AM</Text>
          </View>
        </View>
      ))}
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
    marginBottom: 10,
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
  courseCard: {
    backgroundColor: "white",
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 15,
    borderRadius: 10,
    elevation: 2,
  },
  courseHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 10,
  },
  courseCode: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#6200ee",
  },
  statusBadge: {
    backgroundColor: "#03dac6",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 5,
  },
  statusText: {
    color: "white",
    fontSize: 12,
    fontWeight: "bold",
  },
  courseName: {
    fontSize: 20,
    fontWeight: "600",
    color: "#333",
    marginBottom: 5,
  },
  instructor: {
    fontSize: 14,
    color: "#666",
    marginBottom: 10,
  },
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: "#eee",
  },
  stat: {
    fontSize: 14,
    color: "#666",
  },
});
