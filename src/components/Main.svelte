<script lang="ts">
  export let isLoading = false;
  import { Spinner } from "flowbite-svelte";

  let currentImageIndex = 1;
  const totalImages = 5;
  setInterval(() => {
    currentImageIndex = (currentImageIndex % totalImages) + 1;
  }, 8000);
</script>

<div>
  <div
    class="absolute inset-0 bg-center bg-cover opacity-30 z-0"
    style="background-image: url('/backgrounds/{currentImageIndex}.png'); transition: background-image 1s;"
  ></div>

  <a href="/" class="absolute top-0 left-0 m-4 z-50">
    <img
      src="/favicon.png"
      alt="logo"
      class="w-10 h-10 rounded-full ease-in-out hover:scale-125 duration-200"
    />
  </a>

  {#if isLoading}
    <!-- Centered and on top of everything -->
    <div class="absolute inset-0 flex justify-center items-center z-50">
      
      <Spinner size={20} />
    </div>
  {/if}

  <div class="z-10">
    <slot />
  </div>
</div>
