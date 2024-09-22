
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// const apiUrl = process.env.NODE_ENV === 'development' ? 'http://backend:8100' : 'http://localhost:8100';

export const useAuthStore = defineStore('authStore', () => {

  const email = ref<string | null>(null);
  const password = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);
  const errorMessage = ref<string | null>(null);
  const router = useRouter();


  const login = async (userEmail: string, userPassword: string) => {
    email.value = userEmail;
    password.value = userPassword;

    try {
      const response = await fetch('http://0.0.0.0:8100/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: userEmail, password: userPassword }),
      });

      if (!response.ok) {
        alert('Not able to login: ' + (await response.text()));
        errorMessage.value = 'Not able to login: ' + (await response.text());
        alert('Not able to login: ' + (await response.text()));
      } else {
        const data = await response.json();  // Get token and other data
        const token = data.access_token;

        localStorage.setItem('token', token);

        isAuthenticated.value = true;
        errorMessage.value = null;

        router.replace({ path: '/upload' });
      }
      // const data = await response.json();
      // isAuthenticated.value = true;
      // errorMessage.value = null;
      // console.log('Logged in successfully', data);

      // router.push('/upload');
    } catch (error) {
      // errorMessage.value = error.message;
      console.log(error);
      isAuthenticated.value = false;
    }
  };

  const signup = async (userEmail: string, userPassword: string) => {
    email.value = userEmail;
    password.value = userPassword;
    console.log(email.value);

    try {
      const response = await fetch('http://0.0.0.0:8100/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: userEmail, password: userPassword }),
      });

      if (!response.ok) {
        throw new Error('Signup failed: ' + (await response.text()));
      }

      // const data = await response.json();
      errorMessage.value = null;
      alert('Signed up successfully');
      router.replace({ path: '/login' });
    } catch (error) {
      console.log(error);
      // errorMessage.value = error.message;
      console.log(error);
    }
  };

  const logout = () => {
    email.value = null;
    password.value = null;
    isAuthenticated.value = false;
    errorMessage.value = null;
    console.log('Logged out successfully');
  };

  return {
    email,
    password,
    isAuthenticated,
    errorMessage,
    login,
    signup,
    logout,
  };
});
