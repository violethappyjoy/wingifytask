<template>
    <div class="container-main">
        <Card>
            <CardHeader>
                <CardTitle>Welcome To Your personal healtheres</CardTitle>
                <CardDescription>Signup or Login for system healtherers</CardDescription>
            </CardHeader>
            <CardContent>
                <Button class="custom-button"><router-link to="/login">Login</router-link></Button>
                <Button class="custom-button"><router-link to="/signup">Signup</router-link></Button>
            </CardContent>
            <CardFooter>
            </CardFooter>
        </Card>
    </div>
</template>
  
<script setup lang="ts">

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button';


</script>

<style scoped>

.container-main {
  display: flex;
  justify-content: center; 
  align-items: center; 
  height: 100vh; 
}

.custom-button {
  padding: 10px 20px; 
  margin: 10px; 
}



.container-main > * {
  width: 40%;
}

</style>
