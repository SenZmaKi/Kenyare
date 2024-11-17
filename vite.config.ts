import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import "dotenv/config";

export default defineConfig({
	plugins: [sveltekit()],
	preview: {
		host: process.env.VITE_PROD_HOST ?? '127.0.0.1',
		port: parseInt(process.env.VITE_PROD_PORT ?? "4173")
	},
	server: {
		host: process.env.VITE_DEV_HOST ?? '127.0.0.1',
		port: parseInt(process.env.VITE_DEV_PORT ?? "5173")
	}
});
