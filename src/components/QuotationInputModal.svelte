<script lang="ts">
  import { Label, Input, Button, Toggle, Modal } from "flowbite-svelte";
  import { quotationOutput } from "$lib/store";
  import {
    ClipboardListSolid,
    BadgeCheckSolid,
    CloseCircleSolid,
    UsersGroupSolid,
    BriefcaseSolid,
    CalendarMonthSolid,
    CashSolid,
    ProfileCardOutline,
    UploadOutline,
    ExclamationCircleSolid,
  } from "flowbite-svelte-icons";
  import {
    testQuotationInput,
    type NullableQuotationInput,
    type QuotationInput,
    type UserQuotationInput,
  } from "$lib/types";
  import { goto } from "$app/navigation";
  import FieldTitle from "./FieldTitle.svelte";
  import { fade, fly } from "svelte/transition";

  export let nullableQuotationInput: NullableQuotationInput =
    testQuotationInput;
  export let open: boolean;
  export let showToast: (text: string, isError?: boolean) => void;
  export let showLoading: (task: string) => void;
  export let resetLoading: () => void;

  $: showFinancialSummary = !nullableQuotationInput.is_profitable;
  let userQuotationInput: UserQuotationInput;
  $: userQuotationInput = {
    qualified_assistants_count: (
      nullableQuotationInput.qualified_assistants_count ?? 0
    ).toString(),
    unqualified_assistants_count: (
      nullableQuotationInput.unqualified_assistants_count ?? 0
    ).toString(),
    others_count: (nullableQuotationInput.others_count ?? 0).toString(),
    annual_fees: (nullableQuotationInput.annual_fees ?? 0).toString(),
    limit_of_indemnity: (
      nullableQuotationInput.limit_of_indemnity ?? 0
    ).toString(),
    partners_count: (nullableQuotationInput.partners_count ?? 0).toString(),
    reinsured_name: nullableQuotationInput.reinsured_name ?? "",
    broker_name: nullableQuotationInput.broker_name ?? "",
    insured_name: nullableQuotationInput.insured_name ?? "",
    is_profitable: !!nullableQuotationInput.is_profitable,
    financial_summary: nullableQuotationInput.financial_summary ?? "",
    profession: nullableQuotationInput.profession ?? "",
    loss_of_documents: !!nullableQuotationInput.loss_of_documents,
    libel_and_slander: !!nullableQuotationInput.libel_and_slander,
    dishonest_employees: !!nullableQuotationInput.dishonest_employees,
    retroactive_cover: !!nullableQuotationInput.retroactive_cover,
  };

  function convertUserQIToQI(): QuotationInput {
    return {
      ...userQuotationInput,

      partners_count: parseInt(userQuotationInput.partners_count),
      qualified_assistants_count: parseInt(
        userQuotationInput.qualified_assistants_count
      ),
      unqualified_assistants_count: parseInt(
        userQuotationInput.unqualified_assistants_count
      ),
      others_count: parseInt(userQuotationInput.others_count),
      annual_fees: parseFloat(userQuotationInput.annual_fees),
      limit_of_indemnity: parseFloat(userQuotationInput.limit_of_indemnity),
    };
  }

  async function generateQuotation() {
    open = false;
    showLoading("Generating quotation");
    console.log("Generating quotation...");
    const quotation_input = convertUserQIToQI();
    console.log(`quotation_input: ${JSON.stringify(quotation_input)}`);
    let success = false;
    try {
      const resp = await fetch("/quotation/output", {
        method: "POST",
        body: JSON.stringify({ quotation_input }),
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      success = resp.ok;
      if (success) {
        console.log("Quotation generated!");
        const resp_json = await resp.json();
        $quotationOutput = resp_json.data.quotation_output;
      }
    } catch (error) {
      console.error(error);
    }
    if (!success) {
      console.log("Error generating quotation");
      showToast("Failed to generate quotation", true);
      resetLoading();
      return;
    }
    console.log($quotationOutput);
    await goto("/quotation/output/");
    resetLoading();
  }
</script>

<Modal
  title={showFinancialSummary ? "Financial Summary" : "Quotation Input"}
  size="lg"
  bind:open
  autoclose={false}
>
  <div class="overflow-x-clip">
    {#if showFinancialSummary}
      <div
        class="flex flex-col m-auto mt-2 justify-center items-center p-4"
        in:fly={{ x: 1000, duration: 500 }}
      >
        <div class="flex gap-2 items-center">
          {#if nullableQuotationInput.is_profitable}
            <BadgeCheckSolid size="md" color="green" />
            <Label class="text-green-500 text-base"
              >The organisation is profitable</Label
            >
          {:else if nullableQuotationInput.is_profitable === null}
            <ExclamationCircleSolid size="md" color="red" />
            <Label class="text-red-500 text-base"
              >Failed to determine whether the organization is profitable</Label
            >
          {:else}
            <CloseCircleSolid size="md" color="red" />
            <Label class="text-red-500 text-base"
              >The organization is not profitable</Label
            >
          {/if}
        </div>
        {#if nullableQuotationInput.financial_summary}
          <p class="p-4">{nullableQuotationInput.financial_summary}</p>
        {/if}
        <slot name="footer">
          <div class="items-center flex">
            <Button
              class="hover:scale-110 duration-300 ease-in-out"
              color="green"
              on:click={() => (showFinancialSummary = false)}
            >
              <div class="flex items-center gap-2">
                <p>Quotation input</p>
                <ClipboardListSolid />
              </div>
            </Button>
          </div>
        </slot>
      </div>
    {:else}
      <div class="flex flex-col" in:fly={{ x: -1000, duration: 500 }}>
        <div class="pl-7 text-xs text-gray-400 italic mt-2 flex gap-1">
          <ExclamationCircleSolid size="sm" color="red" />
          means the field could not be extracted so it may require manual input.
        </div>
        <div class="flex flex-col m-auto mt-2 justify-center items-center">
          <div class=" flex-col p-2 mb-5 grid gap-10 border rounded-lg">
            <div class="flex gap-5 justify-between">
              <div class="pb-1 flex flex-col">
                <div class="flex items-center">
                  <ProfileCardOutline />
                  <FieldTitle
                    title="Reinsured"
                    field="reinsured_name"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="reinsured_name"
                  bind:value={userQuotationInput.reinsured_name}
                />
              </div>
              <div class="pb-1">
                <div class="flex items-center">
                  <ProfileCardOutline />
                  <FieldTitle
                    title="Broker"
                    field="broker_name"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="broker_name"
                  bind:value={userQuotationInput.broker_name}
                />
              </div>
              <div class="pb-1">
                <div class="flex items-center">
                  <ProfileCardOutline />
                  <FieldTitle
                    title="Insured name"
                    field="insured_name"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="insured_name"
                  bind:value={userQuotationInput.insured_name}
                />
              </div>
            </div>
            <div class="flex gap-5 justify-between">
              <div>
                <div class="pb-1 flex items-center">
                  <UsersGroupSolid />
                  <FieldTitle
                    title="Partners"
                    field="partners_count"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="partners_count"
                  type="number"
                  bind:value={userQuotationInput.partners_count}
                />
              </div>
              <div>
                <div class="pb-1 flex items-center">
                  <UsersGroupSolid />
                  <FieldTitle
                    title="Qualified assistants"
                    field="qualified_assistants_count"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="qualified_assistants_count"
                  bind:value={userQuotationInput.qualified_assistants_count}
                  type="number"
                  placeholder="Qualified Assistants Count"
                />
              </div>
              <div>
                <div class="pb-1 flex items-center">
                  <UsersGroupSolid />
                  <FieldTitle
                    title="Unqualified assistants"
                    field="unqualified_assistants_count"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="unqualified_assistants_count"
                  type="number"
                  bind:value={userQuotationInput.unqualified_assistants_count}
                  placeholder="Unqualified Assistants Count"
                />
              </div>
              <div>
                <div class="pb-1 flex items-center">
                  <UsersGroupSolid />
                  <FieldTitle
                    title="Other employees"
                    field="others_count"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="others_count"
                  type="number"
                  bind:value={userQuotationInput.others_count}
                  placeholder="Others Count"
                />
              </div>
            </div>
            <div class="flex gap-4 justify-between">
              <div>
                <div class="flex pb-1">
                  <CalendarMonthSolid />
                  <FieldTitle
                    title="Annual fees"
                    field="annual_fees"
                    {nullableQuotationInput}
                  />
                </div>

                <Input
                  id="annual_fees"
                  type="number"
                  bind:value={userQuotationInput.annual_fees}
                  placeholder="Annual Fees"
                />
              </div>
              <div class="">
                <div class="flex pb-1">
                  <CashSolid />
                  <FieldTitle
                    title="Limit of indemnity"
                    field="limit_of_indemnity"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="limit_of_indemnity"
                  type="number"
                  bind:value={userQuotationInput.limit_of_indemnity}
                  placeholder="Limit of Indemnity"
                />
              </div>
              <div>
                <div class="flex items-center pb-1">
                  <BriefcaseSolid />
                  <FieldTitle
                    title="Profession"
                    field="profession"
                    {nullableQuotationInput}
                  />
                </div>
                <Input
                  id="profession"
                  bind:value={userQuotationInput.profession}
                  placeholder="Profession"
                />
              </div>
            </div>
            <div class="flex gap-5 justify-between">
              <div class="pb-1 items-center flex flex-col">
                <FieldTitle
                  title="Loss of documents"
                  field="loss_of_documents"
                  {nullableQuotationInput}
                />
                <Toggle
                  class="hover:cursor-pointer"
                  bind:checked={userQuotationInput.loss_of_documents}
                />
              </div>
              <div class="pb-1 items-center flex flex-col">
                <FieldTitle
                  title="Libel and slander"
                  field="libel_and_slander"
                  {nullableQuotationInput}
                />
                <Toggle
                  class="hover:cursor-pointer"
                  bind:checked={userQuotationInput.libel_and_slander}
                />
              </div>
              <div class="pb-1 items-center flex flex-col">
                <FieldTitle
                  title="Dishonest employees"
                  field="dishonest_employees"
                  {nullableQuotationInput}
                />
                <Toggle
                  class="hover:cursor-pointer"
                  bind:checked={userQuotationInput.dishonest_employees}
                />
              </div>

              <div class="pb-1 items-center flex flex-col">
                <FieldTitle
                  title="Retroactive cover"
                  field="retroactive_cover"
                  {nullableQuotationInput}
                />
                <Toggle
                  class="hover:cursor-pointer"
                  bind:checked={userQuotationInput.retroactive_cover}
                />
              </div>
            </div>
          </div>
          <slot name="footer">
            <div class="flex gap-4">
              <Button
                on:click={generateQuotation}
                class="hover:scale-110 duration-300 ease-in-out"
              >
                <div class="flex items-center gap-2">
                  <p>Generate quotation</p>
                  <UploadOutline />
                </div>
              </Button>
              <Button
                class="hover:scale-110 duration-300 ease-in-out"
                color="green"
                on:click={() => (showFinancialSummary = true)}
              >
                <div class="flex items-center gap-2">
                  <p>Financial summary</p>
                  <CashSolid />
                </div>
              </Button>
            </div>
          </slot>
          <div />
        </div>
      </div>
    {/if}
  </div>
</Modal>
