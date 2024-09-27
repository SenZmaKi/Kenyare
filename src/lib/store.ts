import { writable } from 'svelte/store';
import { type QuotationOutput } from '$lib/types';

export let quotationOutput = writable<QuotationOutput | null>(null);