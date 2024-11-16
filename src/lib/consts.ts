const FLASK_PORT = process.env.FLASK_PORT ?? 5000;
const FLASK_HOST = process.env.FLASK_HOST ?? "http://127.0.0.1";
export const API_BASE_URL = `${FLASK_HOST}:${FLASK_PORT}`;