module.exports = {
  apps: [

    // ============================
    // Backend API
    // ============================
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      node_args: "--max-old-space-size=512",
      max_memory_restart: "600M",
      env: {
        NODE_ENV: "production",
        PORT: 4000,
        AUTH_COOKIE_NAME: "sl_auth",
        NLP_BASE_URL: "http://127.0.0.1:8000",
        JWT_SECRET: "YOUR_SECRET_HERE",
        SYSTEM_INGEST_USER_ID: "69841d4f065476f7a38de668",

        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin",

        INGESTION_TIMEOUT_MINUTES: 30,
        INGESTION_MAX_RETRIES: 3,
        INGESTION_MAX_CONCURRENT: 8,
        INGESTION_MAX_QUEUE: 200
      }
    },

    // ============================
    // Auto Enqueue Worker
    // ============================
    {
      name: "sl-auto-enqueue",
      script: "dist/workers/ingestionAutoEnqueue.worker.js",
      cwd: "/var/www/solvelitigation/backend",
      node_args: "--max-old-space-size=256",
      max_memory_restart: "300M",
      env: {
        NODE_ENV: "production",

        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin",

        INGESTION_MAX_CONCURRENT: 8,
        INGESTION_MAX_QUEUE: 200,
        INGESTION_AUTO_ENQUEUE_INTERVAL: 15000
      }
    },

    // ============================
    // Queue Processor Worker
    // ============================
    {
      name: "sl-queue-processor",
      script: "dist/workers/queuedIngestion.worker.js",
      cwd: "/var/www/solvelitigation/backend",
      node_args: "--max-old-space-size=256",
      max_memory_restart: "300M",
      env: {
        NODE_ENV: "production",
        NLP_BASE_URL: "http://127.0.0.1:8000",

        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin",

        INGESTION_MAX_CONCURRENT: 8
      }
    }

  ]
};
