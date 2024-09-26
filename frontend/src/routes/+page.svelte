<script lang="ts">
  import { onMount } from 'svelte';

  let file: File | null = null;

  const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      file = input.files[0];
    }
  };

  // Animation variables
  let titleStyle = { transform: 'translateX(-200px)', opacity: 0 };

  onMount(() => {
    // Animate the title on mount
    titleStyle = { transform: 'translateX(0)', opacity: 1 };
  });
</script>

<style>
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100vh;
    padding: 0 20px;
  }
  
  .title {
    font-size: 2rem;
    font-weight: bold;
    transition: transform 1s, opacity 1s;
  }
  
  .upload-button {
    background-color: #0070f3;
    color: #fff;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  input[type="file"] {
    display: none;
  }
</style>

<div class="container">
  <h1 class="title" style="transform: {titleStyle.transform}; opacity: {titleStyle.opacity};">
    Welcome to the Kenyare Underwriter
  </h1>

  <div>
    <label class="upload-button">
      Upload
      <input type="file" on:change={handleFileChange} />
    </label>
  </div>
</div>

{#if file}
  <p>Selected File: {file.name}</p>
{/if}
