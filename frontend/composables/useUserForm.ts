import { reactive } from 'vue';
import { useAuth } from './useAuth';

interface UserFormData {
  id?: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export function useUserForm() {
  const { token } = useAuth();
  
  // Common form data structure
  const form = reactive<UserFormData>({
    email: '',
    role: '',
    is_active: true,
    created_at: '',
    updated_at: ''
  });

  // Common role and active status options
  const roles = [
    { label: 'Member', value: 'member' },
    { label: 'Manager', value: 'manager' },
    { label: 'Admin', value: 'admin' }
  ];
  
  const activeOptions = [
    { label: 'Active', value: true },
    { label: 'Inactive', value: false }
  ];

  // Set form data with proper data typing
  function setFormData(userData: Partial<UserFormData>) {
    if (!userData) return;
    
    form.id = userData.id;
    form.email = userData.email || '';
    
    // Ensure role is properly set from incoming data and has a default
    if (userData.role && typeof userData.role === 'string') {
      form.role = userData.role;
    } else {
      form.role = 'member'; // Default when no role is provided
    }
    
    // Handle boolean is_active value explicitly to ensure proper type
    if (userData.is_active !== undefined) {
      if (typeof userData.is_active === 'boolean') {
        form.is_active = userData.is_active;
      } else if (userData.is_active === 1 || userData.is_active === '1' || userData.is_active === 'true') {
        form.is_active = true;
      } else {
        form.is_active = false;
      }
    } else {
      form.is_active = true; // Default when not provided
    }
    
    form.created_at = userData.created_at || '';
    form.updated_at = userData.updated_at || '';
    
    // Log to help with debugging
    console.log('Form data set:', { 
      role: form.role, 
      is_active: form.is_active,
      userData
    });
  }

  // Clear the form
  function clearForm() {
    form.id = undefined;
    form.email = '';
    form.role = 'member'; // Always default to member
    form.is_active = true; // Always default to active
    form.created_at = '';
    form.updated_at = '';
  }

  // Get updatable fields for API
  function getUpdatableFields() {
    return {
      role: form.role,
      is_active: form.is_active
    };
  }

  // Update user (can be for current user or specific user by ID)
  async function updateUser(userId?: string) {
    if (!token.value) return false;
    
    const endpoint = userId 
      ? `http://localhost:8000/users/${userId}` 
      : 'http://localhost:8000/users/me';
    
    try {
      const res = await fetch(endpoint, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token.value}`
        },
        body: JSON.stringify(getUpdatableFields())
      });
      
      return res.ok;
    } catch (error) {
      console.error('Error updating user:', error);
      return false;
    }
  }

  // Delete user (can be for current user or specific user by ID)
  async function deleteUser(userId?: string) {
    if (!token.value) return false;
    
    const endpoint = userId 
      ? `http://localhost:8000/users/${userId}` 
      : 'http://localhost:8000/users/me';
    
    try {
      const res = await fetch(endpoint, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      });
      
      return res.ok;
    } catch (error) {
      console.error('Error deleting user:', error);
      return false;
    }
  }

  // Fetch user data (current user or all users)
  async function fetchUserData(fetchAll = false): Promise<UserFormData | UserFormData[] | null> {
    if (!token.value) return null;
    
    const endpoint = fetchAll 
      ? 'http://localhost:8000/users'
      : 'http://localhost:8000/users/me';
    
    try {
      const res = await fetch(endpoint, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      });
      
      if (res.ok) {
        return await res.json();
      }
      return null;
    } catch (error) {
      console.error('Error fetching user data:', error);
      return null;
    }
  }

  // Create a new user
  async function createUser(email: string, password: string): Promise<{ success: boolean; error?: string }> {
    if (!token.value) return { success: false, error: 'Not authenticated' };
    
    try {
      const res = await fetch('http://localhost:8000/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token.value}`
        },
        body: JSON.stringify({ email, password })
      });
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        return { 
          success: false, 
          error: err.detail || 'User creation failed' 
        };
      }
      
      return { success: true };
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : 'Unknown error';
      return { 
        success: false, 
        error: errorMessage || 'User creation failed' 
      };
    }
  }

  return {
    form,
    roles,
    activeOptions,
    setFormData,
    clearForm,
    updateUser,
    deleteUser,
    fetchUserData,
    createUser
  };
}