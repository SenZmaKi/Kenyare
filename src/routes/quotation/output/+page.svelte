<script lang="ts">
  import { Table, TableBodyCell, TableBodyRow, Button } from "flowbite-svelte";
  import { DownloadSolid } from "flowbite-svelte-icons";
  import Main from "../../../components/Main.svelte";
  import { quotationOutput as quotationOutputStore } from "$lib/store";
  import { testQuotationOutput } from "$lib/types";

  // let quotationOutput = testQuotationOutput;
  let quotationOutput = $quotationOutputStore;
  function toPercentStr(value: number) {
    return (value * 100).toFixed(3) + "%";
  }
</script>

<Main>
  {#if quotationOutput}
    <div class="flex flex-col justify-center items-center p-10">
      <div class="flex pb-5 justify-center items-center">
        <p class="text-xl pr-5 font-bold">Professional Indemnity Quotation</p>

        <a
          href={quotationOutput.excel_download_url}
          download={quotationOutput.input.insured_name
            ? `${quotationOutput.input.insured_name.toLowerCase().replaceAll(" ", "-")}-quotation.xlsx`
            : "quotation.xlsx"}
        >
          <Button
            class="flex p-2 gap-2 ease-in-out duration-300 hover:scale-110"
            color="green"
          >
            <p>Download Excel</p>
            <DownloadSolid />
          </Button>
        </a>
      </div>
      <Table class="border " striped={true} hoverable={true}>
        <TableBodyRow>
          <TableBodyCell>Reinsured</TableBodyCell>
          <TableBodyCell>{quotationOutput.input.reinsured_name}</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Broker</TableBodyCell>
          <TableBodyCell>{quotationOutput.input.broker_name}</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Insured</TableBodyCell>
          <TableBodyCell>{quotationOutput.input.insured_name}</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Partners/Principal</TableBodyCell>
          <TableBodyCell>{quotationOutput.partners.original}</TableBodyCell>
          <TableBodyCell
            >{quotationOutput.partners.rate.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell
            >{quotationOutput.partners.value.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Qualified Assistants</TableBodyCell>
          <TableBodyCell
            >{quotationOutput.qualified_assistants.original}</TableBodyCell
          >
          <TableBodyCell>
            {quotationOutput.qualified_assistants.rate.toFixed(2)}
          </TableBodyCell>
          <TableBodyCell>
            {quotationOutput.qualified_assistants.value.toFixed(2)}
          </TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Unqualified Assistants</TableBodyCell>
          <TableBodyCell>
            {quotationOutput.unqualified_assistants.original}
          </TableBodyCell>
          <TableBodyCell>
            {quotationOutput.unqualified_assistants.rate.toFixed(2)}
          </TableBodyCell>
          <TableBodyCell>
            {quotationOutput.unqualified_assistants.value.toFixed(2)}
          </TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Others</TableBodyCell>
          <TableBodyCell>{quotationOutput.others.original}</TableBodyCell>
          <TableBodyCell>{quotationOutput.others.rate.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell
            >{quotationOutput.others.value.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Annual fees</TableBodyCell>
          <TableBodyCell
            >{quotationOutput.annual_fees.original.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell
            >{toPercentStr(quotationOutput.annual_fees.rate)}</TableBodyCell
          >
          <TableBodyCell
            >{quotationOutput.annual_fees.value.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell class="bg-gray-300"
            >{quotationOutput.A.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell>A</TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Limit of indemnity</TableBodyCell>
          <TableBodyCell
            >{quotationOutput.limit_of_indemnity.original.toFixed(
              2
            )}</TableBodyCell
          >
          <TableBodyCell
            >{toPercentStr(
              quotationOutput.limit_of_indemnity.rate
            )}</TableBodyCell
          >
          <TableBodyCell class="bg-gray-300"
            >{quotationOutput.limit_of_indemnity.value.toFixed(
              2
            )}</TableBodyCell
          >
          <TableBodyCell>B</TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Profession</TableBodyCell>
          <TableBodyCell>{quotationOutput.profession.original}</TableBodyCell>
          <TableBodyCell
            >{toPercentStr(quotationOutput.profession.rate)}</TableBodyCell
          >
          <TableBodyCell class="bg-gray-300"
            >{quotationOutput.profession.value.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell>C</TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell class="bg-yellow-100"
            >{quotationOutput.A_B_C.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell>A+B+C</TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell>Extensions</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Loss of documents @10% of LOI</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell
            >{quotationOutput.loss_of_documents.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Libel and slander @10% of LOI</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell
            >{quotationOutput.libel_and_slander.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Dishonest of employees @10% of LOI</TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell
            >{quotationOutput.dishonest_employees.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Basic premium</TableBodyCell>
          <TableBodyCell class="bg-yellow-100"
            >{quotationOutput.basic_premium.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Levies</TableBodyCell>
          <TableBodyCell>{quotationOutput.levies.toFixed(2)}</TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>

        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>SD</TableBodyCell>
          <TableBodyCell>{quotationOutput.sd.toFixed(2)}</TableBodyCell>
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
        <TableBodyRow>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell></TableBodyCell>
          <TableBodyCell>Total premium</TableBodyCell>
          <TableBodyCell class="bg-green-300"
            >{quotationOutput.total_premium.toFixed(2)}</TableBodyCell
          >
          <TableBodyCell></TableBodyCell>
        </TableBodyRow>
      </Table>
    </div>
  {/if}
</Main>
