<script lang="ts">
  import { Label, Input, Button, Toggle, Modal } from "flowbite-svelte";
  import { quotationOutput } from "$lib/store";
  import {
    UsersGroupSolid,
    BriefcaseSolid,
    CalendarMonthSolid,
    CashSolid,
    ProfileCardOutline,
    UploadOutline,
  } from "flowbite-svelte-icons";
  import { type QuotationInput } from "$lib/types";
  import { goto } from "$app/navigation";
  export let quotationInput: QuotationInput;
  export let open: boolean;
  export let isLoading: boolean;
  export let showToast: (text: string, isError?: boolean) => void;
  function convertQuotationInputToProperFormat(quotationInput: QuotationInput) {
    return {
      reinsured_name: quotationInput.reinsured_name,
      broker_name: quotationInput.broker_name,
      insured_name: quotationInput.insured_name,
      // @ts-ignore
      partners_count: parseInt(quotationInput.partners_count),
      qualified_assistants_count: parseInt(
        // @ts-ignore
        quotationInput.qualified_assistants_count
      ),
      unqualified_assistants_count: parseInt(
        // @ts-ignore
        quotationInput.unqualified_assistants_count
      ),
      // @ts-ignore
      others_count: parseInt(quotationInput.others_count),
      // @ts-ignore
      annual_fees: parseFloat(quotationInput.annual_fees),
      // @ts-ignore
      limit_of_indemnity: parseFloat(quotationInput.limit_of_indemnity),
      profession: quotationInput.profession,
      loss_of_documents: quotationInput.loss_of_documents,
      libel_and_slander: quotationInput.libel_and_slander,
      dishonest_employees: quotationInput.dishonest_employees,
      retroactive_cover: quotationInput.retroactive_cover,
    };
  }
  async function generateQuotation() {
    open = false;
    isLoading = true;
    const properQuotationInput =
      convertQuotationInputToProperFormat(quotationInput);
    console.log(
      `properQuotationInput: ${JSON.stringify(properQuotationInput)}`
    );
    console.log("Generating quotation...");
    const resp = await fetch("/quotation/output", {
      method: "POST",
      body: JSON.stringify({ quotation_input: properQuotationInput }),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    if (!resp.ok) {
      console.log("Error generating quotation");
      isLoading = false;
      open = false;
      showToast("Failed to generate quotation", true);
      return;
    }
    console.log("Quotation generated!");
    const resp_json = await resp.json();
    $quotationOutput = resp_json.data.quotation_output;
    console.log($quotationOutput);
    isLoading = false;
    goto("/quotation/output/");
  }
</script>

<Modal title="Quotation Input" size="lg" bind:open autoclose>
  <div class="z-0 flex flex-col m-auto mt-2 justify-center items-center">
    <div class=" flex-col p-2 mb-5 grid gap-10 border rounded-lg">
      <div class="flex gap-5 justify-between">
        <div class="pb-1 flex flex-col">
          <div class="flex items-center">
            <ProfileCardOutline />
            <Label class="pl-2" for="reinsured_name">Reinsured</Label>
          </div>
          <Input
            id="reinsured_name"
            bind:value={quotationInput.reinsured_name}
          />
        </div>
        <div class="pb-1">
          <div class="flex items-center">
            <ProfileCardOutline />
            <Label class="pl-2" for="broker_name">Broker</Label>
          </div>
          <Input id="broker_name" bind:value={quotationInput.broker_name} />
        </div>
        <div class="pb-1">
          <div class="flex items-center">
            <ProfileCardOutline />
            <Label class="pl-2" for="insured_name">Insured</Label>
          </div>
          <Input id="insured_name" bind:value={quotationInput.insured_name} />
        </div>
      </div>
      <div class="flex gap-5 justify-between">
        <div>
          <div class="pb-1 flex items-center">
            <UsersGroupSolid />
            <Label class="pl-2" for="partners_count">Partners</Label>
          </div>
          <Input
            id="partners_count"
            type="number"
            bind:value={quotationInput.partners_count}
          />
        </div>
        <div>
          <div class="pb-1 flex items-center">
            <UsersGroupSolid />
            <Label class="pl-2" for="qualified_assistants_count"
              >Qualified assistants</Label
            >
          </div>
          <Input
            id="qualified_assistants_count"
            bind:value={quotationInput.qualified_assistants_count}
            type="number"
            placeholder="Qualified Assistants Count"
          />
        </div>
        <div>
          <div class="pb-1 flex items-center">
            <UsersGroupSolid />
            <Label class="pl-2" for="unqualified_assistants_count"
              >Unqualified assistants</Label
            >
          </div>
          <Input
            id="unqualified_assistants_count"
            type="number"
            bind:value={quotationInput.unqualified_assistants_count}
            placeholder="Unqualified Assistants Count"
          />
        </div>
        <div>
          <div class="pb-1 flex items-center">
            <UsersGroupSolid />
            <Label class="pl-2" for="others_count">Other employees</Label>
          </div>
          <Input
            id="others_count"
            type="number"
            bind:value={quotationInput.others_count}
            placeholder="Others Count"
          />
        </div>
      </div>
      <div class="flex gap-4 justify-between">
        <div>
          <div class="flex pb-1">
            <CalendarMonthSolid />
            <Label class="pl-2">Annual fees</Label>
          </div>

          <Input
            id="annual_fees"
            type="number"
            bind:value={quotationInput.annual_fees}
            placeholder="Annual Fees"
          />
        </div>
        <div class="">
          <div class="flex pb-1">
            <CashSolid />
            <Label class="pl-2" for="limit_of_indemnity"
              >Limit of indemnity</Label
            >
          </div>
          <Input
            id="limit_of_indemnity"
            type="number"
            bind:value={quotationInput.limit_of_indemnity}
            placeholder="Limit of Indemnity"
          />
        </div>
        <div>
          <div class="flex items-center pb-1">
            <BriefcaseSolid />
            <Label class="pl-2" for="profession">Profession</Label>
          </div>
          <Input
            id="profession"
            bind:value={quotationInput.profession}
            placeholder="Profession"
          />
        </div>
      </div>
      <div class="flex gap-5 justify-between">
        <div class="pb-1 items-center flex flex-col">
          <Label>Loss of documents</Label>
          <Toggle
            class="hover:cursor-pointer"
            bind:checked={quotationInput.loss_of_documents}
          />
        </div>
        <div class="pb-1 items-center flex flex-col">
          <Label>Libel and slander</Label>
          <Toggle
            class="hover:cursor-pointer"
            bind:checked={quotationInput.libel_and_slander}
          />
        </div>
        <div class="pb-1 items-center flex flex-col">
          <Label>Dishonest employees</Label>
          <Toggle
            class="hover:cursor-pointer"
            bind:checked={quotationInput.dishonest_employees}
          />
        </div>

        <div class="pb-1 items-center flex flex-col">
          <Label>Retroactive cover</Label>
          <Toggle
            class="hover:cursor-pointer"
            bind:checked={quotationInput.retroactive_cover}
          />
        </div>
      </div>
    </div>
    <Button
      on:click={generateQuotation}
      slot="footer"
      class="z-0 hover:scale-110 duration-300 ease-in-out"
    >
      <div class="flex items-center gap-2">
        <p>Generate quotation</p>
        <UploadOutline />
      </div>
    </Button>
    <div />
  </div></Modal
>

<style>
</style>
