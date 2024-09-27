import { writable } from 'svelte/store';

export let quotationOutput = writable<QuotationOutput | null>(null);