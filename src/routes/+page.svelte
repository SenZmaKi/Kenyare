<script lang="ts">
  import Main from "../components/Main.svelte";
  import { Button, Toast } from "flowbite-svelte";
  import { onMount } from "svelte";
  import { CheckCircleSolid, CloseCircleSolid } from "flowbite-svelte-icons";
  import QuotationInput from "../components/QuotationInput.svelte";

  let file: File | null = null;
  let fileInput: HTMLInputElement | null = null;
  let toastIsError = false;
  let toastText = "";
  let toastShowTimeout: NodeJS.Timeout | null = null;
  const showToast = (text: string, isError = false, duration_ms = 4000) => {
    if (toastShowTimeout) {
      clearTimeout(toastShowTimeout);
    }
    toastText = text;
    toastShowTimeout = setTimeout(() => {
      toastText = "";
    }, duration_ms);
    toastIsError = isError;
  };
  import { type QuotationInput as QuotationInputType } from "$lib/types";
  let quotationInput: QuotationInputType | null = null;
  let isLoading = false;
  const handleFileChange = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      file = input.files[0];
      if (!file.type.includes("pdf")) {
        console.log("Error invalid file type");
        showToast("Please upload a PDF file", true);
        return;
      }
      isLoading = true;
      const formData = new FormData();
      formData.append("file", file);
      console.log("Uploading...");
      const upload_resp = await fetch("/quotation/upload", {
        method: "POST",
        body: formData,
      });
      if (!upload_resp.ok) {
        console.log("Error uploading");
        isLoading = false;
        showToast("Failed to upload file", true);
        return;
      }
      console.log("Uploaded!");
      showToast("Uploaded! Extracting proposal info...");
      console.log("Extracting...");
      const input_resp = await fetch("/quotation/input", {
        method: "GET",
      });
      if (!input_resp.ok) {
        console.log("Error extracting");
        isLoading = false;
        showToast("Failed to extract proposal info", true);
        return;
      }
      console.log("Extracted!");
      const resp_json = await input_resp.json();
      isLoading = false;
      quotationInput = resp_json.data.quotation_input;
      //   quotationInput = {
      //     reinsured_name: "FEKAN HOWELL",
      //     broker_name: "RSI",
      //     insured_name: "FEKAN HOWELL",
      //     partners_count: 3,
      //     qualified_assistants_count: 7,
      //     unqualified_assistants_count: 0,
      //     others_count: 0,
      //     annual_fees: 70_000_000,
      //     limit_of_indemnity: 100_000_000,
      //     profession:
      //       "AUDIT, TAX AND ADVISORY SERVICES(CERTIFIED PUBLIC ACCOUNTANTS)",
      //     loss_of_documents: true,
      //     libel_and_slander: true,
      //     dishonest_employees: true,
      //     retroactive_cover: false,
      //   };
    }
  };

  const triggerFilePick = () => {
    if (fileInput) {
      fileInput.click();
    }
  };

  onMount(() => {
    titleStyle = { transform: "translateX(0)", opacity: 1 };
  });
  let titleStyle = { transform: "translateX(-200px)", opacity: 0 };

  let currentImageIndex = 1;
  const totalImages = 5;
  setInterval(() => {
    currentImageIndex = (currentImageIndex % totalImages) + 1;
  }, 5000);
  let defaultModal = true;
</script>

<Main {isLoading}>
  {#if toastText}
    <Toast
      class="absolute top-0 right-0 toast"
      on:close={() => (toastText = "")}
      color={toastIsError ? "red" : "green"}
    >
      <svelte:fragment slot="icon">
        {#if toastIsError}
          <CloseCircleSolid class="w-5 h-5" />
        {:else}
          <CheckCircleSolid class="w-5 h-5" />
        {/if}
      </svelte:fragment>
      {toastText}
    </Toast>
  {/if}
  {#if quotationInput}
    <QuotationInput
      {quotationInput}
      {showToast}
      bind:isLoading
      open={!!quotationInput}
    />
  {/if}
  <div
    class="z-10 justify-center items-center h-screen flex flex-col space-y-20"
  >
    <h1
      class="z-10 title"
      style="transform: {titleStyle.transform}; opacity: {titleStyle.opacity};"
    >
      Welcome to the Kenyare AI Underwriter
    </h1>

    <Button
      on:click={triggerFilePick}
      class="z-10 duration-300 ease-in-out hover:scale-110"
    >
      <div class="font-bold text-lg mt-2 mr-4">Upload Proposal form</div>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        version="1.1"
        width="40"
        height="40"
        viewBox="0 0 256 256"
        xml:space="preserve"
      >
        <defs> </defs>
        <g
          style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;"
          transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)"
        >
          <path
            d="M 86.554 26.164 v 58.519 c 0 2.937 -2.381 5.317 -5.317 5.317 H 22.076 c -2.937 0 -5.317 -2.381 -5.317 -5.317 V 71.549 V 5.317 C 16.759 2.381 19.139 0 22.076 0 h 38.315 C 68.66 0.135 86.554 16.011 86.554 26.164 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(226,226,226); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 16.833 21.859 H 57.1 c 3.218 0 5.827 2.609 5.827 5.827 v 18.341 c 0 3.218 -2.609 5.827 -5.827 5.827 H 9.273 c -3.218 0 -5.827 -2.609 -5.827 -5.827 V 16.032"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(241,86,66); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 3.446 16.032 c 0 3.218 2.609 5.827 5.827 5.827 h 7.56 V 10.552 h -7.56 c -3.218 0 -5.827 2.609 -5.827 5.827"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(190,64,48); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 60.391 0 h 6.662 c 2.826 0 5.536 1.123 7.534 3.121 l 8.847 8.847 c 1.998 1.998 3.121 4.708 3.121 7.534 v 6.662 c 0 -3.419 -2.772 -6.19 -6.19 -6.19 h -7.866 c -3.268 0 -5.917 -2.649 -5.917 -5.917 c 0 0 0 -7.866 0 -7.866 v 0 C 66.581 2.772 63.81 0 60.391 0 C 60.391 0 60.391 0 60.391 0 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(183,183,183); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 20.708 27.68 h -5.489 c -0.829 0 -1.5 0.671 -1.5 1.5 v 9.1 v 6.231 c 0 0.829 0.671 1.5 1.5 1.5 s 1.5 -0.671 1.5 -1.5 V 39.78 h 3.989 c 2.272 0 4.122 -1.849 4.122 -4.121 v -3.858 C 24.829 29.529 22.98 27.68 20.708 27.68 z M 21.829 35.659 c 0 0.618 -0.503 1.121 -1.122 1.121 h -3.989 v -6.1 h 3.989 c 0.619 0 1.122 0.503 1.122 1.121 V 35.659 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 34.554 27.68 h -5.22 c -0.829 0 -1.5 0.671 -1.5 1.5 v 15.332 c 0 0.829 0.671 1.5 1.5 1.5 h 5.22 c 2.421 0 4.391 -1.97 4.391 -4.391 v -9.55 C 38.945 29.65 36.976 27.68 34.554 27.68 z M 35.945 41.621 c 0 0.767 -0.624 1.391 -1.391 1.391 h -3.72 V 30.68 h 3.72 c 0.767 0 1.391 0.624 1.391 1.391 V 41.621 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 51.841 27.68 h -8.11 c -0.829 0 -1.5 0.671 -1.5 1.5 v 15.332 c 0 0.829 0.671 1.5 1.5 1.5 s 1.5 -0.671 1.5 -1.5 v -6.166 h 3.812 c 0.828 0 1.5 -0.671 1.5 -1.5 s -0.672 -1.5 -1.5 -1.5 H 45.23 V 30.68 h 6.61 c 0.828 0 1.5 -0.671 1.5 -1.5 S 52.669 27.68 51.841 27.68 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
          <path
            d="M 45.142 69.824 c -0.587 0.586 -1.536 0.586 -2.122 0 l -5.248 -5.248 v 15.642 c 0 0.828 -0.671 1.5 -1.5 1.5 s -1.5 -0.672 -1.5 -1.5 V 64.576 l -5.248 5.248 c -0.586 0.586 -1.535 0.586 -2.121 0 s -0.586 -1.535 0 -2.121 l 6.323 -6.323 c 0.625 -0.625 1.424 -0.955 2.243 -1.024 c 0.098 -0.02 0.2 -0.031 0.304 -0.031 s 0.206 0.011 0.304 0.031 c 0.818 0.069 1.618 0.399 2.243 1.024 l 6.323 6.323 C 45.727 68.289 45.727 69.238 45.142 69.824 z"
            style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(183,183,183); fill-rule: nonzero; opacity: 1;"
            transform=" matrix(1 0 0 1 0 0) "
            stroke-linecap="round"
          />
        </g>
      </svg>
    </Button>

    <!-- Hidden File Input -->
    <input
      type="file"
      bind:this={fileInput}
      on:change={handleFileChange}
      style="display: none;"
    />
  </div>
</Main>

<style>
  .title {
    font-size: 3rem;
    font-weight: bold;
    transition:
      transform 4s,
      opacity 4s;
  }

  input[type="file"] {
    display: none;
  }
</style>
