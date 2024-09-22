import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUploadStore = defineStore('uploadStore', () => {
  // State
  const selectedFile = ref<File | null>(null);
  const uploadStatus = ref<string | null>(null);

  // Actions
  const setSelectedFile = (file: File) => {
    selectedFile.value = file;
  };

  const uploadFile = async () => {
    if (!selectedFile.value) {
      uploadStatus.value = 'No file selected!';
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile.value);

    try {
      const token = localStorage.getItem('token');

      if (!token) {
        uploadStatus.value = 'Authentication token not found. Please login again.';
        return;
      }

      const response = await fetch('http://0.0.0.0:8100/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        uploadStatus.value = 'File uploaded successfully! You can check your mail after some time for your report';
      } else {
        uploadStatus.value = 'File upload failed. ' + (await response.text());
      }
    } catch (error) {
      uploadStatus.value = 'Error during upload.';
      console.error(error);
    }
  };
  return {
    selectedFile,
    uploadStatus,
    setSelectedFile,
    uploadFile,
  };
});
