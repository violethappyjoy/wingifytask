<template>
    <div class="container-login">
        <Card style="width: 40%;">
            <CardHeader>
                <CardTitle>Login</CardTitle>
            </CardHeader>
            <CardContent>
                <form @submit.prevent="handleLogin">
                <Label for="email">Email</Label>
                <Input
                    id="email"
                    type="email"
                    v-model="email"
                    autocomplete="off"
                    :class="{ 'input-error': !isValidEmail && email.length > 0 }"
                />
                <p v-if="!isValidEmail && email.length > 0" class="error-message">
                    Please enter a valid email address.
                </p>

                <Label for="password">Password</Label>
                <Input id="password" type="password" v-model="password" autocomplete="off" />

                <Button type="submit" class="custom-button" :disabled="!validPassword" >Login</Button>
            </form>
            </CardContent>
            <CardFooter>
            </CardFooter>
        </Card>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue';
  import { useAuthStore } from '@/stores/authStore';
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from '@/components/ui/card';
  
  const authStore = useAuthStore();
  const email = ref('');
  const password = ref('');

  const validPassword = computed(() => {
    return password.value.length >= 8;
  });
  
  const isValidEmail = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email.value);
});
  

  const handleLogin = () => {
    authStore.login(email.value, password.value);
  };
  
  const errorMessage = authStore.errorMessage;


  </script>
  
  <style scoped>
  /* Centering the login form on the page */
  .container-login {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .custom-button {
    padding: 10px 20px; /* Adds padding to the button */
    margin-top: 15px; /* Adds space between the button and input fields */
  }
  
  form {
    display: flex;
    flex-direction: column;
    width: 300px; /* Set the width of the form */
  }
  
  input {
    margin-bottom: 10px; /* Adds space between input fields */
  }
  
  /* Styling for error message */
  .error-message {
    color: red;
    margin-top: 10px;
  }
  </style>
  