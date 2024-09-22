<template>
    <div class="container-upload">
        <Card >
        <CardHeader>
            <CardTitle>PDF Uploader</CardTitle>
        </CardHeader>
        <CardContent>
            <input type="file" accept="application/pdf" @change="onFileChange" />
            <Button class="custom-button" @click="uploadFile" :disabled="!selectedFile">
            Upload PDF
            </Button>
            <p v-if="uploadStatus">{{ uploadStatus }}</p>
        </CardContent>
        </Card>
    </div>
</template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useUploadStore } from '@/stores/uploadStore';
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from '@/components/ui/card';
  import { Button } from '@/components/ui/button';
  
  const uploadStore = useUploadStore();
  const selectedFile = computed(() => uploadStore.selectedFile);
  const uploadStatus = computed(() => uploadStore.uploadStatus);
  
  const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      uploadStore.setSelectedFile(target.files[0]);
    }
  };
  
  const uploadFile = () => {
    uploadStore.uploadFile();
  };
  </script>
  
  <style scoped>
  .container-upload {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  

  .custom-button {
    padding: 10px 20px; 
    margin-top: 15px;
  }
  
  
  input[type="file"] {
    margin-bottom: 10px;
  }
  </style>
  