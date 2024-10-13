import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	preview: {
		port: parseInt(process.env.VITE_PROD_PORT ?? "4173")
	},
	server: {
		port: parseInt(process.env.VITE_DEV_PORT ?? "5173")
	}
});
