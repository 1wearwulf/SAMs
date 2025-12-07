/**
 * User model representing a user in the SAMS system
 */
export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: 'student' | 'lecturer' | 'admin';
    is_active: boolean;
    date_joined?: string;
    last_login?: string;
}

/**
 * User profile model with additional profile information
 */
export interface UserProfile extends User {
    phone_number?: string;
    address?: string;
    date_of_birth?: string;
    profile_picture?: string;
}

/**
 * Create a full name from first and last name
 */
export function getFullName(user: User): string {
    if (user.first_name && user.last_name) {
        return `${user.first_name} ${user.last_name}`.trim();
    }
    return user.username;
}

/**
 * Check if user has a specific role
 */
export function hasRole(user: User, role: 'student' | 'lecturer' | 'admin'): boolean {
    return user.role === role;
}

/**
 * Check if user is a student
 */
export function isStudent(user: User): boolean {
    return hasRole(user, 'student');
}

/**
 * Check if user is a lecturer
 */
export function isLecturer(user: User): boolean {
    return hasRole(user, 'lecturer');
}

/**
 * Check if user is an admin
 */
export function isAdmin(user: User): boolean {
    return hasRole(user, 'admin');
}

/**
 * Get role display name
 */
export function getRoleDisplayName(role: 'student' | 'lecturer' | 'admin'): string {
    switch (role) {
        case 'student':
            return 'Student';
        case 'lecturer':
            return 'Lecturer';
        case 'admin':
            return 'Administrator';
        default:
            return 'Unknown';
    }
}
