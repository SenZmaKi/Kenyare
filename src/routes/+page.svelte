<script lang="ts">
  import Main from "../components/Main.svelte";
  import { Toast, Button } from "flowbite-svelte";
  import { onMount } from "svelte";
  import {
    CheckCircleSolid,
    CloseCircleSolid,
    UploadSolid,
  } from "flowbite-svelte-icons";
  import QuotationInputModal from "../components/QuotationInputModal.svelte";
  import { Fileupload, Label } from "flowbite-svelte";
  import { testQuotationInput, type QuotationInput } from "$lib/types";

  let financialAuditFileList: FileList | undefined = undefined;
  let proposalFormFileList: FileList | undefined = undefined;

  // let quotationInput: QuotationInput | null = testQuotationInput;
  let quotationInput: QuotationInput | null = null;
  let isLoading = false;
  let toastIsError = false;
  let toastText = "";
  let toastShowTimeout: NodeJS.Timeout | null = null;
  const defaultHometext = "Welcome to the Kenyare AI Underwriter";
  let homeText = defaultHometext;

  function showToast(text: string, isError = false, duration_ms = 4000) {
    if (toastShowTimeout) {
      clearTimeout(toastShowTimeout);
    }
    toastText = text;
    toastShowTimeout = setTimeout(() => {
      toastText = "";
    }, duration_ms);
    toastIsError = isError;
  }

  let homeTextLoadingInterval: NodeJS.Timeout | null = null;
  let currentPeriodCount = 1;
  let maxPeriodCount = 3;
  let homeTextLoading = "";

  function updateHometextLoading() {
    if (currentPeriodCount > maxPeriodCount) {
      currentPeriodCount = 0;
    }
    homeTextLoading = `${".".repeat(currentPeriodCount)}`;
    currentPeriodCount++;
  }

  function showLoading(task: string) {
    isLoading = true;
    homeText = task;
    if (homeTextLoadingInterval) {
      clearInterval(homeTextLoadingInterval);
    }
    homeTextLoadingInterval = setInterval(() => {
      updateHometextLoading();
    }, 200);
  }

  function resetLoading() {
    isLoading = false;
    if (homeTextLoadingInterval) {
      clearInterval(homeTextLoadingInterval);
    }
    homeTextLoading = "";
    homeText = defaultHometext;
  }

  async function uploadFiles(proposalForm: File, financialAudit: File) {
    if (!financialAudit.name.endsWith(".pdf")) {
      showToast("Financial audit must be a PDF", true);
      return;
    }
    if (!proposalForm.name.endsWith(".pdf")) {
      showToast("Proposal form must be a PDF", true);
      return;
    }
    showLoading("Uploading");
    const formData = new FormData();
    formData.append("proposalForm", proposalForm);
    formData.append("financialAudit", financialAudit);
    console.log("Uploading...");
    let success = false;
    try {
      const upload_resp = await fetch("/quotation/upload", {
        method: "POST",
        body: formData,
      });
      success = upload_resp.ok;
    } catch (error) {
      console.error(error);
    }
    if (!success) {
      console.log("Error uploading");
      resetLoading();
      showToast("Failed to upload", true);
      return false;
    }
    console.log("Uploaded!");
    return true;
  }

  async function getQuotationInput() {
    showLoading("Extracting proposal info");
    showToast("This may take a while...", false);
    console.log("Extracting...");
    let success = false;
    try {
      const input_resp = await fetch("/quotation/input", {
        method: "GET",
      });
      success = input_resp.ok;
      if (success) {
        const resp_json = await input_resp.json();
        quotationInput = resp_json.data.quotation_input;
        console.log("Extracted!");
      }
    } catch (error) {
      console.error(error);
    }
    resetLoading();
    if (!success) {
      console.log("Error extracting");
      showToast("Failed to extract proposal info", true);
      return;
    }
  }

  async function uploadAndExtract() {
    console.log("Upload and extract");
    if (!proposalFormFileList && !financialAuditFileList) {
      showToast("Please add both files", true);
      return;
    }
    if (!proposalFormFileList) {
      showToast("Please add a proposal form", true);
      return;
    }
    if (!financialAuditFileList) {
      showToast("Please add a financial audit", true);
      return;
    }
    const success = await uploadFiles(
      proposalFormFileList[0],
      financialAuditFileList[0]
    );
    if (!success) return;
    await getQuotationInput();
  }

  // DEBUG
  //  $: if (proposalFormFileList && financialAuditFileList) uploadAndExtract();

  onMount(() => {
    titleStyle = { transform: "translateX(0)", opacity: 1 };
  });
  let titleStyle = { transform: "translateX(-200px)", opacity: 0 };
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
    <QuotationInputModal
      {quotationInput}
      {showToast}
      {showLoading}
      {resetLoading}
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
      {homeText}
      <span class="">
        {homeTextLoading}
      </span>
    </h1>
    <div class="z-10 flex flex-col gap-6 items-center">
      <div class="z-10 flex gap-6">
        <Label class="space-y-2">
          <span>Financial audit</span>
          <Fileupload bind:files={financialAuditFileList} />
        </Label>
        <Label class="space-y-2 ">
          <span>Proposal form</span>
          <Fileupload bind:files={proposalFormFileList} />
        </Label>
      </div>
      <Button
        class="flex gap-2 w-min hover:scale-110 ease-in-out duration-300"
        on:click={uploadAndExtract}
      >
        <div>Upload</div>
        <UploadSolid />
      </Button>
    </div>

    <div />
  </div></Main
>

<style>
  .title {
    font-size: 3rem;
    font-weight: bold;
    transition:
      transform 4s,
      opacity 4s;
  }
</style>
