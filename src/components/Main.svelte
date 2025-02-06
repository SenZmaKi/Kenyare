<script lang="ts">
  export let isLoading = false;
  import { Spinner } from "flowbite-svelte";

  let currentImageNum = 1;
  const totalImages = 5;
  setInterval(() => {
    currentImageNum += 1;
    if (currentImageNum > totalImages) currentImageNum = 1;
  }, 5000);
  const imageNumToUrl = (i: number) => `/backgrounds/${i}.png`;
</script>

<div>
  <!-- Preload images -->
  {#each Array(totalImages) as _, i}
    <link rel="preload" as="image" href={imageNumToUrl(i + 1)} />
  {/each}

  <div
  class="absolute inset-0 bg-center bg-cover opacity-30 -z-10"
    style="background-image: url({imageNumToUrl(
      currentImageNum
    )}); transition: background-image 1s;"
  ></div>

  <a href="/" class="absolute top-0 left-0 m-4">
    <img
      src="/favicon.png"
      alt="logo"
      class="w-10 h-10 rounded-full ease-in-out hover:scale-125 duration-200"
    />
  </a>

  {#if isLoading}
    <!-- Centered and on top of everything -->
    <div class="absolute inset-0 flex justify-center items-center">
      <Spinner size={20} />
    </div>
  {/if}

  <div class="">
    <slot />
  </div>
</div>
