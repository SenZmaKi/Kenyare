<script lang="ts">
  import type { NullableQuotationInput } from "$lib/types";
  import { Label } from "flowbite-svelte";
  import { ExclamationCircleSolid } from "flowbite-svelte-icons";
  export let title: string;
  export let field: keyof NullableQuotationInput;
  export let nullableQuotationInput: NullableQuotationInput;
</script>

<div class="flex items-center gap-1">
  <Label class="pl-2" for={field}>{title}</Label>
  {#if nullableQuotationInput[field] === null}
    <ExclamationCircleSolid size="sm" color="red" />
  {/if}
</div>
